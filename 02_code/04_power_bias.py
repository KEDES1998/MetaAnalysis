"""
04_power_bias.py -- Schritte 5 und 6 im PLAN.md (Aufgaben 4 und 5 des Prof)

For every available sample (original, original without Bendick, original + new):

Power (Aufgabe 4)
    q_i = Phi(|mu| / SE_i - 1.96) with mu = UWLS estimate ("true" effect)
    -> median / mean power, number of adequately powered studies (q_i >= 0.8)

Publication bias (Aufgabe 5)
    funnel plot, WAAP, ESS, FAT-PET (meta-regression of the effect on its SE),
    PEESE as an extra

Outputs
    04_report/tables/pubbias_estimates.tex/.csv   pooled ORs: FE, UWLS, RE, WAAP, PET, PEESE
    04_report/tables/power_bias_stats.tex/.csv    power, FAT, ESS
    04_report/tables/power_by_study.csv           power of every study
    04_report/tables/power_robustness.tex/.csv    why power falls in the combined sample (appendix)
    04_report/tables/macros_power_bias.tex
    04_report/figures/funnel_<sample>.pdf/.png, funnel_precision_<sample>, power_<sample>

Run from the repository root:  python 02_code/04_power_bias.py
"""

import numpy as np
import pandas as pd

import utils_meta as um

FIGURE_SAMPLES = ("original", "combined")   # no extra plots for the robustness sample
MACRO_SUFFIX = {"original": "", "original_no_bendick": "NoBendick", "combined": "Comb"}
DOMINANT_STUDY = "Kline"   # new study with by far the largest weight, see power_robustness()


def analyse(df: pd.DataFrame) -> dict:
    y, se = df["log_or"].to_numpy(), df["se"].to_numpy()
    fe = um.fixed_effect(y, se)
    uw = um.uwls(y, se)
    re = um.random_effects(y, se, "REML")
    q = um.power(se, uw.est)
    wa, mask = um.waap(y, se, uw.est)
    fp = um.fat_pet(y, se)
    pe = um.peese(y, se)
    return {
        "k": len(y), "fe": fe, "uwls": uw, "re": re, "waap": wa, "n_adequate": int(mask.sum()),
        "power": q, "median_power": float(np.median(q)), "mean_power": float(np.mean(q)),
        "median_power_re": float(np.median(um.power(se, re.est))),
        "fatpet": fp, "peese": pe,
        "pet": um.reg_to_meta(fp, "PET (b0)", "PET"),
        "peese_est": um.reg_to_meta(pe, "PEESE (b0)", "PEESE"),
        "ess": um.ess(y, se, uw.est, tau2=0.0),
        "ess_tau": um.ess(y, se, uw.est, tau2=re.tau2),
    }


def or_ci(r: um.MetaResult | None) -> str:
    if r is None:
        return "n.a."
    return f"{np.exp(r.est):.2f} {um.fmt_ci(np.exp(r.ci_low), np.exp(r.ci_upp))}"


