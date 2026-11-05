"""
02_replication.py -- Schritt 2 im PLAN.md (Aufgabe 2 des Prof)

Replicates the pooled estimate of Zschirnt & Ruedin (2016) and compares
FE, UWLS and random effects (DL, PM, REML, REML + Knapp-Hartung).

Original (meta-replication.pdf / supplement S6), random effects with REML:
    study level (k = 34):     ln OR = -0.5086 (SE 0.0701), tau2 = 0.1406, I2 = 92.73 %
                              -> OR = 0.60 [0.52; 0.69]
    without Bendick (k = 33): ln OR = -0.5404 (SE 0.0549), tau2 = 0.0764
    subgroup level (k = 215): ln OR = -0.6041 (SE 0.0283), tau2 = 0.0934

Outputs
    04_report/tables/replication.tex / .csv
    04_report/tables/macros_replication.tex
    04_report/figures/forest_original.pdf / .png

Run from the repository root:  python 02_code/02_replication.py
"""

import numpy as np
import pandas as pd

import utils_meta as um

TARGETS = {
    "study":      dict(k=34, est=-0.5086, se=0.0701, tau2=0.1406, Q=327.6821, I2=92.73),
    "no_bendick": dict(k=33, est=-0.5404, se=0.0549, tau2=0.0764, Q=231.2032),
    "subgroup":   dict(k=215, est=-0.6041, se=0.0283, tau2=0.0934, Q=647.3077),
}
TOL = dict(k=0, est=6e-4, se=6e-4, tau2=6e-4, Q=0.01, I2=0.01)


def check(name: str, res: um.MetaResult) -> bool:
    """Compare our result with the numbers printed in the original replication file."""
    ok = True
    msgs = []
    for key, target in TARGETS[name].items():
        ours = getattr(res, key)
        good = abs(ours - target) <= TOL[key]
        ok &= good
        msgs.append(f"{key}={ours:.4f} (orig. {target}) {'OK' if good else 'DIFFERENT'}")
    print(f"  check {name:<10}: " + ", ".join(msgs))
    return ok


