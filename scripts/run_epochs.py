"""Training-length study for the fine-tuned encoders (reviewer request: two epochs, no tuning).

For each split the encoder is fine-tuned once for --epochs epochs (linear decay over the whole run).
A CPU copy of the weights is kept after every epoch; after training, each snapshot is evaluated:

  source validation (known units only, held-out unit never present): cross-entropy loss, macro-F1
  target test: AUROC-OOD per score, known macro-F1, and unknown recall / total benign alert rate
               at the 1% warm-up budget (clean window of 2,000 flows)

Validation-based selection picks the epoch with the best source-validation macro-F1 (ties: lower
loss), using no held-out labels. One output row per split x epoch x score.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loao.adaptation import make_warmup  # noqa: E402
from loao.calibration import target_warmup_far  # noqa: E402
from loao.data import feature_columns  # noqa: E402
from loao.encoders import EncoderConfig, FlowEncoder  # noqa: E402
from loao.metrics import UNKNOWN, open_set_report, threshold_free  # noqa: E402
from loao.openset import SCORES  # noqa: E402
from loao.serialize import FlowSerializer  # noqa: E402
from loao.splits import load_split  # noqa: E402
from run_neural import cap_per_unit  # noqa: E402


def val_metrics(enc: FlowEncoder, texts: list[str], labels: np.ndarray) -> dict:
    logits, _ = enc._forward(texts)
    idx = {c: i for i, c in enumerate(enc.classes_)}
    y = torch.tensor([idx[v] for v in labels])
    loss = float(torch.nn.functional.cross_entropy(logits, y))
    pred = enc.classes_[logits.argmax(-1).numpy()]
    return {"val_loss": loss, "val_macro_f1": float(f1_score(labels, pred, average="macro"))}


def run(manifest: Path, a: argparse.Namespace) -> list[dict]:
    split = load_split(manifest)
    u = split.unit_col
    feats = [c for c in feature_columns(split.train) if pd.api.types.is_numeric_dtype(split.train[c])]
    train = cap_per_unit(split.train, u, a.max_train_per_unit, a.seed)
    val = cap_per_unit(split.val, u, a.max_val_per_unit, a.seed)
    test = split.test
    warm, _ = make_warmup(split.target_pool, u, a.warmup_n, 0.0, a.seed)
    ser = FlowSerializer("sentence").fit(train[feats])
    tx = lambda d: ser.transform(d[feats])  # noqa: E731
    t_train, t_val, t_test, t_warm = tx(train), tx(val), tx(test), tx(warm)

    cfg = EncoderConfig(model=a.model, epochs=a.epochs, lr=a.lr, seed=a.seed)
    enc = FlowEncoder(cfg)
    snaps: list = []
    enc.fit(t_train, train[u].to_numpy(), snapshots=snaps)
    y_unk = (test[u] == split.spec.holdout).astype(int).to_numpy()
    is_ben = (test[u] == "BENIGN").to_numpy()
    rows = []
    for ep, state in enumerate(snaps, start=1):
        enc.load_snapshot(state)
        vm = val_metrics(enc, t_val, val[u].to_numpy())
        s_test = enc.score(t_test)
        s_warm = enc.score(t_warm)
        for sc in SCORES:
            r = {"split_id": split.spec.split_id, "protocol": split.spec.protocol, "holdout": split.spec.holdout,
                 "model": a.model, "seed": a.seed, "epoch": ep, "epochs_total": a.epochs, "score": sc,
                 "train_seconds_total": round(enc.train_seconds, 1), **vm}
            r.update(threshold_free(y_unk, s_test[sc], is_ben))
            th = target_warmup_far(s_warm[sc], 0.01)
            pred = np.where(th.flags(s_test[sc]), UNKNOWN, s_test["pred"])
            rep = open_set_report(test[u].to_numpy(), pred, split.spec.holdout)
            r.update({k: rep[k] for k in ("unknown_recall", "benign_false_alarm_rate", "benign_rejected_as_unknown",
                                          "known_macro_f1")})
            rows.append(r)
        print(f"  epoch {ep}: val_f1={vm['val_macro_f1']:.3f} val_loss={vm['val_loss']:.3f} "
              f"maha AUROC={[x['auroc_ood'] for x in rows if x['epoch'] == ep and x['score'] == 'maha'][0]:.3f}",
              flush=True)
    del snaps
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--model", default="distilbert")
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--max-train-per-unit", type=int, default=2000)
    ap.add_argument("--max-val-per-unit", type=int, default=500)
    ap.add_argument("--warmup-n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    index = pd.read_csv(Path(a.splits) / "index.csv")
    ids = index.loc[index["status"] == "ok", "split_id"]
    if a.only:
        ids = ids[ids.apply(lambda s: any(o in s for o in a.only))]
    out = Path(a.out)
    done = set(pd.read_csv(out)["split_id"]) if out.exists() else set()
    for sid in ids:
        if sid in done:
            continue
        print(sid, flush=True)
        rows = run(Path(a.splits) / f"{sid}.json", a)
        pd.DataFrame(rows).to_csv(out, mode="a", header=not out.exists(), index=False)


if __name__ == "__main__":
    main()
