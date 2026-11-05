"""
01_prepare_data.py -- Schritt 1 im PLAN.md

Reads the replication data of Zschirnt & Ruedin (2016) (Harvard Dataverse,
doi:10.7910/DVN/ZU8H79, file 01_data/raw_files/meta-clean.csv) and builds

    01_data/zr2016_studies.csv            34 studies with call-back counts (study level)
    01_data/zr2016_subgroups.csv          215 subgroups with call-back counts
    01_data/zr2016_studies_no_counts.csv  9 studies without counts (not in the OR analysis)

For every row: ln OR and SE from the 2x2 table, exactly as metafor::escalc(measure = "OR"):
    a = call-backs minority, b = no call-back minority,
    c = call-backs majority, d = no call-back majority.

Check: our ORs must match the forest plot of the original (Figure 1 /
meta-replication.pdf) to 2 decimals.

Run from the repository root:  python 02_code/01_prepare_data.py
"""

import numpy as np
import pandas as pd

import utils_meta as um

RAW_CSV = um.RAW / "meta-clean.csv"

COUNT_COLS = {
    "positive.treatment.minority": "cb_minority",
    "negative.treatment.minority": "nocb_minority",
    "positive.treatment.majority": "cb_majority",
    "negative.treatment.majority": "nocb_majority",
}

# Forest plot of the original study level model (meta-replication.pdf, p. 5),
# same order as the rows in meta-clean.csv: (OR, CI low, CI high)
PUBLISHED_FOREST = [
    (2.45, 1.86, 3.22), (0.75, 0.61, 0.91), (0.32, 0.09, 1.12), (0.87, 0.72, 1.05),
    (0.67, 0.48, 0.93), (0.64, 0.45, 0.90), (0.52, 0.23, 1.16), (0.43, 0.33, 0.56),
    (0.78, 0.54, 1.13), (0.59, 0.46, 0.76), (0.50, 0.38, 0.68), (0.47, 0.40, 0.54),
    (0.49, 0.43, 0.55), (0.33, 0.26, 0.43), (0.59, 0.50, 0.69), (0.58, 0.48, 0.70),
    (0.94, 0.79, 1.12), (0.22, 0.11, 0.44), (0.39, 0.32, 0.48), (0.39, 0.25, 0.61),
    (0.50, 0.44, 0.57), (0.34, 0.12, 0.97), (0.50, 0.42, 0.60), (0.62, 0.53, 0.74),
    (0.55, 0.45, 0.66), (0.81, 0.63, 1.04), (0.27, 0.17, 0.43), (0.56, 0.47, 0.68),
    (0.77, 0.66, 0.90), (0.82, 0.73, 0.91), (0.86, 0.75, 0.99), (0.63, 0.52, 0.76),
    (0.92, 0.69, 1.22), (0.67, 0.48, 0.95),
]


def read_raw() -> pd.DataFrame:
    d = pd.read_csv(RAW_CSV, encoding="utf-8")
    d.columns = [c.strip() for c in d.columns]
    for c in d.columns:
        if d[c].dtype == object or pd.api.types.is_string_dtype(d[c]):
            d[c] = d[c].str.strip()
    return d


def add_variables(d: pd.DataFrame) -> pd.DataFrame:
    """Effect sizes and moderators in our own (English, snake_case) names."""
    out = pd.DataFrame(index=d.index)
    out["authors"] = d["author"]
    out["year"] = d["year"].astype(int)
    out["country"] = d["country"]
    out["region_original"] = d["region"]
    out = out.join(um.region_variables(d["country"]))
    out["directive"] = d["directive"]
    out["directive_after"] = d["directive"].map({"after": 1, "before": 0})  # NA outside the EU
    out["testing_year"] = d["testing.year.implicit"]
    out["gen_explicit"] = d["firstgen.explicit"]
    out["gen_implicit"] = d["firstgen.implicit"]
    out["second_gen"] = d["firstgen.implicit"].map({"second": 1, "first": 0})
    out["gender"] = d["gender"]
    out["skills"] = d["skills"]
    out["skill_high"] = d["skills"].map({"high": 1, "low": 0, "mixed": 0})
    out["skill_low"] = d["skills"].map({"high": 0, "low": 1, "mixed": 0})
    minority = (d["minority"].str.replace(r",?\s*\n\s*", ", ", regex=True)
                .str.replace(r"\s+", " ", regex=True).str.strip(" ,"))
    out["minority"] = minority.str[:1].str.upper() + minority.str[1:]

    for raw, new in COUNT_COLS.items():
        out[new] = d[raw]
    out["n_minority"] = out["cb_minority"] + out["nocb_minority"]
    out["n_majority"] = out["cb_majority"] + out["nocb_majority"]
    out["cb_rate_minority"] = out["cb_minority"] / out["n_minority"]
    out["cb_rate_majority"] = out["cb_majority"] / out["n_majority"]
    out["relative_cb_rate"] = d["relative.call.back.rate"]  # majority / minority (paper's measure)

    y, se = um.log_odds_ratio(out["cb_minority"], out["nocb_minority"],
                              out["cb_majority"], out["nocb_majority"])
    out["log_or"] = y
    out["se"] = se
    out["or"] = np.exp(y)
    out["ci_low"] = np.exp(y - um.Z975 * se)
    out["ci_high"] = np.exp(y + um.Z975 * se)
    out["in_original"] = 1
    out["new"] = 0
    out["source"] = "Dataverse meta-clean.csv"
    return out


