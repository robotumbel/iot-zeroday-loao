"""L1: transformer encoder fine-tuned on serialized flows, with open-set scores.

Models
  distilbert   distilbert/distilbert-base-uncased (general-domain, 66M parameters)
  secbert      jackaduma/SecBERT (cybersecurity-domain BERT)
  tiny-local   small BERT trained from scratch with a WordPiece vocabulary built on the
               training texts. No download; used for smoke tests and as a "no pretraining" ablation.

Open-set scores: msp, energy, knn, maha (see loao/openset.py), computed on mean-pooled,
L2-normalized last-layer embeddings.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

from .openset import OpenSetScorer

HF_MODELS = {
    "distilbert": "distilbert/distilbert-base-uncased",
    "secbert": "jackaduma/SecBERT",
}


@dataclass
class EncoderConfig:
    model: str = "distilbert"
    max_length: int = 512
    epochs: int = 2
    batch_size: int = 32
    lr: float = 5e-5
    weight_decay: float = 0.01
    warmup_ratio: float = 0.06
    fp16: bool = True
    knn_k: int = 10
    knn_bank_size: int = 5000
    seed: int = 0


def _device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _tiny_local(train_texts: list[str], n_labels: int, max_length: int):
    from tokenizers import BertWordPieceTokenizer
    from transformers import BertConfig, BertForSequenceClassification, PreTrainedTokenizerFast

    wp = BertWordPieceTokenizer(lowercase=True)
    wp.train_from_iterator(train_texts, vocab_size=4000, min_frequency=2)
    tok = PreTrainedTokenizerFast(tokenizer_object=wp._tokenizer, unk_token="[UNK]", pad_token="[PAD]",
                                  cls_token="[CLS]", sep_token="[SEP]", mask_token="[MASK]")
    cfg = BertConfig(vocab_size=tok.vocab_size, hidden_size=128, num_hidden_layers=2, num_attention_heads=4,
                     intermediate_size=256, max_position_embeddings=max(512, max_length), num_labels=n_labels)
    return tok, BertForSequenceClassification(cfg)


def load_model(name: str, train_texts: list[str], n_labels: int, max_length: int):
    if name == "tiny-local":
        return _tiny_local(train_texts, n_labels, max_length)
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    repo = HF_MODELS.get(name, name)
    tok = AutoTokenizer.from_pretrained(repo)
    model = AutoModelForSequenceClassification.from_pretrained(repo, num_labels=n_labels)
    return tok, model


class FlowEncoder:
    def __init__(self, cfg: EncoderConfig):
        self.cfg = cfg
        self.dev = _device()
        self.classes_: np.ndarray | None = None
        self.scorer: OpenSetScorer | None = None
        self.train_seconds = 0.0
        self.token_stats: dict = {}

    def _encode(self, texts: list[str]) -> dict:
        return self.tok(texts, truncation=True, max_length=self.cfg.max_length, padding=True, return_tensors="pt")

    def fit(self, texts: list[str], labels: np.ndarray) -> "FlowEncoder":
        cfg = self.cfg
        torch.manual_seed(cfg.seed)
        np.random.seed(cfg.seed)
        self.classes_, y = np.unique(labels, return_inverse=True)
        self.tok, self.model = load_model(cfg.model, texts, len(self.classes_), cfg.max_length)
        self.model.to(self.dev)

        lens = [len(x) for x in self.tok(texts[:500], truncation=False)["input_ids"]]
        self.token_stats = {"tokens_median": float(np.median(lens)), "tokens_max": int(max(lens)),
                            "share_truncated": float(np.mean(np.array(lens) > cfg.max_length))}

        # Class-balanced loss weights.
        counts = np.bincount(y, minlength=len(self.classes_))
        w = torch.tensor(len(y) / (len(counts) * np.maximum(counts, 1)), dtype=torch.float, device=self.dev)
        loss_fn = nn.CrossEntropyLoss(weight=w)

        idx = np.arange(len(texts))
        steps_per_epoch = math.ceil(len(idx) / cfg.batch_size)
        total = steps_per_epoch * cfg.epochs
        opt = torch.optim.AdamW(self.model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
        warm = int(cfg.warmup_ratio * total)
        sched = torch.optim.lr_scheduler.LambdaLR(
            opt, lambda s: min(1.0, (s + 1) / max(warm, 1)) * max(0.0, (total - s) / max(total - warm, 1)))
        scaler = torch.amp.GradScaler("cuda", enabled=cfg.fp16 and self.dev.type == "cuda")
        rng = np.random.default_rng(cfg.seed)
        t0 = time.time()
        self.model.train()
        for _ in range(cfg.epochs):
            rng.shuffle(idx)
            for b in range(steps_per_epoch):
                bi = idx[b * cfg.batch_size:(b + 1) * cfg.batch_size]
                enc = {k: v.to(self.dev) for k, v in self._encode([texts[i] for i in bi]).items()}
                yb = torch.tensor(y[bi], device=self.dev)
                with torch.autocast(self.dev.type, dtype=torch.float16, enabled=scaler.is_enabled()):
                    logits = self.model(**enc).logits
                    loss = loss_fn(logits.float(), yb)
                opt.zero_grad(set_to_none=True)
                scaler.scale(loss).backward()
                scaler.unscale_(opt)
                nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                scaler.step(opt)
                scaler.update()
                sched.step()
        self.train_seconds = time.time() - t0
        # Free optimizer state and gradients before inference: on a 6 GB GPU they push
        # inference batches into shared system memory and slow it down about 7x.
        opt.zero_grad(set_to_none=True)
        del opt, sched, scaler
        if self.dev.type == "cuda":
            torch.cuda.empty_cache()

        # Embedding bank for the kNN and Mahalanobis scores (random subsample of training flows).
        bank_idx = rng.choice(len(texts), min(cfg.knn_bank_size, len(texts)), replace=False)
        _, emb = self._forward([texts[i] for i in bank_idx])
        self.scorer = OpenSetScorer(cfg.knn_k, self.dev).fit(emb, y[bank_idx])
        return self

    @torch.no_grad()
    def _forward(self, texts: list[str], batch_size: int = 64) -> tuple[torch.Tensor, torch.Tensor]:
        self.model.eval()
        all_logits, all_emb = [], []
        for b in range(0, len(texts), batch_size):
            enc = {k: v.to(self.dev) for k, v in self._encode(texts[b:b + batch_size]).items()}
            with torch.autocast(self.dev.type, dtype=torch.float16, enabled=self.cfg.fp16 and self.dev.type == "cuda"):
                out = self.model(**enc, output_hidden_states=True)
            h = out.hidden_states[-1].float()
            m = enc["attention_mask"].unsqueeze(-1).float()
            emb = (h * m).sum(1) / m.sum(1)  # mean pooling
            all_logits.append(out.logits.float().cpu())
            all_emb.append(nn.functional.normalize(emb, dim=-1).cpu())
        return torch.cat(all_logits), torch.cat(all_emb)

    def score(self, texts: list[str]) -> dict:
        """Return closed-set prediction and all open-set scores for each text."""
        t0 = time.time()
        logits, emb = self._forward(texts)
        infer_s = time.time() - t0
        out = self.scorer.score(logits, emb)
        out["pred"] = self.classes_[logits.argmax(-1).numpy()]
        out["ms_per_flow"] = 1000.0 * infer_s / max(len(texts), 1)
        return out
