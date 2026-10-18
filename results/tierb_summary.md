# Tier-B experiments (seeds 0-2)

## 1. Warm-up window size (contamination 5%, any target unit), RF full

```
protocol           calibration  warmup_requested benign_rejected_as_unknown unknown_recall  n_seeds
      P1 target_warmup_far0.01               250              0.011 ± 0.003  0.352 ± 0.014        3
      P1 target_warmup_far0.01               500              0.009 ± 0.002  0.332 ± 0.063        3
      P1 target_warmup_far0.01              1000              0.010 ± 0.004  0.336 ± 0.077        3
      P1 target_warmup_far0.01              2000              0.009 ± 0.003  0.332 ± 0.039        3
      P1 target_warmup_far0.05               250              0.046 ± 0.001  0.637 ± 0.010        3
      P1 target_warmup_far0.05               500              0.039 ± 0.007  0.623 ± 0.032        3
      P1 target_warmup_far0.05              1000              0.042 ± 0.008  0.630 ± 0.032        3
      P1 target_warmup_far0.05              2000              0.041 ± 0.003  0.637 ± 0.014        3
      P3 target_warmup_far0.01               250              0.008 ± 0.005  0.029 ± 0.028        3
      P3 target_warmup_far0.01               500              0.005 ± 0.001  0.036 ± 0.015        3
      P3 target_warmup_far0.01              1000              0.007 ± 0.003  0.037 ± 0.015        3
      P3 target_warmup_far0.01              2000              0.006 ± 0.002  0.046 ± 0.025        3
      P3 target_warmup_far0.05               250              0.034 ± 0.009  0.119 ± 0.018        3
      P3 target_warmup_far0.05               500              0.038 ± 0.007  0.113 ± 0.000        3
      P3 target_warmup_far0.05              1000              0.034 ± 0.005  0.119 ± 0.005        3
      P3 target_warmup_far0.05              2000              0.035 ± 0.004  0.116 ± 0.007        3
```

## 1b. Contamination source (window 2,000 flows), RF full

```
protocol           calibration warmup_attack_source    c unknown_recall benign_rejected_as_unknown warmup_holdout_share  n_seeds
      P1 target_warmup_far0.01                  all 0.05  0.332 ± 0.039              0.009 ± 0.003        0.010 ± 0.000        3
      P1 target_warmup_far0.01                  all 0.20  0.228 ± 0.055              0.007 ± 0.002        0.040 ± 0.000        3
      P1 target_warmup_far0.01              holdout 0.05  0.106 ± 0.032              0.004 ± 0.001        0.050 ± 0.000        3
      P1 target_warmup_far0.01              holdout 0.20  0.030 ± 0.002              0.003 ± 0.001        0.200 ± 0.000        3
      P1 target_warmup_far0.01                known 0.05  0.404 ± 0.050              0.011 ± 0.003        0.000 ± 0.000        3
      P1 target_warmup_far0.01                known 0.20  0.399 ± 0.059              0.011 ± 0.002        0.000 ± 0.000        3
      P1 target_warmup_far0.05                  all 0.05  0.637 ± 0.014              0.041 ± 0.003        0.010 ± 0.000        3
      P1 target_warmup_far0.05                  all 0.20  0.547 ± 0.024              0.033 ± 0.006        0.040 ± 0.000        3
      P1 target_warmup_far0.05              holdout 0.05  0.515 ± 0.029              0.024 ± 0.003        0.050 ± 0.000        3
      P1 target_warmup_far0.05              holdout 0.20  0.176 ± 0.017              0.012 ± 0.002        0.200 ± 0.000        3
      P1 target_warmup_far0.05                known 0.05  0.654 ± 0.010              0.047 ± 0.003        0.000 ± 0.000        3
      P1 target_warmup_far0.05                known 0.20  0.650 ± 0.017              0.047 ± 0.005        0.000 ± 0.000        3
      P3 target_warmup_far0.01                  all 0.05  0.046 ± 0.025              0.006 ± 0.002        0.025 ± 0.000        3
      P3 target_warmup_far0.01                  all 0.20  0.010 ± 0.009              0.005 ± 0.000        0.100 ± 0.000        3
      P3 target_warmup_far0.01              holdout 0.05  0.029 ± 0.015              0.007 ± 0.002        0.050 ± 0.000        3
      P3 target_warmup_far0.01              holdout 0.20  0.011 ± 0.009              0.006 ± 0.001        0.200 ± 0.000        3
      P3 target_warmup_far0.01                known 0.05  0.096 ± 0.013              0.008 ± 0.001        0.000 ± 0.000        3
      P3 target_warmup_far0.01                known 0.20  0.094 ± 0.015              0.006 ± 0.001        0.000 ± 0.000        3
      P3 target_warmup_far0.05                  all 0.05  0.116 ± 0.007              0.035 ± 0.004        0.025 ± 0.000        3
      P3 target_warmup_far0.05                  all 0.20  0.076 ± 0.047              0.028 ± 0.004        0.100 ± 0.000        3
      P3 target_warmup_far0.05              holdout 0.05  0.117 ± 0.007              0.037 ± 0.002        0.050 ± 0.000        3
      P3 target_warmup_far0.05              holdout 0.20  0.061 ± 0.035              0.035 ± 0.003        0.200 ± 0.000        3
      P3 target_warmup_far0.05                known 0.05  0.118 ± 0.008              0.040 ± 0.004        0.000 ± 0.000        3
      P3 target_warmup_far0.05                known 0.20  0.117 ± 0.007              0.038 ± 0.004        0.000 ± 0.000        3
```

