"""Neural detectors per split, with open-set scores and warm-up calibration.

  --model mlp                        MLP on numeric NetFlow features (no text, no pretraining)
  --model distilbert|secbert|tiny-local   L1: transformer encoder fine-tuned on serialized flows

Thresholds (no labels from the held-out unit, see loao/calibration.py):
  benign_far         budget on source benign validation flows
  target_warmup_far  budget on an unlabeled warm-up window from the target network
Scores: msp, energy, knn, maha (loao/openset.py). One output row per split x score x rule.
Results are appended after every split, and finished splits are skipped on restart.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loao.adaptation import make_warmup  # noqa: E402
from loao.calibration import benign_far, target_warmup_far  # noqa: E402
from loao.data import feature_columns  # noqa: E402
from loao.encoders import EncoderConfig, FlowEncoder  # noqa: E402
from loao.openset import SCORES  # noqa: E402
from loao.tabular import MLPConfig, MLPDetector  # noqa: E402
from loao.metrics import BENIGN, UNKNOWN, open_set_report, threshold_free  # noqa: E402
from loao.serialize import Discretizer, FlowSerializer  # noqa: E402
from loao.splits import load_split  # noqa: E402

def cap_per_unit(df: pd.DataFrame, unit: str, n: int, seed: int) -> pd.DataFrame:
    if n <= 0:
        return df
    rng = np.random.default_rng(seed)
    df = df.iloc[rng.permutation(len(df))]
    return df[df.groupby(unit).cumcount() < n]


def run(manifest: Path, a: argparse.Namespace) -> list[dict]:
    split = load_split(manifest)
    u = split.unit_col
    feats = [c for c in feature_columns(split.train) if pd.api.types.is_numeric_dtype(split.train[c])]
    train = cap_per_unit(split.train, u, a.max_train_per_unit, a.seed)
    test = cap_per_unit(split.test, u, a.max_test_per_unit, a.seed)
    benign_val = split.val[split.val[u] == BENIGN]
    warms = {c: make_warmup(split.target_pool, u, a.warmup_n, c, a.seed) for c in a.contamination}

    if a.model == "mlp":
        method = "MLP" + (f"-bin{a.discretize}" if a.discretize else "") + ("-nan" if a.nan_token else "")
        if a.discretize:  # same quantile bins the text serialization uses
            disc = Discretizer(a.discretize, nan_token=a.nan_token).fit(train[feats])

            def inp(d):
                d = d.copy()
                d[feats] = disc.transform(d[feats])
                return d
        else:
            inp = lambda d: d  # noqa: E731
        enc = MLPDetector(MLPConfig(epochs=a.epochs, lr=a.lr, seed=a.seed)).fit(inp(train), feats, train[u].to_numpy())
    else:
        # Non-default serializations get their own method name so results and score files stay separate.
        method = f"L1-{a.model}" + ("" if a.scheme == "sentence" else f"-{a.scheme}") + ("-nan" if a.nan_token else "")
        ser = FlowSerializer(a.scheme, nan_token=a.nan_token).fit(train[feats])
        inp = lambda d: ser.transform(d[feats])  # noqa: E731
        cfg = EncoderConfig(model=a.model, max_length=a.max_length, epochs=a.epochs, batch_size=a.batch_size,
                            lr=a.lr, seed=a.seed)
        enc = FlowEncoder(cfg).fit(inp(train), train[u].to_numpy())
    s_test = enc.score(inp(test))
    s_ben = enc.score(inp(benign_val))
    s_warm = {c: enc.score(inp(w)) for c, (w, _) in warms.items()}

    # Keep raw per-flow scores so thresholds can be recomputed later without retraining.
    sdir = Path(a.out).parent / "scores" / f"{method}_cap{a.max_train_per_unit}"
    sdir.mkdir(parents=True, exist_ok=True)
    arrays = {f"test_{k}": s_test[k] for k in (*SCORES, "pred")}
    arrays["test_unit"] = test[u].to_numpy().astype(str)
    arrays.update({f"benign_val_{k}": s_ben[k] for k in SCORES})
    for c, (w, _) in warms.items():
        arrays.update({f"warm{c:g}_{k}": s_warm[c][k] for k in SCORES})
        arrays[f"warm{c:g}_unit"] = w[u].to_numpy().astype(str)
    np.savez_compressed(sdir / f"{split.spec.split_id}.npz", **arrays)

    y_unk = (test[u] == split.spec.holdout).astype(int).to_numpy() if split.spec.holdout else np.zeros(len(test), int)
    base = {"split_id": split.spec.split_id, **asdict(split.spec), "method": method,
            "scheme": a.scheme if a.model != "mlp" else "numeric", "max_train_per_unit": a.max_train_per_unit,
            "n_train": len(train), "n_test": len(test), "n_test_unknown": int(y_unk.sum()),
            "train_seconds": round(enc.train_seconds, 1), "ms_per_flow": round(s_test["ms_per_flow"], 3),
            **enc.token_stats}
    rows = []
    for sc in SCORES:
        b = dict(base, score=sc)
        b.update(threshold_free(y_unk, s_test[sc]))
        ths = [(th, None) for th in (benign_far(s_ben[sc], f) for f in a.far)]
        for c, (_, winfo) in warms.items():
            ths += [(target_warmup_far(s_warm[c][sc], f), winfo) for f in a.far]
        for th, winfo in ths:
            pred = np.where(th.flags(s_test[sc]), UNKNOWN, s_test["pred"])
            r = dict(b, calibration=th.rule, threshold=th.value,
                     warmup_size=winfo["warmup_size"] if winfo else np.nan,
                     warmup_contamination=winfo["warmup_contamination"] if winfo else np.nan)
            r.update(open_set_report(test[u].to_numpy(), pred, split.spec.holdout))
            rows.append(r)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--only", nargs="*", default=None, help="keep split_ids containing any of these substrings")
    ap.add_argument("--model", default="distilbert", help="mlp | distilbert | secbert | tiny-local | HF repo id")
    ap.add_argument("--scheme", default="binned", choices=["kv", "binned", "sentence"])
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--max-train-per-unit", type=int, default=2000)
    ap.add_argument("--max-test-per-unit", type=int, default=0, help="0 = full test partition")
    ap.add_argument("--far", type=float, nargs="+", default=[0.01, 0.05])
    ap.add_argument("--warmup-n", type=int, default=2000)
    ap.add_argument("--contamination", type=float, nargs="+", default=[0.0, 0.05])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--discretize", type=int, default=0, help="MLP only: train/test on N-level quantile bins")
    ap.add_argument("--nan-token", action="store_true", help="write missing values as 'missing' (default: top level)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    index = pd.read_csv(Path(a.splits) / "index.csv")
    ids = index.loc[index["status"] == "ok", "split_id"]
    if a.only:
        ids = ids[ids.apply(lambda s: any(o in s for o in a.only))]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set(pd.read_csv(out)["split_id"]) if out.exists() else set()
    (out.with_suffix(".config.json")).write_text(json.dumps(vars(a), indent=2), encoding="utf-8")
    for sid in ids:
        if sid in done:
            print(f"skip {sid}")
            continue
        rows = run(Path(a.splits) / f"{sid}.json", a)
        pd.DataFrame(rows).to_csv(out, mode="a", header=not out.exists(), index=False)
        best = {r["score"]: r["auroc_ood"] for r in rows}
        r0 = rows[0]
        print(f"{sid}: AUROC " + " ".join(f"{k}={v:.3f}" for k, v in best.items()) + " "
              f"train={r0['train_seconds']}s infer={r0['ms_per_flow']}ms/flow",
              flush=True)


if __name__ == "__main__":
    main()
