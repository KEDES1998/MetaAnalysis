"""
utils_meta.py -- shared functions for the meta-analysis
(replication and update of Zschirnt & Ruedin 2016).

Effect size everywhere: log odds ratio (ln OR) of a call-back,
minority applicants vs. majority applicants.
    ln OR < 0  ->  minority is called back less often (discrimination)

Conventions
-----------
y   : effect sizes (ln OR), 1-d array
se  : standard errors of y
v   : sampling variances, v = se**2

Fixed- and random-effects intervals use the normal distribution (as metafor
in R, which the original paper used). Regression-based estimators (UWLS,
WAAP, FAT-PET, WLS meta-regression) use the t distribution with k - p degrees
of freedom (as lm() in R, see Winkelmann's notes).

Only numpy, pandas, scipy and matplotlib are needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

import matplotlib

matplotlib.use("Agg")  # write files only, no window
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import transforms  # noqa: E402

# ---------------------------------------------------------------------------
# Paths (all relative to the repository root)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "01_data"
RAW = DATA / "raw_files"
FIG = ROOT / "04_report" / "figures"
TAB = ROOT / "04_report" / "tables"
TMP = ROOT / "03_tmp"

STUDIES_CSV = DATA / "zr2016_studies.csv"      # 34 studies (study level)
SUBGROUPS_CSV = DATA / "zr2016_subgroups.csv"  # 215 subgroups
UPDATE_CSV = DATA / "update_studies.csv"       # new studies (filled in by hand)
COMBINED_CSV = DATA / "combined_studies.csv"   # original + new studies

Z975 = stats.norm.ppf(0.975)                   # 1.959964
Z_POWER80 = Z975 + stats.norm.ppf(0.80)        # 2.8016: se <= |mu| / 2.8 -> power >= 80 %


def ensure_dirs() -> None:
    """Create the output folders if they do not exist yet."""
    for p in (FIG, TAB, TMP):
        p.mkdir(parents=True, exist_ok=True)


# Region coding as in the original replication file (meta-replication.Rmd),
# extended by further European OECD countries for the new studies.
# Note: the UK counts as EU (as in the original, all UK studies are pre-Brexit).
NORTH_AMERICA = {"US", "Canada"}
EUROPE = {"Austria", "Belgium", "France", "Germany", "Greece", "Ireland", "Italy",
          "Netherlands", "Norway", "Poland", "Spain", "Sweden", "Switzerland", "UK",
          # not in the original, possible in the update:
          "Denmark", "Finland", "Portugal", "Luxembourg", "Czech Republic", "Hungary",
          "Slovakia", "Slovenia", "Estonia", "Latvia", "Lithuania", "Iceland"}
EU = EUROPE - {"Norway", "Switzerland", "Iceland"}
GERMAN_SPEAKING = {"Austria", "Germany", "Switzerland"}
COUNTRY_ALIASES = {"USA": "US", "United States": "US", "United Kingdom": "UK",
                   "Great Britain": "UK", "Czechia": "Czech Republic"}


def region_variables(country: pd.Series) -> pd.DataFrame:
    """continent, europe, eu, german_speaking from the country name (original coding).

    Countries not in the sets above are coded as 'Other' -- add them if needed.
    """
    c = country.astype(str).str.strip().replace(COUNTRY_ALIASES)
    return pd.DataFrame({
        "continent": np.where(c.isin(NORTH_AMERICA), "North America",
                              np.where(c.isin(EUROPE), "Europe", "Other")),
        "europe": c.isin(EUROPE).astype(int),
        "eu": c.isin(EU).astype(int),
        "german_speaking": c.isin(GERMAN_SPEAKING).astype(int),
    }, index=country.index)


# ---------------------------------------------------------------------------
# Effect sizes
# ---------------------------------------------------------------------------
def log_odds_ratio(cb_min, nocb_min, cb_maj, nocb_maj, add: float = 0.5):
    """ln OR and its standard error from the 2x2 table of call-backs.

    a = call-backs minority, b = no call-back minority,
    c = call-backs majority, d = no call-back majority.

        OR = (a / b) / (c / d),   SE(ln OR) = sqrt(1/a + 1/b + 1/c + 1/d)

    As in metafor's escalc(measure = "OR"): if a row has a zero cell,
    `add` (0.5) is added to all four cells of that row.
    """
    a, b, c, d = (np.asarray(x, dtype=float) for x in (cb_min, nocb_min, cb_maj, nocb_maj))
    zero = (a == 0) | (b == 0) | (c == 0) | (d == 0)
    a, b, c, d = (np.where(zero, x + add, x) for x in (a, b, c, d))
    y = np.log((a * d) / (b * c))
    se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return y, se


def se_from_ci(ci_low, ci_high, level: float = 0.95):
    """SE of ln OR from a confidence interval reported on the OR scale.

        SE = (ln UL - ln LL) / (2 * 1.96)
    """
    z = stats.norm.ppf(0.5 + level / 2)
    return (np.log(np.asarray(ci_high, float)) - np.log(np.asarray(ci_low, float))) / (2 * z)


def _prep(y, se):
    y = np.asarray(y, dtype=float)
    se = np.asarray(se, dtype=float)
    if y.shape != se.shape:
        raise ValueError("y and se must have the same length")
    if np.any(~np.isfinite(y)) or np.any(~np.isfinite(se)) or np.any(se <= 0):
        raise ValueError("y and se must be finite and se > 0")
    return y, se


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------
@dataclass
class MetaResult:
    """Pooled estimate of one meta-analytic method (on the ln OR scale)."""

    method: str
    k: int
    est: float
    se: float
    ci_low: float
    ci_upp: float
    tau2: float = np.nan
    Q: float = np.nan
    I2: float = np.nan        # percent
    pi_low: float = np.nan    # 95 % prediction interval (random effects only)
    pi_upp: float = np.nan
    dist: str = "z"           # "z" or "t"
    df: float = np.inf

    @property
    def p(self) -> float:
        stat = self.est / self.se
        if self.dist == "t":
            return 2 * stats.t.sf(abs(stat), self.df)
        return 2 * stats.norm.sf(abs(stat))

    @property
    def OR(self) -> float:
        return float(np.exp(self.est))

    def as_dict(self) -> dict:
        return {
            "method": self.method,
            "k": self.k,
            "log_or": self.est,
            "se": self.se,
            "ci_low": self.ci_low,
            "ci_upp": self.ci_upp,
            "OR": np.exp(self.est),
            "OR_ci_low": np.exp(self.ci_low),
            "OR_ci_upp": np.exp(self.ci_upp),
            "tau2": self.tau2,
            "I2": self.I2,
            "Q": self.Q,
            "OR_pi_low": np.exp(self.pi_low),
            "OR_pi_upp": np.exp(self.pi_upp),
            "p": self.p,
        }

    def __str__(self) -> str:
        s = (f"{self.method:<28} k={self.k:<4} lnOR={self.est: .4f} (SE {self.se:.4f})  "
             f"OR={np.exp(self.est):.3f} [{np.exp(self.ci_low):.3f}; {np.exp(self.ci_upp):.3f}]")
        if np.isfinite(self.tau2):
            s += f"  tau2={self.tau2:.4f}"
        if np.isfinite(self.I2):
            s += f"  I2={self.I2:.1f}%"
        return s


@dataclass
class RegResult:
    """Coefficients of a (meta-)regression."""

    method: str
    names: list
    coef: np.ndarray
    se: np.ndarray
    k: int
    df: float
    dist: str = "t"
    sigma: float = np.nan     # residual standard error (WLS only)
    tau2: float = np.nan      # residual heterogeneity (random-effects regression only)

    def table(self) -> pd.DataFrame:
        stat = self.coef / self.se
        if self.dist == "t":
            p = 2 * stats.t.sf(np.abs(stat), self.df)
            crit = stats.t.ppf(0.975, self.df)
        else:
            p = 2 * stats.norm.sf(np.abs(stat))
            crit = Z975
        return pd.DataFrame(
            {"coef": self.coef, "se": self.se, "stat": stat, "p": p,
             "ci_low": self.coef - crit * self.se, "ci_upp": self.coef + crit * self.se},
            index=self.names,
        )

    def __getitem__(self, name: str) -> pd.Series:
        return self.table().loc[name]

    def __str__(self) -> str:
        head = f"{self.method}  (k = {self.k}"
        if np.isfinite(self.sigma):
            head += f", residual SE = {self.sigma:.3f}"
        if np.isfinite(self.tau2):
            head += f", tau2 = {self.tau2:.4f}"
        return head + ")\n" + self.table().round(4).to_string()


# ---------------------------------------------------------------------------
# Weighted least squares (multiplicative error, like lm(..., weights = w))
# ---------------------------------------------------------------------------
def wls(y, X, w, names=None, method: str = "WLS") -> RegResult:
    """WLS with Var(e_i) = sigma^2 / w_i, sigma^2 estimated from the residuals.

    This is the regression used for UWLS, WAAP, FAT-PET and the WLS
    meta-regression (Stanley & Doucouliagos 2012). Same as lm(y ~ X, weights = w).
    """
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    w = np.asarray(w, float)
    k, p = X.shape
    if k <= p:
        raise ValueError(f"need more observations ({k}) than coefficients ({p})")
    sw = np.sqrt(w)
    Xs, ys = X * sw[:, None], y * sw
    beta, *_ = np.linalg.lstsq(Xs, ys, rcond=None)
    resid = ys - Xs @ beta
    df = k - p
    sigma2 = float(resid @ resid) / df
    cov = sigma2 * np.linalg.inv(Xs.T @ Xs)
    names = list(names) if names is not None else [f"x{j}" for j in range(p)]
    return RegResult(method, names, beta, np.sqrt(np.diag(cov)), k, df, "t", sigma=np.sqrt(sigma2))


# ---------------------------------------------------------------------------
# Heterogeneity
# ---------------------------------------------------------------------------
def q_statistic(y, se) -> float:
    """Cochran's Q around the fixed-effect mean."""
    y, se = _prep(y, se)
    w = 1 / se**2
    mu = np.sum(w * y) / np.sum(w)
    return float(np.sum(w * (y - mu) ** 2))