## 2. Time-ordered warm-up (window from the earliest 30% of target traffic, test on the rest)

```
protocol           calibration benign_rejected_as_unknown unknown_recall benign_false_alarm_rate  n_seeds
      P1        benign_far0.01              0.012 ± 0.002  0.470 ± 0.068           0.032 ± 0.001        3
      P1        benign_far0.05              0.031 ± 0.003  0.768 ± 0.013           0.048 ± 0.004        3
      P1 target_warmup_far0.01              0.011 ± 0.002  0.449 ± 0.041           0.032 ± 0.001        3
      P1 target_warmup_far0.05              0.028 ± 0.002  0.715 ± 0.030           0.046 ± 0.004        3
      P3        benign_far0.01              0.562 ± 0.072  0.548 ± 0.016           0.614 ± 0.060        3
      P3        benign_far0.05              0.840 ± 0.044  0.716 ± 0.006           0.857 ± 0.041        3
      P3 target_warmup_far0.01              0.047 ± 0.045  0.097 ± 0.019           0.174 ± 0.043        3
      P3 target_warmup_far0.05              0.119 ± 0.110  0.128 ± 0.026           0.231 ± 0.102        3
```

Random (exchangeable) windows, same detector, for comparison:

```
protocol           calibration benign_rejected_as_unknown unknown_recall benign_false_alarm_rate  n_seeds
      P1        benign_far0.01              0.011 ± 0.003  0.399 ± 0.058           0.135 ± 0.003        3
      P1        benign_far0.05              0.047 ± 0.003  0.653 ± 0.013           0.164 ± 0.004        3
      P1 target_warmup_far0.01              0.009 ± 0.003  0.332 ± 0.039           0.134 ± 0.002        3
      P1 target_warmup_far0.05              0.041 ± 0.003  0.637 ± 0.014           0.159 ± 0.003        3
      P3        benign_far0.01              0.470 ± 0.052  0.544 ± 0.014           0.575 ± 0.048        3
      P3        benign_far0.05              0.773 ± 0.069  0.723 ± 0.007           0.827 ± 0.067        3
      P3 target_warmup_far0.01              0.006 ± 0.002  0.046 ± 0.025           0.178 ± 0.020        3
      P3 target_warmup_far0.05              0.035 ± 0.004  0.116 ± 0.007           0.197 ± 0.018        3
```

## 3. De-duplication = none (RF full, warm-up 1%, clean window)

```
protocol     auroc_ood unknown_recall benign_false_alarm_rate  n_seeds
      P1 0.805 ± 0.005  0.304 ± 0.005           0.138 ± 0.001        3
      P3 0.511 ± 0.026  0.043 ± 0.032           0.209 ± 0.014        3
```
- ToN RECON (P1) without de-duplication: AUROC 0.385 ± 0.004

## 3. De-duplication = majority (RF full, warm-up 1%, clean window)

```
protocol     auroc_ood unknown_recall benign_false_alarm_rate  n_seeds
      P1 0.875 ± 0.003  0.429 ± 0.066           0.132 ± 0.002        3
      P3 0.596 ± 0.030  0.068 ± 0.044           0.191 ± 0.007        3
```

