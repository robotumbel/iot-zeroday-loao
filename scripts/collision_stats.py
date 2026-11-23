"""Label-collision statistics on the full NF-v3 files and a near-duplicate check for reconnaissance.

1. For every flow in the full CSV, hash (a) the 47 model features (identifiers removed) and (b) all
   columns except the labels (identifiers kept). Report the share of rows whose feature vector occurs
   with more than one attack label, per label pair, for both variants.
2. Near duplicates: on a processed (de-duplicated) dataset, the share of flows of each attack family
   whose nearest neighbour (log-standardized features) is benign.

Output: results/collision_stats.md
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from loao.data import feature_columns  # noqa: E402

DATA = {"NF-ToN-IoT-v3": ("nf_ton_iot_v3", "data/raw/NF-ToN-IoT-v3/NF-ToN-IoT-v3.csv"),
        "NF-BoT-IoT-v3": ("nf_bot_iot_v3", "data/raw/NF-BoT-IoT-v3/NF-BoT-IoT-v3.csv"),
        "NF-UNSW-NB15-v3": ("nf_unsw_nb15_v3", "data/raw/NF-UNSW-NB15-v3/NF-UNSW-NB15-v3.csv"),
        "NF-CICIDS2018-v3": ("nf_cicids2018_v3", "data/raw/NF-CICIDS2018-v3/NF-CICIDS2018-v3.csv")}


def full_file(name: str, cfg: dict, path: Path) -> list[str]:
    drop = [c for c in cfg["drop_columns"]]
    time_cols = ["FLOW_START_MILLISECONDS", "FLOW_END_MILLISECONDS"]
    hs_feat, hs_host, hs_all, labs = [], [], [], []
    for chunk in pd.read_csv(path, chunksize=1_000_000, low_memory=False):
        lab = chunk["Attack"].astype(str)
        feats = chunk.drop(columns=[c for c in drop + ["Attack"] if c in chunk.columns])
        host = chunk.drop(columns=[c for c in time_cols + ["DNS_QUERY_ID", "Attack", "Label"] if c in chunk.columns])
        allc = chunk.drop(columns=[c for c in ("Attack", "Label") if c in chunk.columns])
        hs_feat.append(pd.util.hash_pandas_object(feats, index=False).to_numpy())
        hs_host.append(pd.util.hash_pandas_object(host, index=False).to_numpy())
        hs_all.append(pd.util.hash_pandas_object(allc, index=False).to_numpy())
        labs.append(lab.to_numpy())
    lab = np.concatenate(labs)
    out = [f"### {name}: {len(lab):,} flows"]
    for title, hs in (("identifiers removed (model features)", hs_feat),
                      ("IP addresses and ports kept, timestamps removed", hs_host),
                      ("all columns kept (timestamps make rows unique)", hs_all)):
        h = np.concatenate(hs)
        d = pd.DataFrame({"h": h, "lab": lab})
        nlab = d.groupby("h")["lab"].nunique()
        conf = d["h"].map(nlab) > 1
        out.append(f"- {title}: {conf.mean():.1%} of rows have a feature vector seen with more than one label "
                   f"({int(conf.sum()):,} rows; {int((nlab > 1).sum()):,} distinct vectors)")
        if conf.any():
            sets = d[conf].drop_duplicates(["h", "lab"]).groupby("h")["lab"].apply(lambda s: tuple(sorted(s)))
            rows_per = d[conf].groupby("h").size()
            pairs = Counter()
            for hh, labs_ in sets.items():
                pairs[" / ".join(labs_)] += int(rows_per[hh])
            top = ", ".join(f"{k}: {v:,} rows" for k, v in pairs.most_common(5))
            out.append(f"  - most affected label sets: {top}")
            share = d[conf].groupby("lab").size() / d.groupby("lab").size()
            out.append("  - share of each label's rows in conflicting vectors: "
                       + ", ".join(f"{k} {v:.1%}" for k, v in share.dropna().sort_values(ascending=False).items()))
    return out


def near_duplicates(processed: Path) -> list[str]:
    df = pd.read_parquet(processed)
    feats = [c for c in feature_columns(df) if pd.api.types.is_numeric_dtype(df[c])]
    x = df[feats].to_numpy(float)
    lx = np.sign(x) * np.log1p(np.abs(x))
    z = np.nan_to_num((lx - np.nanmean(lx, 0)) / (np.nanstd(lx, 0) + 1e-6))
    fam = df["family"].to_numpy()
    out = [f"### Near duplicates in {processed.name} (after de-duplication)"]
    nn = NearestNeighbors(n_neighbors=2).fit(z)
    dist, idx = nn.kneighbors(z)
    nb = fam[idx[:, 1]]
    for f in sorted(set(fam) - {"BENIGN"}):
        m = fam == f
        out.append(f"- {f}: {np.mean(nb[m] == 'BENIGN'):.1%} of flows have a benign nearest neighbour "
                   f"(median distance {np.median(dist[m, 1]):.3f})")
    m = fam == "BENIGN"
    out.append(f"- BENIGN: {np.mean(nb[m] == 'BENIGN'):.1%} of benign flows have a benign nearest neighbour")
    return out


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", nargs="+", default=list(DATA))
    ap.add_argument("--out", default="results/collision_stats.md")
    a = ap.parse_args()
    cfgs = json.loads((ROOT / "configs/datasets.json").read_text(encoding="utf-8"))
    parts = ["# Label collisions and near duplicates\n", "## Full files\n"]
    for name, (key, rel) in DATA.items():
        if name not in a.datasets:
            continue
        parts += full_file(name, cfgs[key], ROOT / rel)
        print("\n".join(parts[-6:]), flush=True)
    parts.append("\n## Near duplicates (seed 0)\n")
    for name, (key, _) in DATA.items():
        if name in a.datasets:
            parts += near_duplicates(ROOT / f"data/processed/{key}__cap20000__seed0.parquet")
    text = "\n".join(parts) + "\n"
    (ROOT / a.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
