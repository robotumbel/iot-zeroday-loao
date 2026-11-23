"""Appendix table for the revision: all 17 planned P1 comparisons (AUROC-OOD and unknown recall at a 1%
warm-up budget), with the dataset-balanced difference from results/stats_clustered.md.
Writes paper/tables/planned_all.tex (table body rows only)."""
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
NAMES = {"DistilBERT": "D", "SecBERT-kv": "S-raw", "SecBERT": "S", "tiny-local": "tiny", "RF full": "RF all",
         "RF 2k bin5": "RF 2k 5-lev.", "MLP 2k bin5": "MLP 2k 5-lev.", "maha": "M", "knn": "$k$NN", "msp": "MSP"}


def short(c: str) -> str:
    out = []
    for side in c.split(" - "):
        det, sc = side.split("|")
        out.append(f"{NAMES.get(det, det)}-{NAMES[sc]}")
    return r" $-$ ".join(out)


def num(x: float, d: int = 3) -> str:
    return f"${x:+.{d}f}$".replace("+", "+")


def planned(path: Path) -> pd.DataFrame:
    txt = path.read_text(encoding="utf-8")
    blk = txt.split("### Scope: P1 only")[1].split("### Scope:")[0]
    tab = blk.split("Planned comparisons")[1].split("```")[1]
    return pd.read_fwf(io.StringIO(tab.strip("\n")))


def clustered(metric: str) -> pd.DataFrame:
    txt = (ROOT / "results/stats_clustered.md").read_text(encoding="utf-8")
    blk = txt.split(f"## {metric} ")[1].split("```")[1]
    return pd.read_fwf(io.StringIO(blk.strip("\n")))


def comparisons() -> str:
    rows = []
    for title, f, m in (("AUROC-OOD", "stats_auroc_3seeds.md", "auroc_ood"),
                        (r"Unknown recall at a 1\% warm-up budget", "stats_recall_far1_3seeds.md", "unknown_recall")):
        d = planned(ROOT / "results" / f)
        c = clustered(m).set_index("comparison")
        rows.append(r"\multicolumn{7}{|l|}{\textit{" + title + r"}} \\")
        for _, r in d.iterrows():
            cc = c.loc[r["comparison"]]
            same = "yes" if str(cc["same_sign_both"]) == "True" else "no"
            rows.append(f"{short(r['comparison'])} & {num(r['mean_diff'])} & {int(r['wins'])}/{int(r['losses'])} & "
                        f"{num(r['r_rb'], 2)} & {r['p_holm']:.3f} & {num(cc['balanced_mean'])} "
                        f"[{num(cc['ci_low'])}, {num(cc['ci_high'])}] & {same} " + r"\\")
    return "\n".join(rows)


if __name__ == "__main__":
    out = ROOT / "paper/tables"
    out.mkdir(parents=True, exist_ok=True)
    (out / "planned_all.tex").write_text(comparisons() + "\n", encoding="utf-8")
    print((out / "planned_all.tex").read_text(encoding="utf-8")[:600])