def power_robustness(samples: dict, res: dict) -> dict:
    """Why power falls in the combined sample -- robustness table for the appendix.

    Power depends on the assumed true effect (the UWLS estimate). In the combined sample one
    very large study (DOMINANT_STUDY) gets a large share of the UWLS weight 1/SE^2 and pulls
    the UWLS estimate towards one, which lowers the power of every study. The table compares
    (a) original, (b) original + new, (c) original + new without that study and
    (d) original + new with power evaluated at the RE estimate (weights 1/(SE^2 + tau^2),
    much more equal across studies). Returns macros for the text ({} if no combined sample).
    """
    if "combined" not in samples:
        return {}
    comb = samples["combined"]
    is_dom = comb["authors"].str.startswith(DOMINANT_STUDY).to_numpy()
    if is_dom.sum() != 1:
        print(f"note: '{DOMINANT_STUDY}' not found exactly once in the combined sample -- "
              "no power robustness table")
        return {}
    se = comb["se"].to_numpy()
    r_o, r_c = res["original"], res["combined"]
    w_fe = 1 / se**2
    w_re = 1 / (se**2 + r_c["re"].tau2)
    if w_fe.argmax() != is_dom.argmax():
        print(f"note: {DOMINANT_STUDY} no longer has the largest weight -- check DOMINANT_STUDY")
    dom = comb[is_dom].iloc[0]
    dom_label = f"{dom['authors']} ({int(dom['year'])})"
    no_dom = comb[~is_dom].reset_index(drop=True)
    r_n = analyse(no_dom)
    q_re = um.power(se, r_c["re"].est)

    def row(sample, k, est, method, q):
        return [sample, str(k), f"{np.exp(est):.2f} ({method})", f"{np.mean(q):.2f}",
                f"{np.median(q):.2f}", f"{int((q >= 0.8).sum())} of {k}"]

    rows = [row("Original", r_o["k"], r_o["uwls"].est, "UWLS", r_o["power"]),
            row("Original + new", r_c["k"], r_c["uwls"].est, "UWLS", r_c["power"]),
            row(f"Original + new, without {dom_label}", r_n["k"], r_n["uwls"].est, "UWLS", r_n["power"]),
            row("Original + new", r_c["k"], r_c["re"].est, "RE", q_re)]
    tab = pd.DataFrame(rows, columns=["Sample", "$k$", "Assumed effect (OR)", "Mean power",
                                      "Median power", "$q_i \\geq 0.8$"])
    share = lambda w, m: 100 * w[m].sum() / w.sum()
    orig_mask = (comb["in_original"] == 1).to_numpy()
    um.to_latex_table(
        tab, um.TAB / "power_robustness.tex",
        caption="Robustness of statistical power in the combined sample", label="tab:power-robust",
        col_format=r">{\raggedright\arraybackslash}p{4.2cm}rrrrr",
        notes=(f"Power of each study at the assumed true effect: "
               f"$q_i = \\Phi(|\\hat\\mu|/SE_i - 1.96)$; last column: number of adequately powered studies ($q_i \\geq 0.8$). "
               f"In the combined sample, {um.latex_escape(dom_label)} receives "
               f"{share(w_fe, is_dom):.0f}\\% of the UWLS weight $1/SE_i^2$ (all {r_o['k']} original "
               f"studies together: {share(w_fe, orig_mask):.0f}\\%) but only {share(w_re, is_dom):.0f}\\% "
               f"of the RE weight $1/(SE_i^2+\\hat\\tau^2)$."))
    tab.rename(columns={"$k$": "k", "$q_i \\geq 0.8$": "adequately_powered"}).to_csv(
        um.TAB / "power_robustness.csv", index=False)
    print(f"\n=== Power robustness (dominant study: {dom_label}) ===\n{tab.to_string(index=False)}")
    print("saved 04_report/tables/power_robustness.tex/.csv")

    n_dom = int(dom["n_minority"] + dom["n_majority"])
    return {
        "maORuwlsComb": um.fmt(np.exp(r_c["uwls"].est), 2),
        "maORkline": um.fmt(np.exp(dom["log_or"]), 2),
        "maNkline": f"{n_dom:,}".replace(",", "'"),
        "maWshareKline": f"{share(w_fe, is_dom):.0f}",
        "maWshareKlineRE": f"{share(w_re, is_dom):.0f}",
        "maWshareOrig": f"{share(w_fe, orig_mask):.0f}",
        "maKnoKline": str(r_n["k"]),
        "maORuwlsNoKline": um.fmt(np.exp(r_n["uwls"].est), 2),
        "maMeanPowerNoKline": f"{r_n['mean_power']:.2f}",
        "maMedPowerNoKline": f"{r_n['median_power']:.2f}",
        "maNadequateNoKline": str(r_n["n_adequate"]),
        "maMeanPowerCombRE": f"{np.mean(q_re):.2f}",
        "maMedPowerCombRE": f"{np.median(q_re):.2f}",
        "maNadequateCombRE": str(int((q_re >= 0.8).sum())),
    }


