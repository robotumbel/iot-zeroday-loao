"""Additional baselines requested in the first-round review (E12).

  mlp-react   MLP (all training data) with ReAct activation clipping (Sun et al., NeurIPS 2021):
              penultimate activations clipped at their 90th training percentile, energy score
  knn-raw     non-parametric open-set baseline: distance to the 10th nearest training flow in the
              signed-log standardized feature space (no learned representation)
  rf-coral    RF on signed-log standardized features after CORAL alignment (Sun et al., AAAI 2016):
              target features are whitened with the covariance of the unlabeled warm-up window and
              re-coloured with the source covariance; a label-free domain-adaptation baseline (P3)
  mlp-coral   the same alignment in front of the MLP (Mahalanobis score)

Same splits, thresholds (warm-up budget, clean window) and metrics as the other detectors.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from scipy import linalg
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loao.adaptation import make_warmup  # noqa: E402
from loao.calibration import target_warmup_far  # noqa: E402
from loao.data import feature_columns  # noqa: E402
from loao.metrics import BENIGN, UNKNOWN, open_set_report, threshold_free  # noqa: E402
from loao.splits import load_split  # noqa: E402
from loao.tabular import MLPConfig, MLPDetector  # noqa: E402

FARS = (0.01, 0.05)


def slog(x: np.ndarray) -> np.ndarray:
    return np.sign(x) * np.log1p(np.abs(x))


class Std:
    def fit(self, X):
        lx = slog(X)
        self.mu, self.sd = np.nanmean(lx, 0), np.nanstd(lx, 0) + 1e-6
        return self

    def __call__(self, X):
        return np.nan_to_num((slog(X) - self.mu) / self.sd, nan=0.0, posinf=0.0, neginf=0.0)


def coral(src: np.ndarray, tgt_window: np.ndarray, eps: float = 1.0):
    """Return a function mapping target rows into the source second-order statistics."""
    cs = np.cov(src, rowvar=False) + eps * np.eye(src.shape[1])
    ct = np.cov(tgt_window, rowvar=False) + eps * np.eye(src.shape[1])
    a = np.real(linalg.fractional_matrix_power(ct, -0.5) @ linalg.fractional_matrix_power(cs, 0.5))
    mt, ms = tgt_window.mean(0), src.mean(0)
    return lambda x: (x - mt) @ a + ms


def react_energy(det: MLPDetector, df: pd.DataFrame, clip: float) -> np.ndarray:
    x = det._prep(df).to(det.dev)
    det.net.eval()
    out = []
    with torch.no_grad():
        for b in range(0, len(x), 8192):
            z = det.net.body(x[b:b + 8192]).clamp(max=clip)
            out.append((-torch.logsumexp(det.net.head(z), dim=-1)).cpu())
    return torch.cat(out).numpy()


def run(manifest: Path, a) -> list[dict]:
    split = load_split(manifest)
    u = split.unit_col
    f = [c for c in feature_columns(split.train) if pd.api.types.is_numeric_dtype(split.train[c])]
    X = lambda d: d[f].to_numpy(dtype=float)  # noqa: E731
    test, train = split.test, split.train
    y_unk = split.y_test_unknown.to_numpy()
    is_ben = (test[u] == BENIGN).to_numpy()
    warm, _ = make_warmup(split.target_pool, u, 2000, 0.0, a.seed)
    std = Std().fit(X(train))
    rows = []

    def emit(name, s_test, s_warm, closed, t0):
        base = {"split_id": split.spec.split_id, **asdict(split.spec), "method": name, "seed_run": a.seed,
                "n_train": len(train), "seconds": round(time.time() - t0, 1)}
        base.update(threshold_free(y_unk, s_test, is_ben))
        for far in FARS:
            th = target_warmup_far(s_warm, far)
            pred = np.where(th.flags(s_test), UNKNOWN, closed)
            r = dict(base, calibration=th.rule, threshold=th.value)
            r.update(open_set_report(test[u].to_numpy(), pred, split.spec.holdout))
            rows.append(r)

    for det in a.detectors:
        t0 = time.time()
        if det == "mlp-react":
            m = MLPDetector(MLPConfig(seed=a.seed)).fit(train, f, train[u].to_numpy())
            with torch.no_grad():
                zt = m.net.body(m._prep(train).to(m.dev)).cpu().numpy()
            clip = float(np.percentile(zt, 90))
            emit(det, react_energy(m, test, clip), react_energy(m, warm, clip), m.score(test)["pred"], t0)
        elif det == "knn-raw":
            xs = std(X(train))
            idx = np.random.default_rng(a.seed).choice(len(xs), min(20000, len(xs)), replace=False)
            nn = NearestNeighbors(n_neighbors=10).fit(xs[idx])
            sc = lambda d: nn.kneighbors(std(X(d)))[0][:, -1]  # noqa: E731
            closed = np.full(len(test), BENIGN, dtype=object)  # distance alone names no attack
            emit(det, sc(test), sc(warm), closed, t0)
        elif det in ("rf-coral", "mlp-coral"):
            if split.spec.source == split.spec.target:
                continue  # alignment is the identity within one network
            xs = std(X(train))
            g = coral(xs, std(X(warm)))
            if det == "rf-coral":
                rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=a.seed,
                                            class_weight="balanced").fit(xs, train[u].to_numpy())
                pt, pw = rf.predict_proba(g(std(X(test)))), rf.predict_proba(g(std(X(warm))))
                emit(det, 1 - pt.max(1), 1 - pw.max(1), rf.classes_[pt.argmax(1)], t0)
            else:
                # The MLP standardizes internally; feed it aligned features mapped back to raw-like scale
                # by giving it the aligned standardized matrix as its input columns.
                tr = pd.DataFrame(xs, columns=f).assign(**{u: train[u].to_numpy()})
                te = pd.DataFrame(g(std(X(test))), columns=f)
                wa = pd.DataFrame(g(std(X(warm))), columns=f)
                m = MLPDetector(MLPConfig(seed=a.seed)).fit(tr, f, train[u].to_numpy())
                st, sw = m.score(te), m.score(wa)
                emit(det, st["maha"], sw["maha"], st["pred"], t0)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--only", nargs="*", default=["P1__", "P3__"])
    ap.add_argument("--detectors", nargs="+", default=["mlp-react", "knn-raw", "rf-coral", "mlp-coral"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    index = pd.read_csv(Path(a.splits) / "index.csv")
    ids = index.loc[index["status"] == "ok", "split_id"]
    ids = ids[ids.apply(lambda s: any(o in s for o in a.only))]
    rows = []
    for sid in ids:
        res = run(Path(a.splits) / f"{sid}.json", a)
        rows += res
        print(sid, {r["method"]: round(r["auroc_ood"], 3) for r in res}, flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)


if __name__ == "__main__":
    main()
