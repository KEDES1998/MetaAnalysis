"""
03_update.py -- Schritte 3 und 4 im PLAN.md (Aufgabe 3 des Prof)

1. Reads the new studies from 01_data/update_studies.csv (filled in by hand).
   If the file does not exist, an empty template is created.
2. Computes ln OR and SE for every new study:
     - preferred: from the call-back counts
         n_minority, cb_minority, n_majority, cb_majority
     - otherwise: from a reported OR and its 95 % CI (or, ci_low, ci_high)
3. Question A: Do the new ORs lie in the 95 % CI of the original RE estimate?
   (also shown: the 95 % prediction interval, which is the fairer benchmark for
   one single new study under heterogeneity)
4. Question B: New pooled estimate with all studies -- does it change much?
5. Writes 01_data/combined_studies.csv (used by 04 and 05), a forest plot with the
   new studies in red, and the table of evidence for the appendix.

Example row for update_studies.csv (one row per study, all minorities pooled):
    study_id,authors,year,title,journal,country,testing_year,minority,gender,skills,
    n_minority,cb_minority,n_majority,cb_majority,or,ci_low,ci_high,source,notes
    NEW01,Koopmans et al.,2019,Taste or statistics?,Ethnic and Racial Studies,Germany,2014,
    35 origin groups,both,mixed,5000,1500,1000,400,,,,"Table 2, p. 240",numbers made up!

Run from the repository root:  python 02_code/03_update.py
"""

import sys
from dataclasses import replace

import numpy as np
import pandas as pd

import utils_meta as um

TEMPLATE_COLUMNS = [
    "study_id", "authors", "year", "title", "journal", "country", "testing_year", "minority",
    "gender", "skills", "n_minority", "cb_minority", "n_majority", "cb_majority",
    "or", "ci_low", "ci_high", "source", "notes",
]

# columns kept in combined_studies.csv
KEEP = ["study_id", "label", "authors", "year", "country", "continent", "europe", "eu",
        "german_speaking", "testing_year", "minority", "gender", "skills", "skill_high", "skill_low",
        "second_gen", "directive_after", "cb_minority", "n_minority", "cb_majority", "n_majority",
        "log_or", "se", "or", "ci_low", "ci_high", "in_original", "new", "source"]


def read_update() -> pd.DataFrame | None:
    """Read and check update_studies.csv; returns None if there are no studies yet."""
    if not um.UPDATE_CSV.exists():
        pd.DataFrame(columns=TEMPLATE_COLUMNS).to_csv(um.UPDATE_CSV, index=False)
        print(f"created empty template {um.UPDATE_CSV.relative_to(um.ROOT)} -- please fill in the new studies")
        return None
    up = pd.read_csv(um.UPDATE_CSV)
    up = up.dropna(how="all")
    if len(up) == 0:
        print(f"{um.UPDATE_CSV.relative_to(um.ROOT)} has no studies yet -- nothing to update")
        return None

    missing = [c for c in ("authors", "year", "country") if up[c].isna().any()]
    if missing:
        sys.exit(f"ERROR in update_studies.csv: empty values in column(s) {missing}")

    counts = ["n_minority", "cb_minority", "n_majority", "cb_majority"]
    has_counts = up[counts].notna().all(axis=1)
    has_ci = up[["or", "ci_low", "ci_high"]].notna().all(axis=1)
    problem = up.loc[~has_counts & ~has_ci, "authors"]
    if len(problem):
        sys.exit("ERROR: these studies need either the 4 count columns or or/ci_low/ci_high:\n  "
                 + "\n  ".join(problem))
    bad = has_counts & ((up["cb_minority"] > up["n_minority"]) | (up["cb_majority"] > up["n_majority"]))
    if bad.any():
        sys.exit(f"ERROR: call-backs larger than applications for: {list(up.loc[bad, 'authors'])}")

    y = pd.Series(np.nan, index=up.index)
    se = pd.Series(np.nan, index=up.index)
    if has_counts.any():
        u = up[has_counts]
        yy, ss = um.log_odds_ratio(u["cb_minority"], u["n_minority"] - u["cb_minority"],
                                   u["cb_majority"], u["n_majority"] - u["cb_majority"])
        y[has_counts], se[has_counts] = yy, ss
    use_ci = ~has_counts & has_ci
    if use_ci.any():
        u = up[use_ci]
        y[use_ci] = np.log(u["or"])
        se[use_ci] = um.se_from_ci(u["ci_low"], u["ci_high"])
        print("note: SE from the reported CI for: " + ", ".join(u["authors"]))

    out = up.copy()
    out["log_or"], out["se"] = y, se
    out["or"] = np.exp(y)
    out["ci_low"] = np.exp(y - um.Z975 * se)
    out["ci_high"] = np.exp(y + um.Z975 * se)
    out = out.join(um.region_variables(out["country"]))
    unknown = out.loc[out["continent"] == "Other", "country"].unique()
    if len(unknown):
        print(f"note: countries coded as 'Other' (add them in utils_meta.py if European): {list(unknown)}")
    out["skill_high"] = out["skills"].map({"high": 1, "low": 0, "mixed": 0})
    out["skill_low"] = out["skills"].map({"high": 0, "low": 1, "mixed": 0})
    out["second_gen"] = np.nan
    out["directive_after"] = np.where(out["eu"] == 1, 1.0, np.nan)  # all new studies are after 2000
    out["label"] = out["authors"].str.strip() + ", " + out["year"].astype(int).astype(str)
    if out["study_id"].isna().any():
        out["study_id"] = [f"NEW{i + 1:02d}" for i in range(len(out))]
    out["in_original"] = 0
    out["new"] = 1
    out["source"] = out["source"].fillna("own coding")
    return out