def main() -> None:
    um.ensure_dirs()
    samples = um.available_samples()
    res = {name: analyse(df) for name, df in samples.items()}

    # ---- console summary -------------------------------------------------
    for name, r in res.items():
        fat = r["fatpet"].table()
        print(f"\n=== {um.SAMPLE_LABELS[name]} (k = {r['k']}) ===")
        print(f"  UWLS OR {or_ci(r['uwls'])},  RE OR {or_ci(r['re'])}")
        print(f"  power at UWLS: median {r['median_power']:.3f}, mean {r['mean_power']:.3f}, "
              f"adequately powered: {r['n_adequate']} of {r['k']}")
        print(f"  WAAP  OR {or_ci(r['waap'])}")
        print(f"  FAT   b1 = {fat.loc['FAT (b1)', 'coef']:.3f} (SE {fat.loc['FAT (b1)', 'se']:.3f}, "
              f"t = {fat.loc['FAT (b1)', 'stat']:.2f})")
        print(f"  PET   OR {or_ci(r['pet'])},  PEESE OR {or_ci(r['peese_est'])}")
        e, et = r["ess"], r["ess_tau"]
        print(f"  significant: {e['n_sig']} of {e['n']} ({e['share_sig']:.2f}); expected "
              f"{e['expected_share']:.2f} -> ESS = {e['ESS']:+.2f}; with tau2: expected "
              f"{et['expected_share']:.2f} -> ESS = {et['ESS']:+.2f}")

    names = list(res)
    head = [um.SAMPLE_LABELS[n] for n in names]

    # ---- table 1: pooled estimates ---------------------------------------
    est_rows = [("Fixed effect (FE)", "fe"), ("UWLS", "uwls"), ("Random effects (REML)", "re"),
                ("WAAP", "waap"), ("PET", "pet"), ("PEESE", "peese_est")]
    t1 = pd.DataFrame([[lab] + [or_ci(res[n][key]) for n in names] for lab, key in est_rows]
                      + [["Adequately powered studies"] + [f"{res[n]['n_adequate']} of {res[n]['k']}"
                                                           for n in names]],
                      columns=["Estimator"] + head)
    um.to_latex_table(
        t1, um.TAB / "pubbias_estimates.tex",
        caption="Pooled odds ratios with and without correction for publication bias",
        label="tab:pubbias-estimates", col_format="l" + "r" * len(names),
        notes=("OR [95\\% CI]. WAAP: UWLS over the studies with power $\\geq 80\\%$ at the UWLS "
               "estimate ($SE_i \\leq |\\hat\\mu_{UWLS}|/2.8$). PET: intercept of the WLS regression "
               "$y_i = \\beta_0 + \\beta_1 SE_i + \\varepsilon_i$ (weights $1/SE_i^2$), i.e.\\ the effect "
               "of a study with $SE \\to 0$. PEESE: the same with $SE_i^2$."))
    pd.DataFrame([{"sample": n, "estimator": lab, **(res[n][key].as_dict() if res[n][key] else {})}
                  for n in names for lab, key in est_rows]).to_csv(um.TAB / "pubbias_estimates.csv",
                                                                   index=False)

    # ---- table 2: power, FAT, ESS -----------------------------------------
    def col(n):
        r = res[n]
        fat = r["fatpet"].table().loc["FAT (b1)"]
        e, et = r["ess"], r["ess_tau"]
        return [str(r["k"]), f"{r['median_power']:.2f}", f"{r['mean_power']:.2f}",
                f"{r['n_adequate']} ({100 * r['n_adequate'] / r['k']:.0f}\\%)",
                f"{fat['coef']:.2f} ({fat['se']:.2f})", f"{fat['stat']:.2f}",
                f"{e['n_sig']} ({e['share_sig']:.2f})", f"{e['expected_share']:.2f}", f"{e['ESS']:+.2f}",
                f"{et['expected_share']:.2f}", f"{et['ESS']:+.2f}"]
    labels = ["$k$", "Median power", "Mean power", "Adequately powered ($q_i \\geq 0.8$)",
              "FAT: $\\hat\\beta_1$ (SE)", "FAT: $t$", "Significant estimates (share)",
              "Expected share significant", "ESS = observed $-$ expected",
              "Expected share significant (with $\\hat\\tau^2$)", "ESS (with $\\hat\\tau^2$)"]
    t2 = pd.DataFrame({"": labels, **{h: col(n) for h, n in zip(head, names)}})
    um.to_latex_table(
        t2, um.TAB / "power_bias_stats.tex", caption="Statistical power and publication bias",
        label="tab:power-bias", col_format="l" + "r" * len(names),
        notes=("Power of each study at the UWLS estimate: $q_i = \\Phi(|\\hat\\mu|/SE_i - 1.96)$. "
               "FAT: slope of the WLS regression of $\\ln OR$ on its SE; with discrimination "
               "($\\ln OR<0$) selection for significance implies $\\beta_1<0$. ESS: observed minus "
               "expected share of significant estimates ($|y_i/SE_i|>1.96$); the expected share uses "
               "the UWLS estimate as true effect, in the last two rows the true effects vary with "
               "$\\hat\\tau^2$ (REML)."))
    t2.to_csv(um.TAB / "power_bias_stats.csv", index=False)

    # ---- power per study ----------------------------------------------------
    pw = []
    for n, df in samples.items():
        d = df[["study_id", "label", "log_or", "se"]].copy()
        d["sample"] = n
        d["power_uwls"] = res[n]["power"]
        d["adequately_powered"] = d["power_uwls"] >= 0.8
        pw.append(d)
    pd.concat(pw).to_csv(um.TAB / "power_by_study.csv", index=False)

    # ---- macros --------------------------------------------------------------
    macros = {}
    for n in names:
        s, r = MACRO_SUFFIX[n], res[n]
        fat = r["fatpet"].table().loc["FAT (b1)"]
        macros.update({
            f"maMedPower{s}": f"{r['median_power']:.2f}", f"maMeanPower{s}": f"{r['mean_power']:.2f}",
            f"maNadequate{s}": str(r["n_adequate"]),
            f"maORwaap{s}": um.fmt(np.exp(r["waap"].est), 2) if r["waap"] else "n.a.",
            f"maCIwaap{s}": um.fmt_ci(np.exp(r["waap"].ci_low), np.exp(r["waap"].ci_upp)) if r["waap"] else "n.a.",
            f"maORpet{s}": um.fmt(np.exp(r["pet"].est), 2),
            f"maCIpet{s}": um.fmt_ci(np.exp(r["pet"].ci_low), np.exp(r["pet"].ci_upp)),
            f"maORpeese{s}": um.fmt(np.exp(r["peese_est"].est), 2),
            f"maFAT{s}": f"{fat['coef']:.2f}", f"maFATse{s}": f"{fat['se']:.2f}", f"maFATt{s}": f"{fat['stat']:.2f}",
            f"maShareSig{s}": f"{r['ess']['share_sig']:.2f}", f"maNsig{s}": str(r["ess"]["n_sig"]),
            f"maExpSig{s}": f"{r['ess']['expected_share']:.2f}", f"maESS{s}": f"{r['ess']['ESS']:+.2f}",
            f"maExpSigTau{s}": f"{r['ess_tau']['expected_share']:.2f}",
            f"maESSTau{s}": f"{r['ess_tau']['ESS']:+.2f}",
        })
    macros.update(power_robustness(samples, res))
    um.write_macros(macros, um.TAB / "macros_power_bias.tex", comment="02_code/04_power_bias.py")

    # ---- figures -------------------------------------------------------------
    for n in FIGURE_SAMPLES:
        if n not in samples:
            continue
        r = res[n]
        title = f"{um.SAMPLE_LABELS[n]} (k = {r['k']})"
        um.funnel_plot(samples[n], r["uwls"].est, f"funnel_{n}", pet=r["pet"].est, title=title)
        um.funnel_plot(samples[n], r["uwls"].est, f"funnel_precision_{n}", pet=r["pet"].est,
                       title=title, precision=True)
        um.power_plot(samples[n], r["uwls"].est, f"power_{n}", title=title)

    print("\nsaved 04_report/tables/pubbias_estimates.tex/.csv, power_bias_stats.tex/.csv, "
          "power_by_study.csv, macros_power_bias.tex")
    print("saved 04_report/figures/funnel_*, funnel_precision_*, power_*")


if __name__ == "__main__":
    main()
