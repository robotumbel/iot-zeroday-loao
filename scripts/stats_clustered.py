"""Dataset-aware view of the planned P1 comparisons (reviewer concern: splits from the same dataset share
training data, so they are not independent observations).

For each planned comparison and metric:
  - mean difference and wins/losses separately within NF-ToN-IoT-v3 (7 splits) and NF-BoT-IoT-v3 (3 splits)
  - dataset-balanced mean difference (each dataset weighted 1/2) with a stratified bootstrap 95% CI
    (splits resampled within their dataset, 10,000 draws)
  - whether the sign agrees in both datasets
Writes results/stats_clustered.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import stats_tests  # noqa: E402

METRICS = [("auroc_ood", "target_warmup_far0.01"), ("unknown_recall", "target_warmup_far0.01"),
           ("benign_false_alarm_rate", "target_warmup_far0.01")]


def one(d: pd.DataFrame, a: str, b: str, metric: str, rng) -> dict:
    p = d[d["combo"].isin([a, b])].groupby(["block", "combo"])[metric].mean().unstack().dropna()
    if a not in p or b not in p:
        return {}
    diff = p[a] - p[b]
    ds = pd.Series(diff.index.str.split("|").str[1].str[:3], index=diff.index)
    out = {}
    means = []
    boots = []
    for name in ("ton", "bot"):
        x = diff[ds == name].to_numpy()
        out[f"{name}_mean"] = x.mean()
        out[f"{name}_WL"] = f"{int((x > 0).sum())}/{int((x < 0).sum())}"
        means.append(x.mean())
        boots.append(rng.choice(x, (10000, len(x))).mean(1))
    out["balanced_mean"] = float(np.mean(means))
    bb = (boots[0] + boots[1]) / 2
    out["ci_low"], out["ci_high"] = np.percentile(bb, [2.5, 97.5])
    out["same_sign_both"] = bool(np.sign(means[0]) == np.sign(means[1]))
    return out


def main() -> None:
    rng = np.random.default_rng(0)
    parts = ["# Dataset-aware planned comparisons (P1)\n",
             "Balanced mean: average of the two per-dataset means. CI: stratified bootstrap over splits within each"
             " dataset. W/L: splits won/lost by the first detector.\n"]
    for metric, rule in METRICS:
        d = stats_tests.load(rule, 0.0, [0, 1, 2])
        d = d[d["protocol"] == "P1"]
        rows = []
        for a, b, q in stats_tests.PLANNED:
            r = one(d, a, b, metric, rng)
            if r:
                rows.append({"comparison": f"{a} - {b}", **r})
        t = pd.DataFrame(rows)
        parts.append(f"## {metric} ({rule})\n\n```\n{t.round(4).to_string(index=False)}\n```\n")
    text = "\n".join(parts)
    (ROOT / "results/stats_clustered.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
