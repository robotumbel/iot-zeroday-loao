# Target warm-up calibration and per-network normalisation — P2/P3, RF + MSP (2026-10-15)

Same setup as `p2_p3_cross_dataset_2026-10-15.md`: NF-ToN-IoT-v3 ↔ NF-BoT-IoT-v3, cap 20,000 per label, 47 NetFlow v3 features, seed 0, Random Forest (100 trees), MSP unknown score. One seed and one baseline.

Full table: `results/adapt_rf_msp_p2p3_seed0.csv` (14 splits × 3 contamination levels × 2 normalisations × 5 threshold rules = 420 rows).

## What was added

| Component | File | Idea |
|---|---|---|
| Unlabeled warm-up window | `loao/adaptation.py::make_warmup` | 2,000 flows from the target network's `val` partition (never the test partition), mostly benign with a set share of attacks (0%, 5%, 20%), drawn from any target unit including the held-out one. Labels only build and describe the window; methods never read them. |
| `target_warmup_far` threshold | `loao/calibration.py` | the 1% / 5% false-alarm budget applied to the warm-up window's scores, as if the window were benign |
| Per-network normalisation | `loao/adaptation.py::NetworkNormalizer` | per-feature rank transform to [0, 1], fitted on each network's own warm-up window (source window from source train+val, target window as above) |

## Main results (contamination 5%)

Family level, means over splits:

| Protocol | Normalisation | Threshold | AUROC-OOD | Unknown recall | Benign → UNKNOWN | Benign → known attack | Known macro-F1 |
|---|---|---|---|---|---|---|---|
| P2 | none | source benign FAR 1% | — | — | 0.377 | 0.201 | 0.120 |
| P2 | none | **target warm-up FAR 1%** | — | — | **0.006** | 0.296 | 0.124 |
| P3 | none | source benign FAR 1% | 0.575 | 0.553 | 0.418 | 0.113 | 0.131 |
| P3 | none | **target warm-up FAR 1%** | 0.575 | 0.070 | **0.008** | 0.186 | 0.156 |
| P3 | none | **target warm-up FAR 5%** | 0.575 | 0.125 | **0.036** | 0.174 | 0.156 |
| P3 | per-network | target warm-up FAR 5% | **0.443** | 0.119 | 0.036 | 0.149 | 0.135 |
| P3 | per-network | source benign FAR 5% | 0.443 | 0.932 | 0.880 | 0.000 | 0.061 |

Subfamily level gives the same picture (P3 AUROC 0.544 without normalisation, 0.518 with it; warm-up FAR 1% → 0.7% of benign rejected).

## Findings

1. **Warm-up calibration fixes the false-alarm budget.** With a 2,000-flow unlabeled window from the new network, the share of target benign traffic rejected as unknown drops from about 38–44% (source-calibrated 1% budget) to 0.2–0.9%, and from about 72–77% to 3.4–5.4% for the 5% budget. The rule is robust to contamination: with 20% attacks in the window it stays at or near budget (at most 1.1% for the 1% rule), mostly becoming more conservative.
2. **It does not create zero-day detection.** Once false alarms are under control, P3 unknown recall falls to 3.5–17% without normalisation (0.6–12% with it). The threshold only picks an operating point; the ranking itself is weak (AUROC 0.54–0.58). The earlier "high P3 unknown recall" was entirely bought with false alarms.
3. **Closed-set confusion remains.** 15–38% of target benign flows are still classified as a known attack, and known-attack macro-F1 stays at 0.07–0.16 (P1: about 0.79). No threshold can fix this; the classifier's decision boundaries themselves do not transfer.
4. **Per-network rank normalisation hurts (negative result).** P3 AUROC drops from 0.575 to 0.443 (family) and 0.544 to 0.518 (subfamily), and known macro-F1 does not improve. A likely reason: rank transforms erase absolute magnitudes (bytes, packets, rates) that separate floods and scans, and the two networks' "normal" traffic differs in composition, so the same rank does not mean the same behaviour. Keep it in the paper as an ablation, not as a method.

## Implications for the paper

- **Operational contribution worth keeping:** a warm-up calibration step that needs no labels and keeps the false-alarm budget on a new network. It is cheap, realistic for IoT deployments, and should be applied to every method in the benchmark, LLM-based or not, so comparisons are made at the same false-alarm rate.
- **Recommended main metric pair for P3:** AUROC-OOD plus unknown recall at a 1% target false-alarm budget (warm-up calibrated). This prevents "reject everything" detectors from looking good.
- **The core gap is representation, not thresholding.** RF on raw NetFlow features ranks unknowns barely above chance across networks. This is precisely the question for the LLM paradigms (RQ1–RQ3): do pretrained text/flow representations transfer better? The RF-MSP numbers above are the baseline they must beat.
- Feature-level adaptation worth trying instead of rank normalisation: log-scaling of volume features, ratio features that are scale-free by design (bytes per packet, in/out ratios, as in SiamXBERT's derived features), and dropping features that encode the capture environment (TTL, TCP window, L7 protocol id) — test with a per-feature drift analysis.

## Caveats

One seed, cap 20,000, 100 trees, one baseline, two datasets sharing only two families (FLOOD, RECON). Warm-up windows are sampled from the target `val` partition, so their benign traffic comes from the same period as the test traffic; a time-ordered split (warm-up strictly before test) would be stricter and needs flow timestamps, which are currently dropped as identifiers.