def make_labels(df: pd.DataFrame) -> pd.Series:
    """'Author, Year'; country added where the same label appears twice."""
    base = df["authors"] + ", " + df["year"].astype(str)
    dup = base.duplicated(keep=False)
    return np.where(dup, base + " (" + df["country"] + ")", base)


def main() -> None:
    um.ensure_dirs()
    raw = read_raw()
    has_counts = raw[list(COUNT_COLS)].notna().all(axis=1)

    # ---- study level -------------------------------------------------------
    glob = raw[raw["global"] == "global"]
    studies = add_variables(glob[has_counts[glob.index]]).reset_index(drop=True)
    studies.insert(0, "label", make_labels(studies))
    studies.insert(0, "study_id", [f"ZR{i + 1:02d}" for i in range(len(studies))])

    no_counts = glob[~has_counts[glob.index]][["author", "year", "country", "minority",
                                               "relative.call.back.rate"]]

    # ---- subgroup level ----------------------------------------------------
    sub = raw[raw["global"] == "subgroup"]
    subgroups = add_variables(sub[has_counts[sub.index]]).reset_index(drop=True)
    subgroups.insert(0, "label", subgroups["authors"] + ", " + subgroups["year"].astype(str))

    # ---- checks ------------------------------------------------------------
    print(f"meta-clean.csv: {(raw['global'] == 'global').sum()} studies, "
          f"{(raw['global'] == 'subgroup').sum()} subgroups")
    print(f"with call-back counts: {len(studies)} studies, {len(subgroups)} subgroups")
    assert len(studies) == 34, "expected 34 studies with counts (original: k = 34)"
    assert len(subgroups) == 215, "expected 215 subgroups with counts (original: k = 215)"

    pub = pd.DataFrame(PUBLISHED_FOREST, columns=["or", "ci_low", "ci_high"])
    diff = (studies[["or", "ci_low", "ci_high"]].round(2) - pub).abs().max(axis=1)
    bad = studies.loc[diff > 0.011, ["label", "or", "ci_low", "ci_high"]]
    if len(bad):
        print("WARNING: these ORs do not match the published forest plot:")
        print(bad.to_string())
    else:
        print("check: all 34 ORs match the published forest plot (2 decimals)  OK")

    n_zero = int(((subgroups[["cb_minority", "nocb_minority", "cb_majority", "nocb_majority"]] == 0)
                  .any(axis=1)).sum())
    if n_zero:
        print(f"note: {n_zero} subgroups with a zero cell -> 0.5 added to all cells (as metafor)")

    # ---- save --------------------------------------------------------------
    studies.to_csv(um.STUDIES_CSV, index=False)
    subgroups.to_csv(um.SUBGROUPS_CSV, index=False)
    no_counts.to_csv(um.DATA / "zr2016_studies_no_counts.csv", index=False)
    print(f"saved {um.STUDIES_CSV.relative_to(um.ROOT)}  ({len(studies)} rows)")
    print(f"saved {um.SUBGROUPS_CSV.relative_to(um.ROOT)}  ({len(subgroups)} rows)")
    print(f"saved 01_data/zr2016_studies_no_counts.csv  ({len(no_counts)} studies without counts:)")
    for _, r in no_counts.iterrows():
        print(f"    {r['author']} {r['year']} ({r['country']})")

    print("\nshort overview (study level):")
    print(f"  applications: {int(studies['n_minority'].sum() + studies['n_majority'].sum()):,}")
    print(f"  publication years: {studies['year'].min()}-{studies['year'].max()}")
    print("  continents: " + ", ".join(f"{k} {v}" for k, v in studies["continent"].value_counts().items()))


if __name__ == "__main__":
    main()