def evidence_table(df: pd.DataFrame) -> None:
    """Table of evidence for the appendix.

    longtable over several pages; Overleaf preamble needs \\usepackage{booktabs,longtable,array}.
    """
    d = df.sort_values(["new", "year", "authors"]).reset_index(drop=True)
    rag = r">{\raggedright\arraybackslash}"
    lines = [
        r"{\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        rf"\begin{{longtable}}{{{rag}p{{3.4cm}}lr{rag}p{{3.2cm}}rrrr}}",
        r"\caption{Table of evidence: all studies in the meta-analysis}\label{tab:evidence}\\",
        r"\toprule",
        r"Study & Country & Test & Minority group & $N$ & CB (\%) & OR [95\% CI] & SE \\",
        r" & & year & & & min. / maj. & & \\",
        r"\midrule\endfirsthead",
        r"\toprule",
        r"Study & Country & Test & Minority group & $N$ & CB (\%) & OR [95\% CI] & SE \\",
        r" & & year & & & min. / maj. & & \\",
        r"\midrule\endhead",
        r"\bottomrule\endfoot",
    ]
    for i, r in d.iterrows():
        if i > 0 and r["new"] == 1 and d.loc[i - 1, "new"] == 0:
            lines.append(r"\midrule \multicolumn{8}{l}{\textit{New studies (update)}}\\ \midrule")
        n = r["n_minority"] + r["n_majority"] if pd.notna(r["n_minority"]) else np.nan
        cb = (f"{100 * r['cb_minority'] / r['n_minority']:.1f} / "
              f"{100 * r['cb_majority'] / r['n_majority']:.1f}") if pd.notna(n) else "--"
        minority = str(r["minority"]) if pd.notna(r["minority"]) else "--"
        ty = f"{int(r['testing_year'])}" if pd.notna(r["testing_year"]) else "--"
        cells = [um.latex_escape(r["label"]), um.latex_escape(r["country"]), ty,
                 um.latex_escape(minority), f"{int(n):,}".replace(",", "'") if pd.notna(n) else "--",
                 cb, f"{r['or']:.2f} {um.fmt_ci(r['ci_low'], r['ci_high'])}", f"{r['se']:.3f}"]
        lines.append(" & ".join(cells) + r" \\")
    lines += [r"\end{longtable}", r"\par\footnotesize $N$: applications sent (minority + majority). "
              r"CB: call-back rate of minority / majority applicants. OR: odds ratio of a call-back, "
              r"minority vs.\ majority; SE: standard error of $\ln OR$.", r"}"]
    (um.TAB / "evidence_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    d.to_csv(um.TAB / "evidence_table.csv", index=False)
    print("saved 04_report/tables/evidence_table.tex/.csv")


def main() -> None:
    um.ensure_dirs()
    orig = um.load_sample("original")
    re_orig = um.random_effects(orig["log_or"], orig["se"], "REML")
    up = read_update()

    if up is None:
        if um.COMBINED_CSV.exists():
            um.COMBINED_CSV.unlink()  # no stale combined file
        evidence_table(orig)
        return

    comb = pd.concat([orig[KEEP], up.reindex(columns=KEEP)], ignore_index=True)
    comb.to_csv(um.COMBINED_CSV, index=False)
    print(f"saved {um.COMBINED_CSV.relative_to(um.ROOT)}  ({len(orig)} original + {len(up)} new studies)")

    # ---- Question A: new studies inside the original CI / PI? -------------
    ci = (re_orig.ci_low, re_orig.ci_upp)
    pi = (re_orig.pi_low, re_orig.pi_upp)
    print(f"\nOriginal RE (REML): OR {np.exp(re_orig.est):.2f}, 95% CI {um.fmt_ci(*np.exp(ci))}, "
          f"95% PI {um.fmt_ci(*np.exp(pi))}")
    rows_a = []
    for _, r in up.iterrows():
        in_ci = ci[0] <= r["log_or"] <= ci[1]
        in_pi = pi[0] <= r["log_or"] <= pi[1]
        overlap = not (np.log(r["ci_high"]) < ci[0] or np.log(r["ci_low"]) > ci[1])
        print(f"  {r['label']:<35} OR {r['or']:.2f} {um.fmt_ci(r['ci_low'], r['ci_high'])}  "
              f"in CI: {'yes' if in_ci else 'no'}, CIs overlap: {'yes' if overlap else 'no'}, "
              f"in PI: {'yes' if in_pi else 'no'}")
        n = r["n_minority"] + r["n_majority"] if pd.notna(r.get("n_minority")) else np.nan
        rows_a.append([r["label"], r["country"], f"{int(n):,}".replace(",", "'") if pd.notna(n) else "--",
                       f"{r['or']:.2f}", um.fmt_ci(r["ci_low"], r["ci_high"]),
                       "yes" if in_ci else "no", "yes" if overlap else "no", "yes" if in_pi else "no"])
    tab_a = pd.DataFrame(rows_a, columns=["Study", "Country", "$N$", "OR", "95\\% CI",
                                          "In CI", "CIs overlap", "In PI"])
    um.to_latex_table(
        tab_a, um.TAB / "update_new_studies.tex",
        caption="New studies compared with the original meta-estimate", label="tab:update-new",
        col_format="llrrrccc",
        notes=(f"In CI: OR of the new study lies in the 95\\% CI of the original RE estimate "
               f"{um.fmt_ci(*np.exp(ci))}. CIs overlap: the study's own 95\\% CI overlaps with it. "
               f"In PI: lies in the 95\\% prediction interval {um.fmt_ci(*np.exp(pi))}."))

    # ---- Question B: pooled estimates before and after --------------------
    print("\nPooled estimates, original vs. original + new:")
    rows_b, comp = [], []
    for name, fun in [("Fixed effect (FE)", um.fixed_effect), ("UWLS", um.uwls),
                      ("Random effects (REML)", lambda y, s: um.random_effects(y, s, "REML"))]:
        a = fun(orig["log_or"].to_numpy(), orig["se"].to_numpy())
        b = fun(comb["log_or"].to_numpy(), comb["se"].to_numpy())
        print(f"  {name:<22} OR {np.exp(a.est):.3f} {um.fmt_ci(np.exp(a.ci_low), np.exp(a.ci_upp))}  ->  "
              f"{np.exp(b.est):.3f} {um.fmt_ci(np.exp(b.ci_low), np.exp(b.ci_upp))}  "
              f"(change {100 * (np.exp(b.est) / np.exp(a.est) - 1):+.1f}%)")
        rows_b.append([name, f"{np.exp(a.est):.2f} {um.fmt_ci(np.exp(a.ci_low), np.exp(a.ci_upp))}",
                       f"{np.exp(b.est):.2f} {um.fmt_ci(np.exp(b.ci_low), np.exp(b.ci_upp))}",
                       f"{100 * (np.exp(b.est) / np.exp(a.est) - 1):+.1f}\\%"])
        comp.append((name, a, b))
    tab_b = pd.DataFrame(rows_b, columns=["Method", f"Original ($k={len(orig)}$)",
                                          f"With new studies ($k={len(comb)}$)", "Change in OR"])
    um.to_latex_table(tab_b, um.TAB / "update_pooled.tex",
                      caption="Pooled odds ratio before and after the update", label="tab:update-pooled",
                      col_format="lrrr")
    pd.DataFrame([{"method": n, "sample": s, **r.as_dict()} for n, a, b in comp
                  for s, r in (("original", a), ("combined", b))]).to_csv(um.TAB / "update_pooled.csv",
                                                                          index=False)

    re_comb = comp[2][2]
    um.write_macros({
        "maKnew": str(len(up)), "maKcomb": str(len(comb)),
        "maORcomb": um.fmt(np.exp(re_comb.est), 2),
        "maCIcomb": um.fmt_ci(np.exp(re_comb.ci_low), np.exp(re_comb.ci_upp)),
        "maORnewMin": um.fmt(up["or"].min(), 2), "maORnewMax": um.fmt(up["or"].max(), 2),
        "maNnewInCI": str(int(((up["log_or"] >= ci[0]) & (up["log_or"] <= ci[1])).sum())),
    }, um.TAB / "macros_update.tex", comment="02_code/03_update.py")

    pooled = [replace(comp[2][1], method=f"RE (REML), original, k = {len(orig)}"),
              replace(re_comb, method=f"RE (REML), with new studies, k = {len(comb)}")]
    um.forest_plot(comb, pooled, "forest_combined",
                   title="Original studies (black) and new studies (red)", weights_tau2=re_comb.tau2)
    print("saved 04_report/tables/update_new_studies.tex, update_pooled.tex/.csv, macros_update.tex")
    print("saved 04_report/figures/forest_combined.pdf/.png")
    evidence_table(comb)


if __name__ == "__main__":
    main()
