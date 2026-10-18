"""Statistical comparison of detectors over splits and seeds.

Unit of analysis: a split (protocol, source, target, held-out unit). Each method's metric is
first averaged over seeds within a split, so seeds are not treated as independent samples.

Reports
  - mean +/- std across seeds of the split-averaged metric (seed stability)
  - Friedman test over all method x score combinations, average ranks, Nemenyi critical difference
  - planned pairwise comparisons: Wilcoxon signed-rank (two-sided), Holm correction,
    mean difference with a bootstrap 95% CI and win/tie/loss counts

Usage:
  python scripts/stats_tests.py --metric auroc_ood --out results/stats_auroc.md
  python scripts/stats_tests.py --metric unknown_recall --rule target_warmup_far0.05 --out ...
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, studentized_range, wilcoxon

ROOT = Path(__file__).resolve().parent.parent

# file pattern (seed placeholder {s}) -> method label
FILES = {
    "results/rf_msp_full_family_seed{s}.csv": "RF full",
    "results/rf_msp_cap2000_family_seed{s}.csv": "RF 2k",
    "results/mlp_cap2000_family_seed{s}.csv": "MLP 2k",
    "results/mlp_full_family_seed{s}.csv": "MLP full",
    "results/l1_tiny-local_family_seed{s}.csv": "tiny-local",
    "results/l1_distilbert_family_seed{s}.csv": "DistilBERT",
    "results/l1_secbert_family_seed{s}.csv": "SecBERT",
    "results/l1_secbert-kv_family_seed{s}.csv": "SecBERT-kv",
    "results/rf_msp_bin5_cap2000_family_seed{s}.csv": "RF 2k bin5",
    "results/mlp_bin5_cap2000_family_seed{s}.csv": "MLP 2k bin5",
}

# One score per detector, fixed before the extended analysis: MSP for RF (its only score) and
# Mahalanobis for every embedding-based detector.
PRIMARY = {"RF full": "msp", "RF 2k": "msp", "MLP full": "maha", "MLP 2k": "maha", "tiny-local": "maha",
           "DistilBERT": "maha", "SecBERT": "maha", "SecBERT-kv": "maha", "RF 2k bin5": "msp",
           "MLP 2k bin5": "maha"}

PLANNED = [
    ("DistilBERT|knn", "RF 2k|msp", "LLM vs RF, same training sample"),
    ("DistilBERT|knn", "RF full|msp", "LLM vs RF with all training data"),
    ("DistilBERT|knn", "MLP 2k|knn", "language model vs plain MLP, same score"),
    ("DistilBERT|knn", "tiny-local|knn", "effect of pretraining"),
    ("DistilBERT|knn", "SecBERT|knn", "general vs security-domain pretraining"),
    ("DistilBERT|maha", "DistilBERT|knn", "Mahalanobis vs kNN score"),
    ("MLP 2k|knn", "RF 2k|msp", "embedding distance vs RF confidence"),
    ("MLP 2k|maha", "MLP 2k|knn", "Mahalanobis vs kNN score (MLP)"),
    # Extended set added after the pre-submission review: every encoder configuration against RF.
    ("DistilBERT|maha", "RF 2k|msp", "best encoder score vs RF, same sample"),
    ("DistilBERT|maha", "RF full|msp", "best encoder score vs RF, all data"),
    ("DistilBERT|maha", "MLP 2k|maha", "encoder vs MLP, both Mahalanobis"),
    ("SecBERT|maha", "RF 2k|msp", "security encoder vs RF, same sample"),
    ("SecBERT|maha", "RF full|msp", "security encoder vs RF, all data"),
    ("SecBERT-kv|maha", "SecBERT|maha", "raw-value vs 5-level serialization"),
    ("SecBERT-kv|knn", "SecBERT|knn", "raw-value vs 5-level serialization (kNN)"),
    ("RF 2k bin5|msp", "RF 2k|msp", "5-level discretization, RF"),
    ("MLP 2k bin5|maha", "MLP 2k|maha", "5-level discretization, MLP"),
]


def rank_biserial(diff: np.ndarray) -> float:
    """Matched-pairs rank-biserial correlation (zero differences dropped)."""
    d = diff[diff != 0]
    if len(d) == 0:
        return 0.0
    r = pd.Series(np.abs(d)).rank().to_numpy()
    return float((r[d > 0].sum() - r[d < 0].sum()) / r.sum())


def load(rule: str, contamination: float, seeds: list[int]) -> pd.DataFrame:
    frames = []
    for pat, label in FILES.items():
        for s in seeds:
            p = ROOT / pat.format(s=s)
            if not p.exists():
                continue
            d = pd.read_csv(p)
            if "norm" in d:
                d = d[d["norm"] == "none"]
            if "score" not in d:
                d = d.assign(score="msp")
            d = d[d["calibration"] == rule]
            if "warmup_contamination" in d:
                c = d["warmup_contamination"].round(3)
                d = d[c.isna() | (c == round(contamination, 3))]
            d = d.drop_duplicates(["split_id", "score"])
            frames.append(d.assign(method=label, seed_run=s))
    d = pd.concat(frames, ignore_index=True)
    d["block"] = d["protocol"] + "|" + d["source"].str[3:6] + ">" + d["target"].str[3:6] + "|" + d["holdout"].astype(str)
    d["combo"] = d["method"] + "|" + d["score"]
    return d


def holm(p: list[float]) -> list[float]:
    order = np.argsort(p)
    adj = np.empty(len(p))
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(p) - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj.tolist()


def boot_ci(x: np.ndarray, n: int = 10000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    means = rng.choice(x, (n, len(x)), replace=True).mean(1)
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def analyse(d: pd.DataFrame, metric: str, scope: str) -> str:
    out = [f"### Scope: {scope}"]
    seeds_per = d.groupby("combo")["seed_run"].nunique()
    full = seeds_per[seeds_per == seeds_per.max()].index
    d = d[d["combo"].isin(full)]
    # Seed stability: per seed, mean over blocks; then mean/std over seeds.
    per_seed = d.groupby(["combo", "seed_run"])[metric].mean().unstack()
    stab = pd.DataFrame({"mean": per_seed.mean(axis=1), "std_over_seeds": per_seed.std(axis=1),
                         "seeds": per_seed.notna().sum(axis=1)})
    # Blocks x combos, averaged over seeds; keep blocks complete for every combo.
    m = d.groupby(["block", "combo"])[metric].mean().unstack().dropna()
    n, k = m.shape
    out.append(f"Blocks (splits) = {n}, method x score combinations = {k}, seeds = {int(stab['seeds'].max())}\n")
    ranks = m.rank(axis=1, ascending=False).mean().sort_values()
    stab = stab.loc[ranks.index].assign(avg_rank=ranks.round(2))
    out.append("```\n" + stab.round(3).to_string() + "\n```")
    if n >= 3 and k >= 3:
        stat, p = friedmanchisquare(*[m[c].to_numpy() for c in m.columns])
        q = studentized_range.ppf(0.95, k, np.inf) / np.sqrt(2)
        cd = q * np.sqrt(k * (k + 1) / (6 * n))
        out.append(f"\nFriedman chi2 = {stat:.2f}, p = {p:.2e}. Nemenyi critical difference (alpha 0.05) = {cd:.2f} ranks. "
                   f"Two combinations differ significantly when their average ranks differ by more than {cd:.2f}.")
    rows = []
    for a_, b_, why in PLANNED:
        if a_ not in m or b_ not in m:
            continue
        diff = (m[a_] - m[b_]).to_numpy()
        p = wilcoxon(diff, zero_method="zsplit").pvalue if np.any(diff != 0) else 1.0
        lo, hi = boot_ci(diff)
        rows.append({"comparison": f"{a_} - {b_}", "question": why, "mean_diff": diff.mean(), "ci95_low": lo,
                     "ci95_high": hi, "wins": int((diff > 0).sum()), "ties": int((diff == 0).sum()),
                     "losses": int((diff < 0).sum()), "r_rb": rank_biserial(diff), "p_wilcoxon": p})
    # Friedman / Nemenyi over one pre-specified score per detector.
    prim = [f"{mth}|{sc}" for mth, sc in PRIMARY.items() if f"{mth}|{sc}" in m]
    if n >= 3 and len(prim) >= 3:
        mp = m[prim]
        stat, pp = friedmanchisquare(*[mp[c].to_numpy() for c in mp.columns])
        kp = len(prim)
        cdp = studentized_range.ppf(0.95, kp, np.inf) / np.sqrt(2) * np.sqrt(kp * (kp + 1) / (6 * n))
        rk = mp.rank(axis=1, ascending=False).mean().sort_values()
        out.append(f"\nPrimary-score analysis ({kp} detectors, one score each): Friedman chi2 = {stat:.2f}, "
                   f"p = {pp:.2e}, Nemenyi CD = {cdp:.2f}. Average ranks: "
                   + ", ".join(f"{c} {v:.2f}" for c, v in rk.items()))
    if rows:
        t = pd.DataFrame(rows)
        t["p_holm"] = holm(t["p_wilcoxon"].tolist())
        out.append(f"\nPlanned comparisons (positive mean_diff = first method higher; Holm over the {len(t)} "
                   "comparisons in this table; r_rb = matched-pairs rank-biserial effect size):\n")
        out.append("```\n" + t.round(4).to_string(index=False) + "\n```")
        if n < 6:
            out.append(f"\nNote: with {n} blocks the smallest attainable two-sided Wilcoxon p-value is "
                       f"{2 / 2 ** n:.3f}; treat this scope as descriptive.")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", default="auroc_ood")
    ap.add_argument("--rule", default="target_warmup_far0.01",
                    help="threshold rule; irrelevant for threshold-free metrics such as auroc_ood")
    ap.add_argument("--contamination", type=float, default=0.0)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    d = load(a.rule, a.contamination, a.seeds)
    parts = [f"# Statistical comparison — metric `{a.metric}`, rule `{a.rule}`, warm-up contamination "
             f"{a.contamination:g}, seeds {a.seeds}\n"]
    p1 = d[d["protocol"] == "P1"]
    for scope, sub in [("all splits (P1 + P3)", d), ("P1 only", p1),
                       ("P1, NF-ToN-IoT-v3 only", p1[p1["source"].str.contains("ton")]),
                       ("P1, NF-BoT-IoT-v3 only", p1[p1["source"].str.contains("bot")]),
                       ("P3 only", d[d["protocol"] == "P3"])]:
        parts.append(analyse(sub, a.metric, scope))
    text = "\n\n".join(parts) + "\n"
    print(text)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
