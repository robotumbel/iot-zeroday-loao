# P1 sanity check — RF + MSP on NF-ToN-IoT-v3 and NF-BoT-IoT-v3 (2026-10-15)

Goal: confirm the pipeline runs on real data and gives plausible numbers. This is **not** a paper result: one seed, at most 20,000 rows per raw label, 100 trees, one baseline.

## Data

| | NF-ToN-IoT-v3 | NF-BoT-IoT-v3 |
|---|---|---|
| Source | UQ RDM, doi 10.48610/44d7c5e (SHA-1 verified) | UQ RDM, UQ:73c4ebc (SHA-1 verified) |
| Full file | 5.3 GB CSV, 27.5 M flows | 3.8 GB CSV, 16.9 M flows |
| Sampled (cap 20k per label) | 169,984 | 81,615 |
| Same-label duplicates dropped | 35,551 | 14,141 |
| **Rows dropped: identical features, different labels** | **40,070 (23.6%)** | 5,683 (7.0%) |
| Kept | 94,363 | 61,791 |
| Features after dropping identifiers | 47 | 47 |

Dropped columns: IPs, source port, flow start/end timestamps, `DNS_QUERY_ID`, binary `Label`. BoT-IoT has `inf` and NaN in `SRC_TO_DST_SECOND_BYTES` and `DST_TO_SRC_SECOND_BYTES` (zero-duration flows); `inf` is now stored as missing (8,677 rows).

**Data-quality finding (worth a paragraph in the paper).** In the first 3 M rows of NF-ToN-IoT-v3, 66.5% of rows belong to feature vectors that appear with both `Benign` and `scanning` labels. Once identifiers and timestamps are removed, many scanning flows are byte-identical to benign flows. NF-ToN-IoT-v3 DDoS shrank from 20,000 sampled rows to 3,112 after removing duplicates. Results on these datasets without de-duplication are inflated.

## Results (P1, threshold calibrated with nested pseudo-unknown folds)

### Family level (far-OOD)

| Dataset | Held out | AUROC-OOD | FPR@95TPR | Unknown recall | Unknown flagged malicious | Benign false alarm | Open-set macro-F1 |
|---|---|---|---|---|---|---|---|
| BoT | FLOOD | 0.991 | 0.018 | 1.000 | 1.000 | 0.098 | 0.960 |
| BoT | RECON | 0.877 | 1.000 | 0.745 | 0.745 | 0.026 | 0.904 |
| BoT | THEFT | 0.996 | 0.011 | 0.989 | 1.000 | 0.047 | 0.869 |
| ToN | BACKDOOR | 0.999 | 0.001 | 0.998 | 1.000 | 0.287 | 0.846 |
| ToN | BRUTEFORCE | 0.810 | 1.000 | 0.265 | 0.925 | 0.256 | 0.817 |
| ToN | FLOOD | 0.868 | 1.000 | 0.808 | 0.993 | 0.282 | 0.885 |
| ToN | MITM_SPOOF | 0.958 | 0.124 | 0.929 | 0.997 | 0.289 | 0.857 |
| ToN | RANSOMWARE | 0.963 | 0.236 | 0.851 | 1.000 | 0.278 | 0.834 |
| ToN | RECON | **0.428** | 1.000 | 0.068 | **0.069** | 0.060 | 0.814 |
| ToN | WEB | 0.917 | 1.000 | 0.734 | 0.894 | 0.288 | 0.859 |
| **Mean** | | 0.881 | 0.539 | 0.739 | 0.862 | 0.191 | 0.865 |

### Subfamily level (near-OOD), selected rows

| Dataset | Held out | AUROC-OOD | Unknown recall | Unknown flagged malicious |
|---|---|---|---|---|
| BoT | DOS (DDoS still known) | 0.561 | 0.012 | 1.000 |
| BoT | DDOS (DoS still known) | 0.617 | 0.120 | 1.000 |
| ToN | DDOS (DoS still known) | 0.988 | 0.984 | 0.997 |
| ToN | SCAN | 0.438 | 0.067 | 0.067 |
| **Mean (13 splits)** | | 0.845 | 0.646 | 0.896 |

Full tables: the P1 rows with `calibration = pseudo_youden` in `results/rf_msp_family_seed0.csv` and `results/rf_msp_subfamily_seed0.csv` (re-run on 2026-10-15 with identical splits; the threshold rules are compared in `results/p2_p3_cross_dataset_2026-10-15.md`).

## Reading

1. **The pipeline works on real data**, and the numbers vary a lot by held-out family. That variance is the point of LOAO: a single "zero-day accuracy" figure hides it.
2. **Near-OOD vs far-OOD shows up as expected.** On BoT-IoT, holding out DoS while DDoS stays known drops AUROC to about 0.56–0.62: the detector cannot say "this is new", but it still raises 100% of those flows as malicious (it calls them DDoS). Reporting both "unknown recall" and "flagged malicious" captures this.
3. **ToN-IoT scanning is a hard case.** With RECON held out, AUROC is 0.43 and only 6.9% of scanning flows are flagged as anything other than benign, which matches the benign/scanning duplicate finding above. This is a dataset problem as much as a model problem.
4. **Benign false alarms on ToN-IoT are high (about 28%).** The pseudo-unknown Youden threshold is aggressive. Calibration should target a fixed benign false-alarm budget (e.g. 1–5%) as a second operating point.
5. **FPR@95TPR = 1.0 in several rows** comes from MSP ties: Random Forest gives probability 1.0 to many unknown flows, so their score is exactly 0. This is a known MSP weakness and a reason to test energy/distance scores and LLM embeddings.

## Next steps suggested by this run

- Add a second threshold rule: fixed false-alarm rate on benign validation flows.
- Run 5 seeds and the full cap (50k) once more baselines exist.
- Check how much the benign/scanning collision drives results: run ToN RECON again with and without de-duplication.
- Start P2/P3 between the two NF-v3 datasets (same 47-feature space); only FLOOD and RECON are shared families.
