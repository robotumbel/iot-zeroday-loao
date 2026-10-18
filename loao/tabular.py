"""Non-language neural baseline: MLP on numeric NetFlow features with the same open-set scores.

It separates "a learned embedding + distance score" from "language-model pretraining":
same scores (msp, energy, knn, maha), same training sample, no text and no pretraining.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from torch import nn

from .openset import OpenSetScorer


@dataclass
class MLPConfig:
    hidden: tuple[int, ...] = (256, 128)
    dropout: float = 0.1
    epochs: int = 30
    batch_size: int = 256
    lr: float = 1e-3
    weight_decay: float = 1e-4
    knn_k: int = 10
    knn_bank_size: int = 5000
    seed: int = 0


class _Net(nn.Module):
    def __init__(self, d_in: int, hidden: tuple[int, ...], n_out: int, dropout: float):
        super().__init__()
        layers, d = [], d_in
        for h in hidden:
            layers += [nn.Linear(d, h), nn.ReLU(), nn.Dropout(dropout)]
            d = h
        self.body = nn.Sequential(*layers)
        self.head = nn.Linear(d, n_out)

    def forward(self, x):
        z = self.body(x)
        return self.head(z), z


class MLPDetector:
    def __init__(self, cfg: MLPConfig):
        self.cfg = cfg
        self.dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.train_seconds = 0.0
        self.token_stats: dict = {}

    def _prep(self, df: pd.DataFrame) -> torch.Tensor:
        x = df[self.features].to_numpy(dtype=float)
        x = np.sign(x) * np.log1p(np.abs(x))  # heavy-tailed counts and rates
        x = np.nan_to_num((x - self.mean) / self.std, nan=0.0, posinf=0.0, neginf=0.0)
        return torch.tensor(x, dtype=torch.float32)

    def fit(self, df: pd.DataFrame, features: list[str], labels: np.ndarray) -> "MLPDetector":
        cfg = self.cfg
        torch.manual_seed(cfg.seed)
        rng = np.random.default_rng(cfg.seed)
        self.features = features
        raw = df[features].to_numpy(dtype=float)
        lx = np.sign(raw) * np.log1p(np.abs(raw))
        self.mean = np.nanmean(lx, 0)
        self.std = np.nanstd(lx, 0) + 1e-6
        x = self._prep(df).to(self.dev)
        self.classes_, y = np.unique(labels, return_inverse=True)
        yt = torch.tensor(y, device=self.dev)
        self.net = _Net(x.shape[1], cfg.hidden, len(self.classes_), cfg.dropout).to(self.dev)
        counts = np.bincount(y, minlength=len(self.classes_))
        w = torch.tensor(len(y) / (len(counts) * np.maximum(counts, 1)), dtype=torch.float, device=self.dev)
        loss_fn = nn.CrossEntropyLoss(weight=w)
        opt = torch.optim.AdamW(self.net.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
        t0 = time.time()
        self.net.train()
        for _ in range(cfg.epochs):
            perm = torch.tensor(rng.permutation(len(y)), device=self.dev)
            for b in range(0, len(y), cfg.batch_size):
                bi = perm[b:b + cfg.batch_size]
                logits, _ = self.net(x[bi])
                loss = loss_fn(logits, yt[bi])
                opt.zero_grad(set_to_none=True)
                loss.backward()
                opt.step()
        self.train_seconds = time.time() - t0
        bank_idx = rng.choice(len(y), min(cfg.knn_bank_size, len(y)), replace=False)
        _, emb = self._forward(x[bank_idx])
        self.scorer = OpenSetScorer(cfg.knn_k, self.dev).fit(emb, y[bank_idx])
        return self

    @torch.no_grad()
    def _forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        self.net.eval()
        logits, emb = [], []
        for b in range(0, len(x), 8192):
            lo, z = self.net(x[b:b + 8192].to(self.dev))
            logits.append(lo.cpu())
            emb.append(nn.functional.normalize(z, dim=-1).cpu())
        return torch.cat(logits), torch.cat(emb)

    def score(self, df: pd.DataFrame) -> dict:
        t0 = time.time()
        logits, emb = self._forward(self._prep(df))
        infer_s = time.time() - t0
        out = self.scorer.score(logits, emb)
        out["pred"] = self.classes_[logits.argmax(-1).numpy()]
        out["ms_per_flow"] = 1000.0 * infer_s / max(len(df), 1)
        return out
