# Zero-day intrusion detection for IoT: leave-one-attack-out evaluation across networks

Code and results for the article *Fine-Tuned Language Encoders for Zero-Day IoT Intrusion Detection: A Cross-Network Leave-One-Attack-Out Benchmark With Label-Free Calibration* by Kurniabudi and Eko Arip Winanto (Universitas Dinamika Bangsa, Jambi, Indonesia), submitted to IEEE Access (revised version, v0.2.0).

The repository evaluates whether language-model detectors help detect previously unseen attack families in IoT traffic. Every attack family is withheld from training in turn, within one network and across four networks that share the NetFlow v3 feature schema (NF-ToN-IoT-v3, NF-BoT-IoT-v3, NF-UNSW-NB15-v3, NF-CICIDS2018-v3), and detection thresholds are set on unlabeled traffic of the deployment network so that all detectors are compared at the same false-alarm budget.

## What is included

| Folder | Content |
|---|---|
| `loao/` | library: data preparation, harmonized taxonomy, split protocols, threshold calibration, detectors, novelty scores, metrics |
| `scripts/` | experiment runners, comparison and statistics scripts |
| `tests/` | unit tests on synthetic data (leakage guards, de-duplication, calibration, scores) |
| `configs/` | dataset definitions and the harmonized attack taxonomy |
| `splits/` | split manifests on NF-ToN-IoT-v3 and NF-BoT-IoT-v3 for seeds 0–2 (with SHA-256 of the processed data they refer to) |
| `splits4/` | four-network split manifests (21 P1 and 24 P3 family-level splits per seed) |
| `results/` | per-split result tables for every detector, score and threshold rule, and analysis reports; `results/revision/` and `results/e11/` hold the experiments added in the revision |

Not included: the datasets (download them yourself, see `data/README.md`), per-flow score dumps (large; available on request), and the manuscript.

## Protocols

| ID | Train | Test | Unknown |
|---|---|---|---|
| P1 | network A without attack unit *k* | A | *k* |
| P2 | network A, all units | network B, units known in A | none (closed-set transfer) |
| P3 | network A without unit *k* | network B | *k* |
| P3-open | network A without unit *k* | network B, all units | every unit absent from A |

A unit is an attack family (far-from-distribution) or a subfamily (near-distribution). Threshold rules: nested pseudo-unknown Youden, a benign false-alarm budget on source validation data, and the proposed **target warm-up budget** on an unlabeled window of target traffic (`loao/calibration.py`, `loao/adaptation.py`).

## Detectors and scores

Random forest (MSP), LightGBM, MLP, and transformer encoders fine-tuned on serialized flows (DistilBERT, SecBERT, and a small transformer trained from scratch), each with MSP, energy, k-nearest-neighbor and Mahalanobis novelty scores (`loao/openset.py`); benign-only Isolation Forest and autoencoder (`scripts/run_anomaly.py`); LightGBM with an energy score, k-NN on raw features, ReAct, CORAL alignment, and a two-stage detector with an autoencoder gate (`scripts/run_baselines_extra.py`, `scripts/run_revision_rf.py`). Serialization controls: random forest and MLP on the same 5-level discretized features the encoders read (`--discretize 5`), and SecBERT on raw-value text (`--scheme kv`).

## Installation

Python 3.10 or newer (developed with 3.14).

```bash
git clone https://github.com/robotumbel/iot-zeroday-loao.git
cd iot-zeroday-loao
pip install -r requirements.txt
```

```bash
python -m unittest discover -s tests -v
```

## Reproducing the experiments

1. Download NF-ToN-IoT-v3, NF-BoT-IoT-v3, NF-UNSW-NB15-v3, and NF-CICIDS2018-v3 (University of Queensland, non-commercial licence) into `data/raw/` as described in `data/README.md`.
2. Prepare the data (two-pass capped sampling, identifier removal, de-duplication, partitions):

```bash
python -m loao.cli prepare --datasets nf_ton_iot_v3 nf_bot_iot_v3 --cap 20000 --seed 0
```

3. Build split manifests:

```bash
python -m loao.cli splits --processed "data/processed/*cap20000__seed0.parquet" --protocols P1 P2 P3 --level family --seed 0
```

4. Random forest baseline:

```bash
python scripts/run_baseline_rf.py --splits splits/family_seed0 --only P1__ P3__ --norm none --contamination 0 0.05 --n-estimators 100 --seed 0 --out results/rf_msp_full_family_seed0.csv
```

5. MLP and transformer encoders for seeds 0–2 (a 6 GB GPU is enough; DistilBERT and SecBERT weights are downloaded from Hugging Face):

```bash
bash scripts/run_all_seeds.sh
```

6. Statistical comparison over seeds (Friedman + Nemenyi, planned Wilcoxon tests with Holm correction):

