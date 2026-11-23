"""Extra baselines requested in the pre-submission review.

  iforest   Isolation Forest trained on benign source flows only (no attack labels)
  ae        autoencoder trained on benign source flows only; score = reconstruction error
  lightgbm  supervised gradient boosting on all source units; score = 1 - max class probability

Benign-only detectors cannot name a known attack, so a flow is either BENIGN or UNKNOWN for them;
compare them on AUROC of the held-out unit against benign flows (`auroc_unknown_vs_benign`) and on
unknown recall at a fixed benign false-alarm budget. Thresholds: source benign budget and the
target warm-up budget, as for the other detectors.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import IsolationForest
from torch import nn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loao.adaptation import make_warmup  # noqa: E402
from loao.calibration import benign_far, target_warmup_far  # noqa: E402
from loao.data import feature_columns  # noqa: E402
from loao.metrics import BENIGN, UNKNOWN, open_set_report, threshold_free  # noqa: E402
from loao.splits import load_split  # noqa: E402


class Prep:
    """Signed log transform + standardization fitted on the training rows."""

    def fit(self, X: np.ndarray) -> "Prep":
        lx = np.sign(X) * np.log1p(np.abs(X))
        self.mu, self.sd = np.nanmean(lx, 0), np.nanstd(lx, 0) + 1e-6
        return self

    def __call__(self, X: np.ndarray) -> np.ndarray:
        lx = np.sign(X) * np.log1p(np.abs(X))
        return np.nan_to_num((lx - self.mu) / self.sd, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)


class AE:
    def __init__(self, d: int, seed: int, epochs: int = 30):
        torch.manual_seed(seed)
        self.net = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Linear(64, 16), nn.ReLU(),
                                 nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, d))
        self.epochs, self.rng = epochs, np.random.default_rng(seed)

    def fit(self, X: np.ndarray) -> "AE":
        x = torch.tensor(X)
        opt = torch.optim.AdamW(self.net.parameters(), lr=1e-3, weight_decay=1e-5)
        for _ in range(self.epochs):
            for b in np.array_split(self.rng.permutation(len(x)), max(1, len(x) // 256)):
                loss = ((self.net(x[b]) - x[b]) ** 2).mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
        return self

    @torch.no_grad()
    def score(self, X: np.ndarray) -> np.ndarray:
        x = torch.tensor(X)
        return ((self.net(x) - x) ** 2).mean(1).numpy()


def run(manifest: Path, a) -> list[dict]:
    split = load_split(manifest)
    u = split.unit_col
    feats = [c for c in feature_columns(split.train) if pd.api.types.is_numeric_dtype(split.train[c])]
    X = lambda d: d[feats].to_numpy(dtype=float)  # noqa: E731
    test = split.test
    y_unk = split.y_test_unknown.to_numpy()
    is_benign = (test[u] == BENIGN).to_numpy()
    benign_val = split.val[split.val[u] == BENIGN]
    warms = {c: make_warmup(split.target_pool, u, a.warmup_n, c, a.seed) for c in a.contamination}
    rows = []
    for det in a.detectors:
        t0 = time.time()
        if det in ("iforest", "ae"):
            ben = split.train[split.train[u] == BENIGN]
            prep = Prep().fit(X(ben))
            if det == "iforest":
                m = IsolationForest(n_estimators=200, random_state=a.seed, n_jobs=-1).fit(prep(X(ben)))
                score_fn = lambda d: -m.score_samples(prep(X(d)))  # noqa: E731
            else:
                m = AE(len(feats), a.seed).fit(prep(X(ben)))
                score_fn = lambda d: m.score(prep(X(d)))  # noqa: E731
            closed = np.full(len(test), BENIGN, dtype=object)
        else:
            import lightgbm as lgb
            prep = None
            m = lgb.LGBMClassifier(n_estimators=200, class_weight="balanced", random_state=a.seed, verbose=-1)
            m.fit(X(split.train), split.train[u].to_numpy())
            if det == "lightgbm_energy":
                # Energy over the raw multiclass margins (log-odds), the tree analogue of the logit energy.
                from scipy.special import logsumexp
                score_fn = lambda d: -logsumexp(m.predict(X(d), raw_score=True), axis=1)  # noqa: E731
            else:
                score_fn = lambda d: 1.0 - m.predict_proba(X(d)).max(1)  # noqa: E731
            closed = m.classes_[m.predict_proba(X(test)).argmax(1)]
        train_s = time.time() - t0
        t1 = time.time()
        s_test = score_fn(test)
        ms = 1000 * (time.time() - t1) / max(len(test), 1)
        ths = [(th, None) for th in (benign_far(score_fn(benign_val), f) for f in a.far)]
        for c, (w, winfo) in warms.items():
            ths += [(target_warmup_far(score_fn(w), f), winfo) for f in a.far]
        base = {"split_id": split.spec.split_id, **asdict(split.spec), "method": det, "score": "native",
                "n_test": len(test), "n_test_unknown": int(y_unk.sum()), "train_seconds": round(train_s, 2),
                "ms_per_flow": round(ms, 5)}
        base.update(threshold_free(y_unk, s_test, is_benign))
        for th, winfo in ths:
            pred = np.where(th.flags(s_test), UNKNOWN, closed)
            r = dict(base, calibration=th.rule, threshold=th.value,
                     warmup_contamination=winfo["warmup_contamination"] if winfo else np.nan)
            r.update(open_set_report(test[u].to_numpy(), pred, split.spec.holdout))
            rows.append(r)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--detectors", nargs="+", default=["iforest", "ae", "lightgbm"])
    ap.add_argument("--far", type=float, nargs="+", default=[0.01, 0.05])
    ap.add_argument("--warmup-n", type=int, default=2000)
    ap.add_argument("--contamination", type=float, nargs="+", default=[0.0, 0.05])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    index = pd.read_csv(Path(a.splits) / "index.csv")
    ids = index.loc[index["status"] == "ok", "split_id"]
    if a.only:
        ids = ids[ids.apply(lambda s: any(o in s for o in a.only))]
    rows = []
    for sid in ids:
        res = run(Path(a.splits) / f"{sid}.json", a)
        rows += res
        auc = {r["method"]: (r["auroc_ood"], r["auroc_unknown_vs_benign"]) for r in res}
        print(sid, {k: f"{v[0]:.3f}/{v[1]:.3f}" for k, v in auc.items()}, flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    (out.with_suffix(".config.json")).write_text(json.dumps(vars(a), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