def _P_matrix(v, X, tau2):
    """P = W - W X (X'WX)^-1 X'W  with W = diag(1 / (v + tau2))."""
    w = 1 / (v + tau2)
    WX = X * w[:, None]
    return np.diag(w) - WX @ np.linalg.inv(X.T @ WX) @ WX.T


def tau2_dl(y, v, X) -> float:
    """DerSimonian-Laird estimator of the between-study variance."""
    k, p = X.shape
    P = _P_matrix(v, X, 0.0)
    Q = float(y @ P @ y)
    return max(0.0, (Q - (k - p)) / np.trace(P))


def _upper_bound(y, v):
    return max(10.0 * float(np.var(y)), 1.0) + 10.0 * float(np.max(v))


def tau2_pm(y, v, X) -> float:
    """Paule-Mandel estimator: tau2 such that the generalised Q equals k - p."""
    k, p = X.shape

    def f(t2):
        return float(y @ _P_matrix(v, X, t2) @ y) - (k - p)

    if f(0.0) <= 0:
        return 0.0
    hi = _upper_bound(y, v)
    while f(hi) > 0:
        hi *= 2
    return optimize.brentq(f, 0.0, hi, xtol=1e-12)


def tau2_reml(y, v, X) -> float:
    """Restricted maximum likelihood estimator (default of metafor::rma)."""

    def neg_restricted_loglik(t2):
        w = 1 / (v + t2)
        XtWX = X.T @ (X * w[:, None])
        P = _P_matrix(v, X, t2)
        _, logdet = np.linalg.slogdet(XtWX)
        return 0.5 * (np.sum(np.log(v + t2)) + logdet + float(y @ P @ y))

    hi = _upper_bound(y, v)
    res = optimize.minimize_scalar(neg_restricted_loglik, bounds=(0.0, hi), method="bounded",
                                   options={"xatol": 1e-12})
    t2 = float(res.x)
    # boundary solution at tau2 = 0?
    if neg_restricted_loglik(0.0) <= neg_restricted_loglik(t2):
        return 0.0
    return t2


