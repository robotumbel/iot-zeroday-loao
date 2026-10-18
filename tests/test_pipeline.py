"""Smoke and invariant tests on synthetic data. Run: python -m unittest discover -s tests -v"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from loao.adaptation import NetworkNormalizer, make_warmup  # noqa: E402
from loao.calibration import benign_far, pseudo_youden, target_warmup_far  # noqa: E402
from loao.data import feature_columns, prepare_dataset  # noqa: E402
from loao.metrics import fpr_at_tpr, open_set_report, threshold_free  # noqa: E402
from loao.openset import OpenSetScorer  # noqa: E402
from loao.tabular import MLPConfig, MLPDetector  # noqa: E402
from loao.serialize import FlowSerializer  # noqa: E402
from loao.splits import build_split, enumerate_specs, load_split, write_manifests  # noqa: E402
from loao.taxonomy import Taxonomy, normalize_label  # noqa: E402


class PipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        subprocess.run([sys.executable, str(ROOT / "scripts/make_synthetic.py"), "--n", "200",
                        "--out", str(cls.tmp / "synthetic")], check=True, capture_output=True)
        cfgs = json.loads((ROOT / "configs/datasets.json").read_text(encoding="utf-8"))
        cls.tax = Taxonomy(ROOT / "configs/taxonomy.json")
        cls.paths, cls.data, cls.spaces = {}, {}, {}
        for name, folder in [("nf_ton_iot_v3", "NF-ToN-IoT-v3"), ("nf_bot_iot_v3", "NF-BoT-IoT-v3")]:
            cfg = dict(cfgs[name], files=[f"synthetic/{folder}/*.csv"])
            p = prepare_dataset(name, cfg, cls.tax, cls.tmp, cls.tmp / "processed", max_per_label=150, seed=0)
            cls.paths[name] = p
            cls.data[name] = pd.read_parquet(p)
            cls.spaces[name] = cfg["feature_space"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_normalize(self):
        self.assertEqual(normalize_label("DDoS-ICMP_Flood"), "ddosicmpflood")

    def test_unmapped_label_raises(self):
        with self.assertRaises(KeyError):
            self.tax.map_labels(pd.Series(["Benign", "totally_new_attack"]), "ton_iot")

    def test_identifiers_dropped_and_cap(self):
        df = self.data["nf_ton_iot_v3"]
        for c in ["IPV4_SRC_ADDR", "IPV4_DST_ADDR", "L4_SRC_PORT", "FLOW_START_MILLISECONDS", "Label"]:
            self.assertNotIn(c, df.columns)
        self.assertLessEqual(df["label_norm"].value_counts().max(), 150)

    def test_dedup_removed_conflicts(self):
        stats = json.loads(self.paths["nf_ton_iot_v3"].with_suffix(".stats.json").read_text())
        self.assertGreater(stats["dropped_conflicting_label_rows"], 0)
        df = self.data["nf_ton_iot_v3"]
        self.assertFalse(pd.util.hash_pandas_object(df[feature_columns(df)], index=False).duplicated().any())

    def test_p1_holdout_absent_from_training(self):
        specs = enumerate_specs(self.data, self.spaces, ["P1"], "family", 0, min_unit_rows=10)
        self.assertTrue(specs)
        for spec in specs:
            s = build_split(spec, self.data, min_unit_rows=10)
            self.assertNotIn(spec.holdout, set(s.train["family"]))
            self.assertNotIn(spec.holdout, set(s.val["family"]))
            self.assertGreater(s.y_test_unknown.sum(), 0)
            self.assertTrue(set(s.train["row_id"]).isdisjoint(s.test["row_id"]))
            for j in s.pseudo_unknown_units:
                tr, cin, cout = s.calibration_fold(j)
                self.assertNotIn(spec.holdout, set(tr["family"]) | set(cin["family"]) | set(cout["family"]))
                self.assertEqual(set(cout["family"]), {j})

    def test_p3_cross_dataset_units(self):
        specs = enumerate_specs(self.data, self.spaces, ["P3"], "family", 0, min_unit_rows=10)
        holdouts = {(s.source, s.holdout) for s in specs}
        # FLOOD and RECON exist in both synthetic datasets.
        self.assertIn(("nf_ton_iot_v3", "FLOOD"), holdouts)
        self.assertIn(("nf_bot_iot_v3", "RECON"), holdouts)
        for spec in specs:
            s = build_split(spec, self.data, min_unit_rows=10)
            allowed = set(s.known_units) | {"BENIGN", spec.holdout}
            self.assertTrue(set(s.test["family"]) <= allowed)

    def test_subfamily_near_ood(self):
        spec = [s for s in enumerate_specs(self.data, self.spaces, ["P1"], "subfamily", 0, 10)
                if s.source == "nf_ton_iot_v3" and s.holdout == "DOS"][0]
        s = build_split(spec, self.data, 10)
        self.assertIn("DDOS", set(s.train["subfamily"]))  # sibling stays known: near-OOD
        self.assertNotIn("DOS", set(s.train["subfamily"]))

    def test_manifest_roundtrip(self):
        specs = enumerate_specs(self.data, self.spaces, ["P1", "P2", "P3"], "family", 0, 10)
        out = self.tmp / "splits"
        idx = write_manifests(specs, self.data, self.paths, out, 10)
        sid = idx.loc[idx["status"] == "ok", "split_id"].iloc[0]
        s = load_split(out / f"{sid}.json", 10)
        self.assertEqual(s.spec.split_id, sid)

    def test_metrics(self):
        y = np.array([0, 0, 0, 1, 1])
        self.assertAlmostEqual(threshold_free(y, np.array([.1, .2, .3, .8, .9]))["auroc_ood"], 1.0)
        self.assertAlmostEqual(fpr_at_tpr(y, np.array([.1, .2, .9, .8, .95])), 1 / 3)
        rep = open_set_report(["BENIGN", "FLOOD", "WEB", "WEB"], ["BENIGN", "FLOOD", "UNKNOWN", "FLOOD"], "WEB")
        self.assertEqual(rep["unknown_recall"], 0.5)
        self.assertEqual(rep["unknown_flagged_malicious"], 1.0)
        self.assertEqual(rep["benign_false_alarm_rate"], 0.0)

    def test_benign_far_budget(self):
        rng = np.random.default_rng(0)
        s = rng.random(1000)
        for far in (0.01, 0.05):
            th = benign_far(s, far)
            self.assertLessEqual(th.flags(s).mean(), far)
        ties = np.r_[np.zeros(900), rng.random(100)]  # MSP-like: many exact zeros
        self.assertLessEqual(benign_far(ties, 0.05).flags(ties).mean(), 0.05)
        th = pseudo_youden([(np.zeros(50), np.ones(50))])
        self.assertTrue(th.flags(np.array([1.0]))[0] and not th.flags(np.array([0.0]))[0])

    def test_warmup_and_normalizer(self):
        spec = [s for s in enumerate_specs(self.data, self.spaces, ["P3"], "family", 0, 10)][0]
        s = build_split(spec, self.data, 10)
        self.assertTrue(set(s.target_pool["row_id"]).isdisjoint(s.test["row_id"]))
        self.assertTrue(set(s.target_pool["family"]) <= set(s.known_units) | {"BENIGN", spec.holdout})
        w, info = make_warmup(s.target_pool, "family", 20, 0.1, 0)
        self.assertEqual(info["warmup_size"], 20)
        self.assertAlmostEqual(info["warmup_contamination"], 0.1)
        self.assertEqual((w["family"] != "BENIGN").sum(), 2)
        _, big = make_warmup(s.target_pool, "family", 10_000, 0.1, 0)  # benign runs short
        self.assertLess(big["warmup_size"], 10_000)
        self.assertAlmostEqual(big["warmup_contamination"], 0.1, delta=0.02)  # rounding on tiny pools
        norm = NetworkNormalizer().fit(w)
        z = norm.transform(s.test)
        self.assertTrue(((z[norm.features].min().min() >= 0) and (z[norm.features].max().max() <= 1)))
        self.assertEqual(target_warmup_far(np.arange(100.0), 0.05).rule, "target_warmup_far0.05")

    def test_openset_scorer(self):
        import torch
        rng = np.random.default_rng(0)
        a = rng.normal([3, 0, 0], 0.3, (200, 3))
        b = rng.normal([0, 3, 0], 0.3, (200, 3))
        bank = torch.nn.functional.normalize(torch.tensor(np.r_[a, b], dtype=torch.float32), dim=-1)
        sc = OpenSetScorer(k=5).fit(bank, np.r_[np.zeros(200), np.ones(200)])
        q = torch.nn.functional.normalize(torch.tensor([[3, 0, 0], [0, 0, 3]], dtype=torch.float32), dim=-1)
        out = sc.score(torch.tensor([[5.0, 0.0], [0.1, 0.0]]), q)
        for k in ("msp", "energy", "knn", "maha"):
            self.assertLess(out[k][0], out[k][1], k)  # in-distribution scores lower than far-away point

    def test_mlp_detector(self):
        df = self.data["nf_ton_iot_v3"]
        tr = df[df["part"] == "train"]
        feats = feature_columns(df)
        det = MLPDetector(MLPConfig(epochs=3)).fit(tr, feats, tr["family"].to_numpy())
        out = det.score(df[df["part"] == "test"])
        self.assertEqual(len(out["maha"]), (df["part"] == "test").sum())
        self.assertTrue(np.isfinite(out["knn"]).all() and np.isfinite(out["maha"]).all())

    def test_serializer(self):
        df = self.data["nf_ton_iot_v3"]
        feats = feature_columns(df)
        for scheme in ["kv", "binned", "sentence"]:
            ser = FlowSerializer(scheme).fit(df[feats])
            txt = ser.transform(df[feats].head(2))
            self.assertEqual(len(txt), 2)
            self.assertIn("IN_BYTES" if scheme != "sentence" else "in bytes", txt[0])


if __name__ == "__main__":
    unittest.main()