```bash
python scripts/stats_tests.py --metric auroc_ood --out results/stats_auroc.md
```

7. Four networks: prepare `nf_unsw_nb15_v3` and `nf_cicids2018_v3` in the same way, then build `splits4/` and run every detector on the new splits:

```bash
bash scripts/run_e11_cpu.sh      # splits4 and all CPU detectors
bash scripts/gpu_queue_e11.sh 0  # encoders (GPU)
python scripts/stats_e11.py       # summary and Friedman/Nemenyi over 11 detectors
```

8. Revision experiments (chronological partitions, P3-open, robust and time-ordered windows, total-alert rule and gate, de-duplication sensitivity, missing-value token, training length): `scripts/run_revision_cpu_batch1.sh`, `run_revision_cpu_batch2.sh`, `gpu_queue_revision.sh`, then `scripts/aggregate_revision.py`, `scripts/stats_clustered.py`, and `scripts/analyze_e9_e14.py`.

Processed data must be regenerated with the same seed before rerunning a split; `load_split` refuses data whose hash differs from the manifest.

## Results

- `results/paper_table6.md` (`.csv`): every detector with its pre-specified score at a 1% warm-up budget (Table 6 of the article; `scripts/paper_tables.py`).
- `results/stats_auroc_3seeds.md`, `stats_recall_far1_3seeds.md`, `stats_recall_far5_3seeds.md`, `stats_totalfa_far1_3seeds.md`: Friedman + Nemenyi on the pre-specified scores and 17 planned Wilcoxon tests with Holm correction and rank-biserial effect sizes (`scripts/stats_tests.py`).
- `results/rfcal_3seeds_summary.md`: random forest under every threshold rule (raw rows in `rfcal_*_seed{0,1,2}.csv`).
- `results/tierb_summary.md` (`scripts/aggregate_tierb.py`): warm-up window size and contamination source (`rf_windows_*`), time-ordered warm-up windows (`rf_temporal_*`), de-duplication sensitivity (`rf_dedupnone_*`, `rf_dedupmajority_*`), benign-only anomaly detectors and LightGBM (`anomaly_*`).
- `results/collision_stats.md` (`scripts/collision_stats.py`): label collisions in the full NF-v3 files and near-duplicate analysis.
- `results/e11_summary.md`: four-network benchmark (21 P1 and 24 P3 splits, 11 detectors, Friedman/Nemenyi).
- `results/revision_summary.md`, `results/revision_tables.md`: revision experiments; `results/stats_clustered.md`: per-dataset signs and dataset-balanced bootstrap intervals; `results/e9_e14_summary.md`: encoder training length and the explicit missing-value token.
- Earlier seed-0 reports (`p1_sanity_check_*`, `p2_p3_cross_dataset_*`, `adaptation_p2_p3_*`, `l1_encoders_*`) are kept for traceability.

Main findings (three seeds, four networks):

1. Within a network, fine-tuned DistilBERT/SecBERT encoders did not beat classical detectors: on two networks AUROC-OOD 0.85-0.86 versus 0.88 (random forest) and 0.90 (MLP, Mahalanobis); on four networks they rank 6th and 7th of 11 detectors, below the MLP, random forest, and a label-free k-NN on raw features. At a 1% budget they recovered fewer zero-day flows than the random forest. The text serialization, missing-value handling, training length (up to six epochs), and domain pretraining do not explain the gap.
2. Across networks, every detector was weak (AUROC-OOD 0.44-0.54 over 24 splits, no detectable difference).
3. Setting the threshold on an unlabeled warm-up window of target traffic lowered benign rejections on a new network from about 66% to about 1%. Drift after the window raises benign rejections (about 5% with time-ordered windows across networks, about 20% with chronological partitions); known attacks in the window are harmless, but the zero-day family itself in the window suppresses its own detection, which the median of several window thresholds mitigates.
4. The budget bounds novelty rejections only: supervised detectors still raise 11-68% of benign flows as alerts, mostly as known attacks. A benign-only autoencoder keeps all alerts near 1%; used as a gate it bounds alerts but passes most known attacks.
5. Duplicate feature vectors with conflicting labels are common in NF-ToN-IoT-v3 (49% of rows; mostly scanning) and NF-CICIDS2018-v3 (26.5%; mostly infiltration), consistent with labels that depend on the hosts involved; results depend on how they are handled.

## Citation

See `CITATION.cff`. Please also cite the four NF-v3 datasets as requested by their publishers.

## Licence

Code: MIT (see `LICENSE`). The datasets keep their own licences.

## AI assistance

Parts of the code were written with the help of an AI assistant (Claude, Anthropic) under the authors' specifications and review; see the article's acknowledgment for the full disclosure.