TAU2_ESTIMATORS = {"DL": tau2_dl, "PM": tau2_pm, "REML": tau2_reml}


def _i2_metafor(se, tau2) -> float:
    """I^2 as reported by metafor: tau2 / (tau2 + typical within-study variance)."""
    w = 1 / se**2
    k = len(w)
    s2 = (k - 1) * np.sum(w) / (np.sum(w) ** 2 - np.sum(w**2))
    return 100 * tau2 / (tau2 + s2)


# ---------------------------------------------------------------------------
# Pooled estimators: FE, RE, UWLS
# ---------------------------------------------------------------------------
def fixed_effect(y, se, label: str = "Fixed effect (FE)") -> MetaResult:
    """Inverse-variance weighted mean, w_i = 1/se_i^2; SE = sqrt(1 / sum w_i)."""
    y, se = _prep(y, se)
    w = 1 / se**2
    mu = np.sum(w * y) / np.sum(w)
    s = np.sqrt(1 / np.sum(w))
    k = len(y)
    Q = float(np.sum(w * (y - mu) ** 2))
    I2 = max(0.0, (Q - (k - 1)) / Q) * 100 if Q > 0 else 0.0
    return MetaResult(label, k, mu, s, mu - Z975 * s, mu + Z975 * s, tau2=0.0, Q=Q, I2=I2)


