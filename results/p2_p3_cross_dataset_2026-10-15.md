# Fixed benign false-alarm threshold + P2/P3 cross-dataset — RF + MSP (2026-10-15)

Setup: NF-ToN-IoT-v3 and NF-BoT-IoT-v3, cap 20,000 rows per raw label, de-duplicated, 47 shared NetFlow v3 features, seed 0, Random Forest with 100 trees, unknown score = 1 − max class probability (MSP). One seed and one baseline, so these are pipeline findings, not paper results.

Full tables: `results/rf_msp_family_seed0.csv`, `results/rf_msp_subfamily_seed0.csv` (one row per split × threshold rule; P1 rows replace the earlier sanity-check CSVs).

## 1. New threshold rule

`loao/calibration.py`, source data only:

| Rule | How the threshold is set |
|---|---|
| `pseudo_youden` | nested pseudo-unknown folds, Youden-J point, averaged (previous rule) |
| `benign_far0.01` / `benign_far0.05` | smallest threshold that flags at most 1% / 5% of benign validation flows as UNKNOWN (strict `>` so MSP ties at 0 cannot break the budget) |

The benign false alarm is now reported in two parts: `benign_rejected_as_unknown` (caused by the threshold) and `benign_as_known_attack` (closed-set confusion, which no threshold can fix).

## 2. Within-dataset (P1): the budget holds

Family level, mean over 10 splits:

| Rule | AUROC-OOD | Unknown recall | Flagged malicious | Benign → UNKNOWN | Benign → known attack | Open-set macro-F1 |
|---|---|---|---|---|---|---|
| benign FAR 1% | 0.881 | 0.373 | 0.620 | **0.008** | 0.128 | 0.826 |
| benign FAR 5% | 0.881 | 0.640 | 0.790 | **0.043** | 0.120 | 0.862 |
| pseudo Youden | 0.881 | 0.739 | 0.862 | 0.088 | 0.103 | 0.865 |

- The fixed-budget rule does what it promises on test data from the same dataset (0.8% and 4.3% against budgets of 1% and 5%).
- The roughly 12% of benign flows still raised as attacks come from closed-set confusion, mostly benign vs scanning in NF-ToN-IoT-v3 (the duplicate problem found earlier). The earlier "28% false alarm" was about two thirds closed-set confusion.
- The trade-off is clear: a 1% budget halves unknown recall (0.74 → 0.37).

Subfamily level shows the same pattern (benign → UNKNOWN 0.8% / 4.5%).

## 3. Cross-dataset closed-set (P2): transfer collapses

| Train → test | Rule | Benign → UNKNOWN | Benign → known attack | Known macro-F1 |
|---|---|---|---|---|
| BoT → ToN | FAR 1% | 0.353 | 0.298 | 0.190 |
| ToN → BoT | FAR 1% | 0.402 | 0.104 | 0.050 |

Mean over both directions, family level: with a 1% budget set on the source, **37.7% of target benign flows are rejected as unknown**, and known-attack macro-F1 falls from about 0.79 (P1) to 0.03–0.12. The two datasets share an identical feature schema, yet a model from one does not transfer to the other even for the attack types both contain. Same features ≠ same distribution.

## 4. Cross-dataset LOAO (P3)

Family level (unknown = held-out family, tested on the other dataset):

| Train → test | Held out | AUROC-OOD | Unknown recall (FAR 1%) | Benign total FA (FAR 1%) |
|---|---|---|---|---|
| BoT → ToN | FLOOD | 0.628 | 0.462 | 0.440 |
| BoT → ToN | RECON | 0.749 | 0.943 | 0.868 |
| ToN → BoT | FLOOD | 0.898 | 0.774 | 0.443 |
| ToN → BoT | RECON | **0.025** | 0.033 | 0.373 |
| **Mean** | | **0.575** (P1: 0.881) | 0.553 | 0.531 |

- **AUROC drops from 0.88 (P1) to 0.58 (P3).** Subfamily level: 0.85 → 0.54, close to chance.
- **The high "unknown recall" in P3 is misleading.** It comes with 40–90% of benign target traffic also rejected: the detector flags almost everything from the new network as unknown. This is exactly the confound in SiamXBERT-style cross-dataset tests, where unknowns come from the other dataset; our protocol makes it visible because benign and known flows also come from the target.
- **ToN → BoT, RECON held out: AUROC 0.025**, i.e. almost perfectly *inverted*. BoT scanning looks more familiar to the ToN-trained model than BoT benign traffic does. A likely cause is the ToN benign/scanning duplicate problem: the ToN model learned scan-like flows as benign. Needs a check before it goes into a paper.

## 5. What this means for the paper

1. **Report AUROC-OOD together with benign false alarm at a fixed budget.** Unknown recall alone rewards detectors that reject everything after a domain shift.
2. **Source-only calibration does not survive a change of network.** A 1% budget on the source became 38–44% on the target on average (14–87% per split). This motivates a concrete method contribution: **recalibrating the threshold with unlabeled traffic from the target network** (e.g. a short warm-up window assumed to be mostly benign), which is realistic for a new IoT deployment and needs no attack labels. Test it as an extra rule `target_warmup_far`.
3. **Covariate shift must be separated from semantic shift.** P2 shows that even known attacks fail across datasets, so P3 numbers mix both effects. Report P3 − P2 differences, and consider feature normalisation per dataset (rank/quantile transform fitted on each network's own unlabeled traffic) as a baseline.
4. **Only FLOOD and RECON are shared between these two datasets**, so P3 has 4 family-level and 6 subfamily-level splits. CICIoT2023 and Edge-IIoTset in NetFlow v3 form are needed for a meaningful P3 table.

## 6. Caveats

One seed; cap 20,000; 100 trees; one baseline. De-duplication was done within each dataset sample; no target-test row matched a source-train row exactly (0 removed). The ToN RECON / inverted-AUROC result needs a dedicated check (with and without de-duplication, and per-feature drift analysis) before any claim.
