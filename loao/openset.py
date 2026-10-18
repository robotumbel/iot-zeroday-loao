"""Open-set scores shared by every neural detector (higher = more likely an unseen attack).

msp     1 - max softmax probability
energy  -logsumexp(logits)
knn     cosine distance to the k-th nearest training embedding (embeddings are L2-normalized)
maha    min over known classes of the Mahalanobis distance, class means + shared covariance
        with Ledoit-Wolf shrinkage (Lee et al., NeurIPS 2018)
"""

from __future__ import annotations

import numpy as np
import torch
from sklearn.covariance import LedoitWolf

SCORES = ("msp", "energy", "knn", "maha")


class OpenSetScorer:
    def __init__(self, k: int = 10, device: str | torch.device = "cpu"):
        self.k = k
        self.dev = torch.device(device)

    def fit(self, bank_emb: torch.Tensor, bank_labels: np.ndarray) -> "OpenSetScorer":
        self.bank = bank_emb.float().to(self.dev)
        z = bank_emb.double().numpy()
        labels = np.asarray(bank_labels)
        classes = [c for c in np.unique(labels) if (labels == c).sum() >= 2]
        mu = np.stack([z[labels == c].mean(0) for c in classes])
        centered = np.concatenate([z[labels == c] - m for c, m in zip(classes, mu)])
        prec = LedoitWolf().fit(centered).precision_
        self.mu = torch.tensor(mu, dtype=torch.float64)
        self.prec = torch.tensor(prec, dtype=torch.float64)
        self.mu_p_mu = torch.einsum("cd,de,ce->c", self.mu, self.prec, self.mu)
        return self

    @torch.no_grad()
    def score(self, logits: torch.Tensor, emb: torch.Tensor) -> dict[str, np.ndarray]:
        logits = logits.float()
        prob = torch.softmax(logits, dim=-1)
        kth = []
        for b in range(0, len(emb), 4096):
            s = emb[b:b + 4096].float().to(self.dev) @ self.bank.T
            kth.append(s.topk(min(self.k, self.bank.shape[0]), dim=1).values[:, -1].cpu())
        z = emb.double()
        zp = z @ self.prec
        d = (zp * z).sum(1, keepdim=True) - 2 * zp @ self.mu.T + self.mu_p_mu
        return {
            "msp": (1.0 - prob.max(-1).values).numpy(),
            "energy": (-torch.logsumexp(logits, dim=-1)).numpy(),
            "knn": (1.0 - torch.cat(kth)).numpy(),
            "maha": d.min(1).values.float().numpy(),
        }