def random_effects(y, se, method: str = "REML", knha: bool = False, label: str | None = None) -> MetaResult:
    """Random-effects mean with weights 1 / (se_i^2 + tau2).

    method : "REML" (as the original paper), "DL" or "PM".
    knha   : Knapp-Hartung adjustment of the SE (t distribution, k - 1 df).
    """
    y, se = _prep(y, se)
    v = se**2
    k = len(y)
    X = np.ones((k, 1))
    tau2 = TAU2_ESTIMATORS[method](y, v, X)
    w = 1 / (v + tau2)
    mu = np.sum(w * y) / np.sum(w)
    var_mu = 1 / np.sum(w)
    if knha:
        s2 = np.sum(w * (y - mu) ** 2) / (k - 1)
        var_mu *= s2
        crit, dist, df = stats.t.ppf(0.975, k - 1), "t", k - 1
    else:
        crit, dist, df = Z975, "z", np.inf
    s = np.sqrt(var_mu)
    pi_half = crit * np.sqrt(var_mu + tau2)
    if label is None:
        label = f"Random effects ({method}{', Knapp-Hartung' if knha else ''})"
    return MetaResult(label, k, mu, s, mu - crit * s, mu + crit * s, tau2=tau2,
                      Q=q_statistic(y, se), I2=_i2_metafor(se, tau2),
                      pi_low=mu - pi_half, pi_upp=mu + pi_half, dist=dist, df=df)


def uwls(y, se, label: str = "UWLS") -> MetaResult:
    """Unrestricted weighted least squares (Stanley & Doucouliagos 2015).

    OLS of t_i = y_i / se_i on 1 / se_i without a constant. The point estimate
    equals FE; the SE is the FE SE times the residual standard error
    sqrt(Q / (k - 1)), so the interval is wider than FE whenever Q > k - 1.
    """
    y, se = _prep(y, se)
    k = len(y)
    reg = wls(y, np.ones((k, 1)), 1 / se**2, names=["mean"], method=label)
    b, s = reg.coef[0], reg.se[0]
    crit = stats.t.ppf(0.975, k - 1)
    return MetaResult(label, k, b, s, b - crit * s, b + crit * s, Q=q_statistic(y, se),
                      dist="t", df=k - 1)


# ---------------------------------------------------------------------------
# Meta-regression
# ---------------------------------------------------------------------------
def design_matrix(df: pd.DataFrame, moderators: list, add_se: bool = True):
    """Design matrix [1, SE, moderators...] from a data frame (rows with NA dropped).

    Returns (y, se, X, names, used_rows).
    """
    cols = ["log_or", "se"] + list(moderators)
    d = df.dropna(subset=cols)
    X = [np.ones(len(d))]
    names = ["Intercept"]
    if add_se:
        X.append(d["se"].to_numpy(float))
        names.append("SE")
    for m in moderators:
        X.append(d[m].to_numpy(float))
        names.append(m)
    return d["log_or"].to_numpy(float), d["se"].to_numpy(float), np.column_stack(X), names, d.index


def wls_meta_regression(y, se, X, names, label: str = "WLS meta-regression") -> RegResult:
    """WLS meta-regression with weights 1/se^2 and multiplicative error (UWLS logic)."""
    y, se = _prep(y, se)
    return wls(y, X, 1 / se**2, names=names, method=label)


