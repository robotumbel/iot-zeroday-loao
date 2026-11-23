"""E9 (training length) and E14 (SecBERT with an explicit missing-value token) summaries.

E9: results/revision/epochs_{model}_family_seed0.csv, one row per split x epoch x score.
    Mean over the P1 splits per epoch, and the epoch chosen per split by validation macro-F1
    (highest) or validation loss (lowest), compared with the 2 epochs used in the main results.
E14: results/revision/l1_secbert-nan_family_seed{s}.csv against results/l1_secbert_family_seed{s}.csv
    on the same splits (P1 with NF-BoT-IoT-v3, all P3), Mahalanobis score, warm-up 1% budget.
Writes results/e9_e14_summary.md.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MET = ["auroc_ood", "unknown_recall", "benign_rejected_as_unknown", "known_macro_f1"]


def e9(model: str) -> list[str]:
    f = ROOT / f"results/revision/epochs_{model}_family_seed0.csv"
    if not f.exists():
        return []
    d = pd.read_csv(f)
    d = d[d["protocol"] == "P1"]
    n = d["split_id"].nunique()
    out = [f"## E9 {model}: {n} P1 splits, seed 0\n"]
    per_epoch = d.groupby(["score", "epoch"])[MET + ["val_macro_f1", "val_loss"]].mean().round(3)
    out.append(per_epoch.to_markdown() + "\n")
    for score, g in d.groupby("score"):
        rows = {}
        for rule, pick in (("epoch 2 (main results)", lambda x: x[x["epoch"] == 2]),
                           ("best val macro-F1", lambda x: x.loc[[x["val_macro_f1"].idxmax()]]),
                           ("lowest val loss", lambda x: x.loc[[x["val_loss"].idxmin()]]),
                           ("epoch 6", lambda x: x[x["epoch"] == x["epoch"].max()])):
            sel = pd.concat([pick(x) for _, x in g.groupby("split_id")])
            rows[rule] = sel[MET].mean().round(3).to_dict() | {"mean epoch": round(sel["epoch"].mean(), 2)}
        out.append(f"### {score}: epoch selection\n")
        out.append(pd.DataFrame(rows).T.to_markdown() + "\n")
        best = g.groupby("split_id")["auroc_ood"].agg(["min", "max"])
        out.append(f"AUROC-OOD range across epochs per split, mean of (max-min): {(best['max'] - best['min']).mean():.3f}\n")
    return out


def e14() -> list[str]:
    out = []
    a, b = [], []
    for s in range(3):
        fa = ROOT / f"results/revision/l1_secbert-nan_family_seed{s}.csv"
        fb = ROOT / f"results/l1_secbert_family_seed{s}.csv"
        if fa.exists() and fb.exists():
            a.append(pd.read_csv(fa))
            b.append(pd.read_csv(fb))
    if not a:
        return out
    a, b = pd.concat(a), pd.concat(b)

    def sel(d):
        d = d[(d["calibration"] == "target_warmup_far0.01") & (d["score"] == "maha")]
        if "warmup_contamination" in d:
            d = d[d["warmup_contamination"].round(2) == 0]
        return d

    a, b = sel(a), sel(b)
    b = b[b["split_id"].isin(set(a["split_id"]))]
    out.append(f"## E14 SecBERT, explicit missing token vs default ({a['split_id'].nunique()} split-seeds)\n")
    rows = []
    for name, d in (("missing token", a), ("default", b)):
        for p, g in d.groupby("protocol"):
            rows.append({"variant": name, "protocol": p, "n": len(g)} | g[["auroc_ood", "unknown_recall",
                                                                          "benign_false_alarm_rate"]].mean().round(3).to_dict())
    out.append(pd.DataFrame(rows).to_markdown(index=False) + "\n")
    return out


def epochs_table() -> None:
    """Per-epoch means over the P1 splits (learning curves) -> paper/tables/epochs.tex."""
    lines = []
    for model, name in (("distilbert", "DistilBERT"), ("secbert", "SecBERT")):
        f = ROOT / f"results/revision/epochs_{model}_family_seed0.csv"
        if not f.exists():
            continue
        d = pd.read_csv(f)
        d = d[d["protocol"] == "P1"]
        for ep, g in d.groupby("epoch"):
            m = g[g["score"] == "maha"].mean(numeric_only=True)
            s = g[g["score"] == "msp"].mean(numeric_only=True)
            e = g[g["score"] == "energy"].mean(numeric_only=True)
            cells = [m["val_macro_f1"], m["val_loss"], m["known_macro_f1"], m["auroc_ood"], m["unknown_recall"],
                     s["auroc_ood"], e["auroc_ood"]]
            fmt = " & ".join(f"{v:.3f}".replace("0.", ".", 1) for v in cells)
            lines.append(f"{name if ep == 1 else ''} & {ep} & {fmt} \\\\")
        lines.append(r"\hline")
    if lines and lines[-1] == r"\hline":
        lines.pop()
    (ROOT / "paper/tables").mkdir(parents=True, exist_ok=True)
    (ROOT / "paper/tables/epochs.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    epochs_table()
    out = e9("distilbert") + e9("secbert") + e14()
    text = "\n".join(out)
    (ROOT / "results/e9_e14_summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