Default (conflicting vectors removed), same detector and rule:

```
protocol     auroc_ood unknown_recall benign_false_alarm_rate  n_seeds
      P1 0.880 ± 0.006  0.408 ± 0.049           0.135 ± 0.002        3
      P3 0.581 ± 0.026  0.094 ± 0.013           0.178 ± 0.019        3
```

## 4. Benign-only anomaly detectors and LightGBM (warm-up 1%, clean window)

```
protocol   method     auroc_ood auroc_unknown_vs_benign unknown_recall benign_rejected_as_unknown   ms_per_flow  n_seeds
      P1       ae 0.596 ± 0.010           0.898 ± 0.002  0.318 ± 0.030              0.008 ± 0.001 0.003 ± 0.000        3
      P1  iforest 0.614 ± 0.002           0.840 ± 0.006  0.204 ± 0.009              0.010 ± 0.001 0.019 ± 0.001        3
      P1 lightgbm 0.774 ± 0.005           0.717 ± 0.005  0.082 ± 0.037              0.012 ± 0.000 0.011 ± 0.001        3
      P3       ae 0.484 ± 0.006           0.499 ± 0.018  0.014 ± 0.007              0.010 ± 0.004 0.003 ± 0.000        3
      P3  iforest 0.497 ± 0.002           0.537 ± 0.003  0.003 ± 0.003              0.008 ± 0.000 0.018 ± 0.000        3
      P3 lightgbm 0.468 ± 0.024           0.449 ± 0.014  0.014 ± 0.014              0.013 ± 0.001 0.009 ± 0.000        3
```

RF full, AUROC of the held-out unit against benign flows:

```
protocol auroc_unknown_vs_benign  n_seeds
      P1           0.878 ± 0.004        3
      P3           0.527 ± 0.052        3
```

Neural detectors, AUROC of the held-out unit against benign flows (from stored scores):

```
protocol                method score auroc_unknown_vs_benign  n_seeds
      P1 L1-distilbert_cap2000   knn           0.848 ± 0.003        3
      P1 L1-distilbert_cap2000  maha           0.865 ± 0.003        3
      P1 L1-secbert-kv_cap2000   knn           0.848 ± 0.009        3
      P1 L1-secbert-kv_cap2000  maha           0.851 ± 0.009        3
      P1    L1-secbert_cap2000   knn           0.834 ± 0.012        3
      P1    L1-secbert_cap2000  maha           0.848 ± 0.005        3
      P1 L1-tiny-local_cap2000   knn           0.846 ± 0.014        3
      P1 L1-tiny-local_cap2000  maha           0.821 ± 0.007        3
      P1      MLP-bin5_cap2000   knn           0.862 ± 0.003        3
      P1      MLP-bin5_cap2000  maha           0.872 ± 0.008        3
      P1              MLP_cap0   knn           0.890 ± 0.003        3
      P1              MLP_cap0  maha           0.876 ± 0.005        3
      P1           MLP_cap2000   knn           0.888 ± 0.009        3
      P1           MLP_cap2000  maha           0.880 ± 0.004        3
      P3 L1-distilbert_cap2000   knn           0.507 ± 0.010        3
      P3 L1-distilbert_cap2000  maha           0.440 ± 0.007        3
      P3 L1-secbert-kv_cap2000   knn           0.446 ± 0.031        3
      P3 L1-secbert-kv_cap2000  maha           0.474 ± 0.018        3
      P3    L1-secbert_cap2000   knn           0.556 ± 0.034        3
      P3    L1-secbert_cap2000  maha           0.515 ± 0.004        3
      P3 L1-tiny-local_cap2000   knn           0.496 ± 0.040        3
      P3 L1-tiny-local_cap2000  maha           0.543 ± 0.004        3
      P3      MLP-bin5_cap2000   knn           0.570 ± 0.033        3
      P3      MLP-bin5_cap2000  maha           0.510 ± 0.044        3
      P3              MLP_cap0   knn           0.510 ± 0.042        3
      P3              MLP_cap0  maha           0.481 ± 0.031        3
      P3           MLP_cap2000   knn           0.461 ± 0.016        3
      P3           MLP_cap2000  maha           0.453 ± 0.021        3
```