def re_meta_regression(y, se, X, names, method: str = "REML", knha: bool = True,
                       label: str = "RE meta-regression") -> RegResult:
    """Random-effects (mixed-effects) meta-regression as metafor::rma(yi ~ mods, knha = TRUE).

    Used to replicate the multivariate models in the original supplement (S13).
    """
    y, se = _prep(y, se)
    v = se**2
    X = np.asarray(X, float)
    k, p = X.shape
    tau2 = TAU2_ESTIMATORS[method](y, v, X)
    w = 1 / (v + tau2)
    XtWX_inv = np.linalg.inv(X.T @ (X * w[:, None]))
    beta = XtWX_inv @ X.T @ (w * y)
    cov = XtWX_inv
    if knha:
        resid = y - X @ beta
        cov = cov * (np.sum(w * resid**2) / (k - p))
        dist, df = "t", k - p
    else:
        dist, df = "z", np.inf
    return RegResult(label, list(names), beta, np.sqrt(np.diag(cov)), k, df, dist, tau2=tau2)


# ---------------------------------------------------------------------------
# Power, WAAP, publication bias
# ---------------------------------------------------------------------------
def power(se, mu, exact: bool = False):
    """Ex-post power of a two-sided 5 % test if the true effect is mu.

    Default (Winkelmann notes, Askarov et al. 2024):  q = Phi(|mu| / se - 1.96)
    exact=True adds the opposite tail Phi(-|mu| / se - 1.96).
    """
    se = np.asarray(se, float)
    m = abs(float(mu))
    q = stats.norm.cdf(m / se - Z975)
    if exact:
        q = q + stats.norm.cdf(-m / se - Z975)
    return q


def adequately_powered(se, mu):
    """True where power >= 80 %, i.e. se <= |mu| / 2.8."""
    return np.asarray(se, float) <= abs(float(mu)) / Z_POWER80


def waap(y, se, mu: float | None = None, label: str = "WAAP"):
    """Weighted average of the adequately powered (Ioannidis, Stanley & Doucouliagos 2017).

    UWLS computed only over the estimates with power >= 80 %, where power is
    evaluated at mu = UWLS estimate of all estimates. If fewer than 2 estimates
    are adequately powered, WAAP is not defined and None is returned.

    Returns (MetaResult or None, boolean mask of the adequately powered estimates).
    """
    y, se = _prep(y, se)
    if mu is None:
        mu = uwls(y, se).est
    mask = adequately_powered(se, mu)
    if mask.sum() < 2:
        return None, mask
    return uwls(y[mask], se[mask], label=label), mask


def fat_pet(y, se) -> RegResult:
    """FAT-PET meta-regression  y_i = b0 + b1 * se_i + e_i  (WLS, weights 1/se_i^2).

    b1 (FAT): funnel asymmetry / publication bias;  b1 = 0 means no bias.
    b0 (PET): effect corrected for publication bias (effect of a study with se -> 0).
    """
    y, se = _prep(y, se)
    X = np.column_stack([np.ones_like(se), se])
    return wls(y, X, 1 / se**2, names=["PET (b0)", "FAT (b1)"], method="FAT-PET")


def peese(y, se) -> RegResult:
    """PEESE  y_i = b0 + b1 * se_i^2 + e_i  (WLS, weights 1/se_i^2)."""
    y, se = _prep(y, se)
    X = np.column_stack([np.ones_like(se), se**2])
    return wls(y, X, 1 / se**2, names=["PEESE (b0)", "b1"], method="PEESE")


def reg_to_meta(reg: RegResult, row: str, label: str) -> MetaResult:
    """Turn one coefficient (e.g. PET) into a MetaResult for summary tables."""
    t = reg.table().loc[row]
    return MetaResult(label, reg.k, t["coef"], t["se"], t["ci_low"], t["ci_upp"],
                      dist=reg.dist, df=reg.df)