def main() -> None:
    um.ensure_dirs()
    df = um.load_sample("original")
    y, se = df["log_or"].to_numpy(), df["se"].to_numpy()

    # ---- the methods (study level, k = 34) ----------------------------------
    fe = um.fixed_effect(y, se)
    uw = um.uwls(y, se)
    re_dl = um.random_effects(y, se, "DL")
    re_pm = um.random_effects(y, se, "PM")
    re_reml = um.random_effects(y, se, "REML")
    re_kh = um.random_effects(y, se, "REML", knha=True)
    main_rows = [fe, uw, re_dl, re_pm, re_reml, re_kh]

    # ---- robustness ---------------------------------------------------------
    nb = um.load_sample("original_no_bendick")
    re_nb = um.random_effects(nb["log_or"], nb["se"], "REML",
                              label="RE (REML) without Bendick et al. (1991)")
    sub = pd.read_csv(um.SUBGROUPS_CSV)
    re_sub = um.random_effects(sub["log_or"], sub["se"], "REML", label="RE (REML), subgroup level")
    robust_rows = [re_nb, re_sub]

    print("Replication of Zschirnt & Ruedin (2016)\n")
    for r in main_rows + robust_rows:
        print("  " + str(r))
    print()
    all_ok = check("study", re_reml) & check("no_bendick", re_nb) & check("subgroup", re_sub)
    print("  -> replication " + ("successful: all numbers match the original" if all_ok
                                 else "NOT exact, see above"))

    # ---- FE vs. UWLS (Aufgabe 2) ------------------------------------------
    width_fe = fe.ci_upp - fe.ci_low
    width_uw = uw.ci_upp - uw.ci_low
    print("\nFE vs. UWLS:")
    print(f"  same point estimate: FE = {fe.est:.6f}, UWLS = {uw.est:.6f}")
    print(f"  SE: FE = {fe.se:.4f}, UWLS = {uw.se:.4f}  (ratio = {uw.se / fe.se:.2f} "
          f"= sqrt(Q/(k-1)) = sqrt({fe.Q:.1f}/{fe.k - 1}))")
    print(f"  95% CI width: FE = {width_fe:.3f}, UWLS = {width_uw:.3f} -> UWLS is "
          f"{width_uw / width_fe:.1f} times wider, because Q/(k-1) = {fe.Q / (fe.k - 1):.1f} > 1 "
          f"(much heterogeneity)")
    print(f"\nRE (REML) 95% prediction interval: OR {um.fmt_ci(np.exp(re_reml.pi_low), np.exp(re_reml.pi_upp))}")

    # ---- table --------------------------------------------------------------
    rows = []
    for r in main_rows + [None] + robust_rows:
        if r is None:
            rows.append([r"\midrule"] + [""] * 7)
            continue
        rows.append([r.method, r.k, um.fmt(r.est), um.fmt(r.se), um.fmt(np.exp(r.est), 2),
                     um.fmt_ci(np.exp(r.ci_low), np.exp(r.ci_upp)),
                     um.fmt(r.tau2) if np.isfinite(r.tau2) else "--",
                     um.fmt(r.I2, 1) if np.isfinite(r.I2) else "--"])
    cols = ["Method", "$k$", r"$\ln OR$", "SE", "OR", "95\\% CI (OR)", r"$\hat\tau^2$", r"$I^2$ (\%)"]
    tab = pd.DataFrame(rows, columns=cols)
    um.to_latex_table(
        tab, um.TAB / "replication.tex",
        caption="Replication of the pooled effect (study level, $k = 34$)",
        label="tab:replication", col_format="lrrrrrrr",
        notes=("Effect size: log odds ratio of a call-back, minority vs.\\ majority applicants; "
               "OR $<1$ means discrimination. FE, random effects (RE) and the $I^2$ of RE as in "
               "metafor; UWLS: OLS of $y_i/SE_i$ on $1/SE_i$ without constant, CI with $t_{k-1}$. "
               "UWLS and FE have the same estimate. For FE and UWLS, $I^2$ is $(Q-(k-1))/Q$. "
               "Original (Zschirnt \\& Ruedin 2016, RE with REML): $\\ln OR = -0.509$, OR $= 0.60$ "
               "[0.52; 0.69], $\\hat\\tau^2 = 0.141$, $I^2 = 92.7\\%$."),
    )
    pd.DataFrame([r.as_dict() for r in main_rows + robust_rows]).to_csv(
        um.TAB / "replication.csv", index=False)

    # ---- macros for the text -------------------------------------------------
    e = np.exp
    um.write_macros({
        "maK": str(re_reml.k),
        "maKsub": str(re_sub.k),
        "maORfe": um.fmt(e(fe.est), 2), "maCIfe": um.fmt_ci(e(fe.ci_low), e(fe.ci_upp)),
        "maORuwls": um.fmt(e(uw.est), 2), "maCIuwls": um.fmt_ci(e(uw.ci_low), e(uw.ci_upp)),
        "maORre": um.fmt(e(re_reml.est), 2), "maCIre": um.fmt_ci(e(re_reml.ci_low), e(re_reml.ci_upp)),
        "maLnORre": um.fmt(re_reml.est), "maSEre": um.fmt(re_reml.se),
        "maPIre": um.fmt_ci(e(re_reml.pi_low), e(re_reml.pi_upp)),
        "maTauSqRe": um.fmt(re_reml.tau2), "maIsqRe": um.fmt(re_reml.I2, 1),
        "maQ": um.fmt(fe.Q, 1), "maIsqQ": um.fmt(fe.I2, 1),
        "maORreKH": um.fmt(e(re_kh.est), 2), "maCIreKH": um.fmt_ci(e(re_kh.ci_low), e(re_kh.ci_upp)),
        "maORreDL": um.fmt(e(re_dl.est), 2), "maORrePM": um.fmt(e(re_pm.est), 2),
        "maORreNoBendick": um.fmt(e(re_nb.est), 2),
        "maCIreNoBendick": um.fmt_ci(e(re_nb.ci_low), e(re_nb.ci_upp)),
        "maORsub": um.fmt(e(re_sub.est), 2), "maCIsub": um.fmt_ci(e(re_sub.ci_low), e(re_sub.ci_upp)),
        "maSEratioUWLS": um.fmt(uw.se / fe.se, 2),
        "maPctLowerOdds": f"{100 * (1 - e(re_reml.est)):.0f}",
    }, um.TAB / "macros_replication.tex", comment="02_code/02_replication.py")

    # ---- forest plot --------------------------------------------------------
    um.forest_plot(df, [re_reml, fe, uw], "forest_original",
                   title="Zschirnt & Ruedin (2016): call-back odds ratios, study level",
                   weights_tau2=re_reml.tau2)

    print("\nsaved 04_report/tables/replication.tex/.csv, macros_replication.tex")
    print("saved 04_report/figures/forest_original.pdf/.png")


if __name__ == "__main__":
    main()
