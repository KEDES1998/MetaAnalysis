"""
05_meta_regression.py -- Schritt 7 im PLAN.md

1. Check: replicate model RG1 of the original replication file (study level,
   ln OR ~ skills, random effects with REML + Knapp-Hartung, k = 30):
       intercept -0.6080 (0.1571), high skills 0.1578 (0.2241),
       low skills 0.0665 (0.1990), tau2 = 0.1696
2. WLS meta-regressions (as asked in instruction.pdf: "a weighted-least squares
   meta regression addressing both publication bias and heterogeneity"):

       y_i = b0 + b1 * SE_i + moderators + e_i,   weights 1 / SE_i^2

   M1  SE only (= FAT-PET)
   M2  + Europe, German-speaking country
   M3  + skill level of the jobs (high, low; reference: mixed)
   M4  + testing year (in decades, 0 = 2000)
   M5  + dummy for the new studies (only after the update)
3. The same models as random-effects meta-regressions (REML + Knapp-Hartung),
   like the original supplement S13, as robustness check.

Sample: original + new studies if 03_update.py has produced them, else original.
Few studies (about 35) -> only few moderators, interpret with care.

Outputs
    04_report/tables/metareg_wls.tex/.csv, metareg_re.tex/.csv

Run from the repository root:  python 02_code/05_meta_regression.py
"""

import numpy as np
import pandas as pd

import utils_meta as um

RG1_TARGET = {"Intercept": (-0.6080, 0.1571), "skill_high": (0.1578, 0.2241),
              "skill_low": (0.0665, 0.1990)}
RG1_TAU2 = 0.1696

NICE = {
    "Intercept": "Intercept (PET)", "SE": "SE (FAT)", "europe": "Europe",
    "german_speaking": "German-speaking country", "skill_high": "High-skilled jobs",
    "skill_low": "Low-skilled jobs", "decade": "Testing year (decades, 0 = 2000)",
    "new": "New study (update)",
}


def replicate_rg1(orig: pd.DataFrame) -> None:
    y, se, X, names, _ = um.design_matrix(orig, ["skill_high", "skill_low"], add_se=False)
    reg = um.re_meta_regression(y, se, X, names, "REML", knha=True, label="RG1 replication")
    t = reg.table()
    ok = abs(reg.tau2 - RG1_TAU2) < 6e-4 and reg.k == 30
    for name, (b, s) in RG1_TARGET.items():
        ok &= abs(t.loc[name, "coef"] - b) < 6e-4 and abs(t.loc[name, "se"] - s) < 6e-4
    print(reg)
    print("  -> check against original model RG1 (k = 30): " + ("OK" if ok else "DIFFERENT"), "\n")


def stars(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def regression_table(models: list, path_stem: str, caption: str, label: str, notes: str) -> None:
    """Coefficients (SE in brackets below) for several models side by side."""
    order = [v for v in NICE if any(v in m.names for m in models)]
    rows = []
    for v in order:
        coef_row, se_row = [NICE[v]], [""]
        for m in models:
            if v in m.names:
                t = m.table().loc[v]
                coef_row.append(f"{t['coef']:.3f}{stars(t['p'])}")
                se_row.append(f"({t['se']:.3f})")
            else:
                coef_row += [""]
                se_row += [""]
        rows += [coef_row, se_row]
    rows.append([r"\midrule"] + [""] * len(models))
    rows.append(["$k$"] + [str(m.k) for m in models])
    if np.isfinite(models[0].sigma):
        rows.append(["Residual SE"] + [f"{m.sigma:.2f}" for m in models])
    else:
        rows.append([r"$\hat\tau^2$ (residual)"] + [f"{m.tau2:.3f}" for m in models])
    cols = [""] + [f"M{i + 1}" for i in range(len(models))]
    um.to_latex_table(pd.DataFrame(rows, columns=cols), um.TAB / f"{path_stem}.tex", caption=caption,
                      label=label, col_format="l" + "r" * len(models), notes=notes)
    pd.concat({f"M{i + 1}": m.table() for i, m in enumerate(models)}).to_csv(um.TAB / f"{path_stem}.csv")


def main() -> None:
    um.ensure_dirs()
    orig = um.load_sample("original")
    replicate_rg1(orig)

    comb = um.load_sample("combined")
    df = comb if comb is not None else orig
    sample = "original + new studies" if comb is not None else "original studies"
    df = df.copy()
    df["decade"] = (df["testing_year"] - 2000) / 10

    specs = [[], ["europe", "german_speaking"], ["europe", "german_speaking", "skill_high", "skill_low"],
             ["europe", "german_speaking", "decade"]]
    if comb is not None:
        specs.append(["europe", "german_speaking", "new"])

    wls_models, re_models = [], []
    for i, mods in enumerate(specs):
        y, se, X, names, _ = um.design_matrix(df, mods, add_se=True)
        wls_models.append(um.wls_meta_regression(y, se, X, names, label=f"M{i + 1} (WLS)"))
        re_models.append(um.re_meta_regression(y, se, X, names, "REML", knha=True, label=f"M{i + 1} (RE)"))

    print(f"WLS meta-regressions, {sample}:\n")
    for m in wls_models:
        print(m, "\n")

    note_common = ("Dependent variable: $\\ln OR$ of a call-back (minority vs.\\ majority); negative = "
                   "discrimination. The intercept is the effect for a study with $SE\\to 0$ in the "
                   "reference group (outside Europe; mixed skills; testing year 2000). "
                   "* $p<0.1$, ** $p<0.05$, *** $p<0.01$.")
    regression_table(wls_models, "metareg_wls",
                     caption=f"WLS meta-regression: publication bias and heterogeneity ({sample})",
                     label="tab:metareg-wls",
                     notes=("WLS with weights $1/SE_i^2$ and multiplicative error (as UWLS), $t$-based "
                            "standard errors. " + note_common))
    regression_table(re_models, "metareg_re",
                     caption=f"Random-effects meta-regression, REML with Knapp-Hartung ({sample})",
                     label="tab:metareg-re",
                     notes=("Mixed-effects model as in the original supplement (S13), "
                            "weights $1/(SE_i^2+\\hat\\tau^2)$. " + note_common))
    print("saved 04_report/tables/metareg_wls.tex/.csv, metareg_re.tex/.csv")


if __name__ == "__main__":
    main()