def ess(y, se, mu: float, tau2: float = 0.0) -> dict:
    """Excess statistical significance.

    observed : share of estimates with |y / se| > 1.96
    expected : mean probability of a significant estimate (either sign) if the
               true mean effect is mu. With tau2 > 0 the true effects vary across
               studies, y_i ~ N(mu, se_i^2 + tau2) (idea of Stanley, Doucouliagos,
               Ioannidis & Carter 2021).
    ESS = observed - expected.  Clearly positive -> hint of selection for significance.
    """
    y, se = _prep(y, se)
    sig = np.abs(y / se) > Z975
    s_tot = np.sqrt(se**2 + tau2)
    p_sig = stats.norm.cdf((mu - Z975 * se) / s_tot) + stats.norm.cdf((-mu - Z975 * se) / s_tot)
    n = len(y)
    n_sig = int(sig.sum())
    expected = float(p_sig.sum())
    var = float(np.sum(p_sig * (1 - p_sig)))
    return {
        "n": n,
        "n_sig": n_sig,
        "share_sig": n_sig / n,
        "expected_n_sig": expected,
        "expected_share": expected / n,
        "ESS": n_sig / n - expected / n,
        "z": (n_sig - expected) / np.sqrt(var) if var > 0 else np.nan,
    }


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------
def load_sample(name: str) -> pd.DataFrame | None:
    """Load an analysis sample.

    'original'              34 studies of Zschirnt & Ruedin (2016)
    'original_no_bendick'   without the outlier Bendick et al. (1991)
    'combined'              original + new studies (None if no update yet)
    """
    if name in ("original", "original_no_bendick"):
        df = pd.read_csv(STUDIES_CSV)
        if name == "original_no_bendick":
            df = df[~df["authors"].str.startswith("Bendick")]
        return df.reset_index(drop=True)
    if name == "combined":
        return pd.read_csv(COMBINED_CSV) if COMBINED_CSV.exists() else None
    raise ValueError(name)


SAMPLE_LABELS = {
    "original": "Original",
    "original_no_bendick": "Original without Bendick (1991)",
    "combined": "Original + new studies",
}


def available_samples() -> dict:
    """All samples that can be analysed right now (combined only after 03_update.py)."""
    out = {}
    for name in ("original", "original_no_bendick", "combined"):
        df = load_sample(name)
        if df is not None and len(df) > 0:
            out[name] = df
    return out


# ---------------------------------------------------------------------------
# Output helpers: LaTeX tables and macros
# ---------------------------------------------------------------------------
def fmt(x, d: int = 3) -> str:
    """Number -> string with d decimals ('--' for missing)."""
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "--"
    return f"{x:.{d}f}"


def fmt_ci(lo, hi, d: int = 2) -> str:
    return f"[{fmt(lo, d)}; {fmt(hi, d)}]"


def latex_escape(s) -> str:
    """Escape & % # _ for LaTeX -- but not inside $...$ and not if already escaped."""
    parts = re.split(r"(\$[^$]*\$)", str(s))
    out = []
    for p in parts:
        if len(p) > 1 and p.startswith("$") and p.endswith("$"):
            out.append(p)  # LaTeX math stays as it is
        else:
            out.append(re.sub(r"(?<!\\)([&%#_])", r"\\\1", p))
    return "".join(out)


def to_latex_table(df: pd.DataFrame, path: Path, caption: str, label: str,
                   col_format: str | None = None, notes: str | None = None,
                   index: bool = False, size: str = r"\small") -> None:
    """Write a data frame (already formatted as strings) as a booktabs table.

    In Overleaf:  \\usepackage{booktabs}  in the preamble, then  \\input{tables/<file>.tex}.
    Column headers are written as they are (LaTeX allowed), cells are escaped.
    """
    d = df.reset_index() if index else df
    if col_format is None:
        col_format = "l" + "r" * (d.shape[1] - 1)
    lines = [r"\begin{table}[htbp]", r"\centering", size,
             rf"\caption{{{caption}}}", rf"\label{{{label}}}",
             rf"\begin{{tabular}}{{{col_format}}}", r"\toprule",
             " & ".join(str(c) for c in d.columns) + r" \\", r"\midrule"]
    for _, row in d.iterrows():
        cells = [latex_escape(x) for x in row.tolist()]
        if cells and cells[0].startswith(r"\midrule"):
            lines.append(r"\midrule")
            continue
        lines.append(" & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    if notes:
        lines.append(rf"\par\smallskip\parbox{{0.95\linewidth}}{{\footnotesize {notes}}}")
    lines.append(r"\end{table}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_macros(values: dict, path: Path, comment: str = "") -> None:
    """Write LaTeX macros so numbers in the report come straight from the code.

    Overleaf:  \\input{tables/macros_replication.tex}   then in the text e.g.  \\maREor
    Macro names: letters only, prefix 'ma' to avoid clashes with LaTeX commands.
    """
    lines = [f"% generated by {comment} -- do not edit by hand"] if comment else []
    for name, val in values.items():
        if not re.fullmatch(r"ma[A-Za-z]+", name):
            raise ValueError(f"invalid macro name {name!r} (letters only, prefix 'ma')")
        lines.append(rf"\newcommand{{\{name}}}{{{val}}}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_fig(fig, name: str) -> None:
    """Save a figure as PDF (for Overleaf) and PNG (for slides)."""
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
NEW_COLOR = "#c0392b"   # new studies (update)
BASE_COLOR = "#222222"


def _or_ticks(ax, lo, hi):
    ticks = [t for t in (0.05, 0.1, 0.25, 0.5, 1, 2, 4, 8) if lo <= t <= hi]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:g}" for t in ticks])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())


def forest_plot(df: pd.DataFrame, pooled: list, name: str, title: str | None = None,
                weights_tau2: float = 0.0) -> None:
    """Forest plot on the OR scale (log axis).

    df     : columns 'label', 'log_or', 'se' and optionally 'new' (bool, highlighted)
    pooled : list of MetaResult, drawn as diamonds at the bottom
    """
    d = df.reset_index(drop=True)
    n, m = len(d), len(pooled)
    lo = np.exp(d["log_or"] - Z975 * d["se"])
    hi = np.exp(d["log_or"] + Z975 * d["se"])
    est = np.exp(d["log_or"])
    w = 1 / (d["se"] ** 2 + weights_tau2)
    size = 3 + 7 * np.sqrt(w / w.max())
    new = d["new"].astype(bool) if "new" in d else pd.Series(False, index=d.index)

    ypos = np.arange(n)[::-1] + m + 1.0  # studies on top, pooled rows below
    fig, ax = plt.subplots(figsize=(8, 0.24 * (n + m + 2) + 0.8))
    for i in range(n):
        col = NEW_COLOR if new[i] else BASE_COLOR
        ax.plot([lo[i], hi[i]], [ypos[i]] * 2, color=col, lw=0.9)
        ax.plot(est[i], ypos[i], "s", color=col, ms=size[i])
    labels = list(d["label"])
    for j, r in enumerate(pooled):
        yj = m - j - 0.3
        e, l_, u_ = np.exp(r.est), np.exp(r.ci_low), np.exp(r.ci_upp)
        ax.fill([l_, e, u_, e], [yj, yj + 0.3, yj, yj - 0.3], color="#2c3e50")
    xmin = max(0.03, float(min(lo.min(), *[np.exp(r.ci_low) for r in pooled])) * 0.8)
    xmax = min(12.0, float(max(hi.max(), *[np.exp(r.ci_upp) for r in pooled])) * 1.25)
    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    _or_ticks(ax, xmin, xmax)
    ax.axvline(1, color="grey", ls=":", lw=1)
    ax.set_yticks(list(ypos) + [m - j - 0.3 for j in range(m)])
    ax.set_yticklabels(labels + [r.method for r in pooled], fontsize=8)
    for tl, is_new in zip(ax.get_yticklabels()[:n], new):
        if is_new:
            tl.set_color(NEW_COLOR)
    trans = transforms.blended_transform_factory(ax.transAxes, ax.transData)
    for i in range(n):
        ax.text(1.02, ypos[i], f"{est[i]:.2f} [{lo[i]:.2f}, {hi[i]:.2f}]", transform=trans,
                va="center", fontsize=8, color=NEW_COLOR if new[i] else BASE_COLOR)
    for j, r in enumerate(pooled):
        ax.text(1.02, m - j - 0.3, f"{np.exp(r.est):.2f} [{np.exp(r.ci_low):.2f}, {np.exp(r.ci_upp):.2f}]",
                transform=trans, va="center", fontsize=8, fontweight="bold")
    ax.axhline(m + 0.4, color="black", lw=0.6)
    ax.set_ylim(-0.6, ypos.max() + 0.8)
    ax.set_xlabel("Odds ratio of a call-back, minority vs. majority (log scale)")
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    if title:
        ax.set_title(title, fontsize=10, loc="left")
    save_fig(fig, name)


def funnel_plot(df: pd.DataFrame, center: float, name: str, pet: float | None = None,
                title: str | None = None, precision: bool = False) -> None:
    """Funnel plot.

    precision=False : x = OR (log axis), y = SE (inverted, 0 on top) with the
                      pseudo 95 % region center +/- 1.96 SE (straight lines).
    precision=True  : x = OR (log axis), y = precision 1/SE (Stanley & Doucouliagos).
    center : pooled ln OR (FE = UWLS) around which the funnel is drawn
    pet    : optional PET estimate (ln OR), drawn as dotted line
    """
    d = df.reset_index(drop=True)
    new = d["new"].astype(bool) if "new" in d else pd.Series(False, index=d.index)
    se = d["se"].to_numpy(float)
    x = np.exp(d["log_or"].to_numpy(float))
    se_grid = np.linspace(1e-4, se.max() * 1.05, 200)
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    yv = 1 / se if precision else se
    ygrid = 1 / se_grid if precision else se_grid
    ax.fill_betweenx(ygrid, np.exp(center - Z975 * se_grid), np.exp(center + Z975 * se_grid),
                     color="#ecf0f1", zorder=0, label="pseudo 95% region")
    ax.plot(np.exp(center - Z975 * se_grid), ygrid, color="grey", lw=0.8)
    ax.plot(np.exp(center + Z975 * se_grid), ygrid, color="grey", lw=0.8)
    ax.scatter(x[~new], yv[~new], s=22, color=BASE_COLOR, zorder=3, label="Zschirnt & Ruedin (2016)")
    if new.any():
        ax.scatter(x[new], yv[new], s=34, color=NEW_COLOR, marker="D", zorder=4, label="new studies")
    ax.axvline(np.exp(center), color="black", lw=1, label=f"FE / UWLS: OR = {np.exp(center):.2f}")
    ax.axvline(1, color="grey", ls=":", lw=1, label="no discrimination (OR = 1)")
    if pet is not None:
        ax.axvline(np.exp(pet), color="#2980b9", ls="--", lw=1, label=f"PET: OR = {np.exp(pet):.2f}")
    xmin = max(0.03, min(x.min(), np.exp(center - Z975 * se.max())) * 0.85)
    xmax = min(12.0, max(x.max(), np.exp(center + Z975 * se.max()), 1.0) * 1.2)
    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    _or_ticks(ax, xmin, xmax)
    if precision:
        ax.set_ylim(0, (1 / se).max() * 1.08)
        ax.set_ylabel("Precision (1 / SE)")
    else:
        ax.set_ylim(se.max() * 1.05, 0)
        ax.set_ylabel("Standard error of ln OR")
    ax.set_xlabel("Odds ratio of a call-back, minority vs. majority (log scale)")
    ax.legend(fontsize=7.5, frameon=False, loc="lower right" if not precision else "upper right")
    for s in ("right", "top"):
        ax.spines[s].set_visible(False)
    if title:
        ax.set_title(title, fontsize=10, loc="left")
    save_fig(fig, name)


def power_plot(df: pd.DataFrame, mu: float, name: str, title: str | None = None) -> None:
    """Ex-post power of each study vs. its estimate (like Askarov et al., Fig. 3)."""
    d = df.reset_index(drop=True)
    q = power(d["se"], mu)
    new = d["new"].astype(bool) if "new" in d else pd.Series(False, index=d.index)
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ok = q >= 0.8
    ax.scatter(np.exp(d["log_or"])[ok & ~new], q[ok & ~new], color=BASE_COLOR, s=22, label="power >= 80%")
    ax.scatter(np.exp(d["log_or"])[~ok & ~new], q[~ok & ~new], facecolors="none", edgecolors=BASE_COLOR,
               s=22, label="power < 80%")
    if new.any():
        ax.scatter(np.exp(d["log_or"])[new], q[new], color=NEW_COLOR, marker="D", s=30, label="new studies")
    ax.axhline(0.8, color="grey", ls=":", lw=1)
    ax.axvline(np.exp(mu), color="black", lw=1, label=f"UWLS: OR = {np.exp(mu):.2f}")
    ax.set_xscale("log")
    lo, hi = np.exp(d["log_or"]).min() * 0.85, max(np.exp(d["log_or"]).max(), 1) * 1.2
    ax.set_xlim(lo, hi)
    _or_ticks(ax, lo, hi)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("Odds ratio (log scale)")
    ax.set_ylabel("Ex-post power at the UWLS estimate")
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    for s in ("right", "top"):
        ax.spines[s].set_visible(False)
    if title:
        ax.set_title(title, fontsize=10, loc="left")
    save_fig(fig, name)
