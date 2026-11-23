# First-round revision experiments (seeds 0-2)

## E1. Time-ordered vs random windows on the same later test flows (RF)

```
protocol            condition           calibration benign_rejected_as_unknown benign_false_alarm_rate unknown_recall unknown_flagged_malicious  seeds
      P1   window_early|c=0.0 target_warmup_far0.01              0.011 ± 0.002           0.032 ± 0.001  0.449 ± 0.041             0.723 ± 0.036      3
      P1   window_early|c=0.0 target_warmup_far0.05              0.028 ± 0.002           0.046 ± 0.004  0.715 ± 0.030             0.877 ± 0.022      3
      P1  window_early|c=0.05 target_warmup_far0.01              0.010 ± 0.003           0.031 ± 0.002  0.374 ± 0.056             0.679 ± 0.027      3
      P1  window_early|c=0.05 target_warmup_far0.05              0.026 ± 0.002           0.044 ± 0.003  0.701 ± 0.034             0.866 ± 0.024      3
      P1  window_random|c=0.0 target_warmup_far0.01              0.012 ± 0.002           0.032 ± 0.001  0.479 ± 0.057             0.729 ± 0.043      3
      P1  window_random|c=0.0 target_warmup_far0.05              0.031 ± 0.003           0.048 ± 0.004  0.767 ± 0.013             0.909 ± 0.008      3
      P1 window_random|c=0.05 target_warmup_far0.01              0.010 ± 0.002           0.031 ± 0.001  0.392 ± 0.046             0.677 ± 0.043      3
      P1 window_random|c=0.05 target_warmup_far0.05              0.026 ± 0.003           0.043 ± 0.003  0.750 ± 0.017             0.894 ± 0.013      3
      P3   window_early|c=0.0 target_warmup_far0.01              0.047 ± 0.045           0.174 ± 0.043  0.097 ± 0.019             0.330 ± 0.012      3
      P3   window_early|c=0.0 target_warmup_far0.05              0.119 ± 0.110           0.231 ± 0.102  0.128 ± 0.026             0.337 ± 0.007      3
      P3  window_early|c=0.05 target_warmup_far0.01              0.048 ± 0.046           0.174 ± 0.043  0.097 ± 0.019             0.330 ± 0.012      3
      P3  window_early|c=0.05 target_warmup_far0.05              0.120 ± 0.110           0.232 ± 0.101  0.128 ± 0.026             0.337 ± 0.007      3
      P3  window_random|c=0.0 target_warmup_far0.01              0.013 ± 0.004           0.143 ± 0.012  0.093 ± 0.013             0.329 ± 0.011      3
      P3  window_random|c=0.0 target_warmup_far0.05              0.057 ± 0.012           0.173 ± 0.012  0.113 ± 0.007             0.335 ± 0.006      3
      P3 window_random|c=0.05 target_warmup_far0.01              0.011 ± 0.006           0.141 ± 0.016  0.044 ± 0.025             0.316 ± 0.011      3
      P3 window_random|c=0.05 target_warmup_far0.05              0.051 ± 0.014           0.170 ± 0.013  0.111 ± 0.006             0.335 ± 0.006      3
```

Benign flows classified as a known attack by the closed-set RF (no threshold), later 70% vs full test:

```
protocol benign_as_attack_closedset_late benign_as_attack_closedset_full  seeds
      P1                   0.024 ± 0.003                   0.140 ± 0.004      3
      P3                   0.137 ± 0.015                   0.175 ± 0.019      3
```

## E2. Total-alert control (RF; AE gate + RF labels)

```
protocol condition               calibration benign_rejected_as_unknown benign_false_alarm_rate unknown_recall unknown_flagged_malicious known_attack_detected known_attack_correct  seeds
      P1     c=0.0      ae_gate_rf_label0.01              0.007 ± 0.001           0.008 ± 0.001  0.289 ± 0.018             0.318 ± 0.030         0.256 ± 0.030        0.255 ± 0.030      3
      P1     c=0.0      ae_gate_rf_label0.05              0.046 ± 0.007           0.051 ± 0.006  0.511 ± 0.027             0.566 ± 0.037         0.479 ± 0.039        0.468 ± 0.037      3
      P1     c=0.0 rf_total_alert_budget0.01              0.001 ± 0.000           0.004 ± 0.001  0.063 ± 0.032             0.097 ± 0.030         0.353 ± 0.049        0.351 ± 0.048      3
      P1     c=0.0 rf_total_alert_budget0.05              0.017 ± 0.001           0.022 ± 0.003  0.281 ± 0.002             0.286 ± 0.004         0.452 ± 0.046        0.435 ± 0.045      3
      P1     c=0.0     rf_unknown_budget0.01              0.011 ± 0.003           0.135 ± 0.002  0.408 ± 0.049             0.629 ± 0.035         0.980 ± 0.001        0.958 ± 0.001      3
      P1     c=0.0     rf_unknown_budget0.05              0.047 ± 0.003           0.164 ± 0.004  0.653 ± 0.013             0.793 ± 0.005         0.987 ± 0.001        0.940 ± 0.001      3
      P1    c=0.05      ae_gate_rf_label0.01              0.003 ± 0.001           0.003 ± 0.001  0.171 ± 0.037             0.179 ± 0.039         0.115 ± 0.031        0.114 ± 0.030      3
      P1    c=0.05      ae_gate_rf_label0.05              0.031 ± 0.003           0.035 ± 0.002  0.415 ± 0.047             0.454 ± 0.054         0.398 ± 0.049        0.391 ± 0.048      3
      P1    c=0.05 rf_total_alert_budget0.01              0.000 ± 0.000           0.000 ± 0.000  0.000 ± 0.000             0.000 ± 0.000         0.000 ± 0.000        0.000 ± 0.000      3
      P1    c=0.05 rf_total_alert_budget0.05              0.002 ± 0.001           0.004 ± 0.001  0.083 ± 0.019             0.083 ± 0.019         0.319 ± 0.059        0.311 ± 0.059      3
      P1    c=0.05     rf_unknown_budget0.01              0.009 ± 0.003           0.134 ± 0.002  0.332 ± 0.039             0.580 ± 0.038         0.980 ± 0.001        0.958 ± 0.001      3
      P1    c=0.05     rf_unknown_budget0.05              0.041 ± 0.003           0.159 ± 0.003  0.637 ± 0.014             0.780 ± 0.009         0.986 ± 0.000        0.942 ± 0.001      3
      P3     c=0.0      ae_gate_rf_label0.01              0.008 ± 0.004           0.010 ± 0.004  0.001 ± 0.000             0.014 ± 0.007         0.014 ± 0.007        0.000 ± 0.000      3
      P3     c=0.0      ae_gate_rf_label0.05              0.045 ± 0.006           0.046 ± 0.006  0.005 ± 0.004             0.024 ± 0.002         0.024 ± 0.002        0.001 ± 0.001      3
      P3     c=0.0 rf_total_alert_budget0.01              0.001 ± 0.000           0.005 ± 0.001  0.002 ± 0.001             0.006 ± 0.001         0.017 ± 0.001        0.001 ± 0.000      3
      P3     c=0.0 rf_total_alert_budget0.05              0.010 ± 0.002           0.043 ± 0.011  0.010 ± 0.007             0.042 ± 0.020         0.049 ± 0.016        0.003 ± 0.002      3
      P3     c=0.0     rf_unknown_budget0.01              0.007 ± 0.001           0.178 ± 0.019  0.094 ± 0.013             0.331 ± 0.010         0.329 ± 0.022        0.222 ± 0.014      3
      P3     c=0.0     rf_unknown_budget0.05              0.039 ± 0.005           0.199 ± 0.016  0.118 ± 0.009             0.339 ± 0.006         0.371 ± 0.030        0.218 ± 0.017      3
      P3    c=0.05      ae_gate_rf_label0.01              0.008 ± 0.004           0.009 ± 0.005  0.001 ± 0.000             0.014 ± 0.007         0.014 ± 0.007        0.000 ± 0.000      3
      P3    c=0.05      ae_gate_rf_label0.05              0.045 ± 0.005           0.046 ± 0.005  0.004 ± 0.004             0.023 ± 0.002         0.023 ± 0.002        0.001 ± 0.001      3
      P3    c=0.05 rf_total_alert_budget0.01              0.001 ± 0.000           0.005 ± 0.001  0.001 ± 0.000             0.006 ± 0.001         0.016 ± 0.002        0.001 ± 0.000      3
      P3    c=0.05 rf_total_alert_budget0.05              0.011 ± 0.003           0.045 ± 0.013  0.011 ± 0.007             0.039 ± 0.024         0.048 ± 0.010        0.003 ± 0.002      3
      P3    c=0.05     rf_unknown_budget0.01              0.006 ± 0.002           0.178 ± 0.020  0.046 ± 0.025             0.318 ± 0.011         0.314 ± 0.006        0.222 ± 0.015      3
      P3    c=0.05     rf_unknown_budget0.05              0.035 ± 0.004           0.197 ± 0.018  0.116 ± 0.007             0.339 ± 0.006         0.367 ± 0.034        0.218 ± 0.017      3
```

## E5. LightGBM with an energy score (1% warm-up budget, clean window)

```
protocol     auroc_ood auroc_unknown_vs_benign unknown_recall benign_false_alarm_rate  seeds
      P1 0.831 ± 0.015           0.775 ± 0.011  0.322 ± 0.017           0.161 ± 0.002      3
      P3 0.486 ± 0.043           0.441 ± 0.051  0.014 ± 0.009           0.211 ± 0.060      3
```

## E7. P3 without filtering target units (every unit unseen in the source is unknown)

```
                                         block detector     auroc_ood auroc_unknown_vs_benign unknown_recall benign_rejected_as_unknown benign_false_alarm_rate recall_BACKDOOR recall_BRUTEFORCE  recall_FLOOD recall_MITM_SPOOF recall_RANSOMWARE    recall_WEB  recall_RECON  recall_THEFT  seeds
nf_bot_iot_v3__to__nf_ton_iot_v3__family=FLOOD       AE 0.701 ± 0.070           0.654 ± 0.054  0.031 ± 0.007              0.010 ± 0.002           0.010 ± 0.002   0.026 ± 0.044     0.052 ± 0.004 0.056 ± 0.029     0.087 ± 0.064     0.007 ± 0.006 0.003 ± 0.000             -             -      3
nf_bot_iot_v3__to__nf_ton_iot_v3__family=FLOOD   RF-MSP 0.620 ± 0.079           0.608 ± 0.113  0.047 ± 0.047              0.008 ± 0.003           0.375 ± 0.044   0.315 ± 0.531     0.003 ± 0.005 0.001 ± 0.002     0.012 ± 0.014     0.080 ± 0.062 0.046 ± 0.046             -             -      3
nf_bot_iot_v3__to__nf_ton_iot_v3__family=RECON       AE 0.526 ± 0.060           0.623 ± 0.052  0.020 ± 0.004              0.010 ± 0.002           0.010 ± 0.002   0.026 ± 0.044     0.052 ± 0.004             -     0.087 ± 0.064     0.007 ± 0.006 0.003 ± 0.000 0.000 ± 0.000             -      3
nf_bot_iot_v3__to__nf_ton_iot_v3__family=RECON   RF-MSP 0.787 ± 0.012           0.701 ± 0.036  0.076 ± 0.020              0.006 ± 0.000           0.011 ± 0.001   0.012 ± 0.010     0.075 ± 0.046             -     0.006 ± 0.004     0.047 ± 0.029 0.119 ± 0.022 0.011 ± 0.006             -      3
nf_ton_iot_v3__to__nf_bot_iot_v3__family=FLOOD       AE 0.875 ± 0.005           0.707 ± 0.008  0.000 ± 0.000              0.009 ± 0.007           0.009 ± 0.007               -                 - 0.000 ± 0.000                 -                 -             -             - 0.000 ± 0.000      3
nf_ton_iot_v3__to__nf_bot_iot_v3__family=FLOOD   RF-MSP 0.873 ± 0.024           0.746 ± 0.045  0.360 ± 0.057              0.009 ± 0.002           0.164 ± 0.056               -                 - 0.364 ± 0.058                 -                 -             -             - 0.011 ± 0.011      3
nf_ton_iot_v3__to__nf_bot_iot_v3__family=RECON       AE 0.064 ± 0.010           0.245 ± 0.041  0.000 ± 0.000              0.009 ± 0.007           0.009 ± 0.007               -                 -             -                 -                 -             - 0.000 ± 0.000 0.000 ± 0.000      3
nf_ton_iot_v3__to__nf_bot_iot_v3__family=RECON   RF-MSP 0.031 ± 0.002           0.073 ± 0.000  0.001 ± 0.002              0.007 ± 0.008           0.164 ± 0.025               -                 -             -                 -                 -             - 0.001 ± 0.002 0.000 ± 0.000      3
```

## E8. MLP 2k, de-duplication = dedupnone (1% warm-up budget, clean window)

```
protocol     auroc_ood auroc_unknown_vs_benign unknown_recall benign_false_alarm_rate  seeds
      P1 0.904 ± 0.004                       -  0.274 ± 0.010           0.154 ± 0.002      3
      P3 0.520 ± 0.042                       -  0.003 ± 0.002           0.259 ± 0.011      3
```

## E8. MLP 2k, de-duplication = dedupmajority (1% warm-up budget, clean window)

```
protocol     auroc_ood auroc_unknown_vs_benign unknown_recall benign_false_alarm_rate  seeds
      P1 0.891 ± 0.004                       -  0.267 ± 0.016           0.176 ± 0.006      3
      P3 0.486 ± 0.044                       -  0.006 ± 0.008           0.253 ± 0.034      3
```

## E8. Autoencoder, de-duplication = dedupnone (1% warm-up budget, clean window)

```
protocol     auroc_ood auroc_unknown_vs_benign unknown_recall benign_false_alarm_rate  seeds
      P1 0.588 ± 0.004           0.915 ± 0.001  0.333 ± 0.021           0.012 ± 0.001      3
      P3 0.502 ± 0.006           0.540 ± 0.019  0.008 ± 0.001           0.011 ± 0.000      3
```

## E8. Autoencoder, de-duplication = dedupmajority (1% warm-up budget, clean window)

```
protocol     auroc_ood auroc_unknown_vs_benign unknown_recall benign_false_alarm_rate  seeds
      P1 0.597 ± 0.010           0.892 ± 0.005  0.295 ± 0.053           0.011 ± 0.002      3
      P3 0.482 ± 0.006           0.484 ± 0.023  0.012 ± 0.007           0.012 ± 0.001      3
```

## E10. Chronological partitions within each family (P1)

```
detector           calibration     auroc_ood auroc_unknown_vs_benign benign_rejected_as_unknown benign_false_alarm_rate unknown_recall unknown_flagged_malicious  seeds
      AE target_warmup_far0.01 0.544 ± 0.007           0.741 ± 0.011              0.206 ± 0.035           0.206 ± 0.035  0.583 ± 0.053             0.583 ± 0.053      3
      AE target_warmup_far0.05 0.544 ± 0.007           0.741 ± 0.011              0.405 ± 0.018           0.405 ± 0.018  0.840 ± 0.026             0.840 ± 0.026      3
  RF-MSP target_warmup_far0.01 0.799 ± 0.008           0.806 ± 0.005              0.234 ± 0.025           0.277 ± 0.024  0.670 ± 0.023             0.857 ± 0.024      3
  RF-MSP target_warmup_far0.05 0.799 ± 0.008           0.806 ± 0.005              0.337 ± 0.007           0.362 ± 0.010  0.748 ± 0.006             0.887 ± 0.005      3
```

## E12. Additional baselines (1% warm-up budget, clean window)

```
protocol    method     auroc_ood auroc_unknown_vs_benign unknown_recall benign_false_alarm_rate known_macro_f1  seeds
      P1   knn-raw 0.883 ± 0.001           0.895 ± 0.001  0.322 ± 0.003           0.009 ± 0.002  0.052 ± 0.000      3
      P1 mlp-react 0.785 ± 0.010           0.748 ± 0.029  0.147 ± 0.134           0.174 ± 0.001  0.790 ± 0.001      3
      P3   knn-raw 0.466 ± 0.004           0.448 ± 0.007  0.019 ± 0.001           0.009 ± 0.002  0.187 ± 0.000      3
      P3 mlp-coral 0.429 ± 0.011           0.445 ± 0.023  0.021 ± 0.012           0.537 ± 0.124  0.212 ± 0.013      3
      P3 mlp-react 0.459 ± 0.032           0.432 ± 0.042  0.040 ± 0.025           0.263 ± 0.010  0.172 ± 0.003      3
      P3  rf-coral 0.397 ± 0.018           0.432 ± 0.019  0.041 ± 0.014           0.385 ± 0.011  0.164 ± 0.013      3
```

## E13. Robust window rules under zero-day contamination (RF)

```
protocol      condition           calibration benign_rejected_as_unknown benign_false_alarm_rate unknown_recall unknown_flagged_malicious  seeds
      P1  holdout_c=0.0       median5_far0.01              0.011 ± 0.003           0.135 ± 0.002  0.404 ± 0.053             0.625 ± 0.041      3
      P1  holdout_c=0.0       median5_far0.05              0.047 ± 0.003           0.164 ± 0.004  0.653 ± 0.012             0.794 ± 0.005      3
      P1  holdout_c=0.0   rf_filtered_far0.01              0.015 ± 0.003           0.138 ± 0.002  0.456 ± 0.030             0.654 ± 0.030      3
      P1  holdout_c=0.0   rf_filtered_far0.05              0.052 ± 0.003           0.168 ± 0.003  0.659 ± 0.010             0.798 ± 0.004      3
      P1  holdout_c=0.0 target_warmup_far0.01              0.011 ± 0.003           0.135 ± 0.002  0.408 ± 0.049             0.629 ± 0.035      3
      P1  holdout_c=0.0 target_warmup_far0.05              0.047 ± 0.003           0.164 ± 0.004  0.653 ± 0.013             0.793 ± 0.005      3
      P1  holdout_c=0.0   trimmed0.05_far0.01              0.055 ± 0.003           0.171 ± 0.003  0.665 ± 0.008             0.800 ± 0.003      3
      P1  holdout_c=0.0   trimmed0.05_far0.05              0.087 ± 0.001           0.193 ± 0.004  0.700 ± 0.002             0.821 ± 0.007      3
      P1  holdout_c=0.0    trimmed0.2_far0.01              0.162 ± 0.002           0.236 ± 0.004  0.789 ± 0.013             0.879 ± 0.002      3
      P1  holdout_c=0.0    trimmed0.2_far0.05              0.180 ± 0.003           0.245 ± 0.004  0.818 ± 0.021             0.883 ± 0.002      3
      P1 holdout_c=0.05       median5_far0.01              0.011 ± 0.002           0.135 ± 0.003  0.399 ± 0.058             0.621 ± 0.048      3
      P1 holdout_c=0.05       median5_far0.05              0.047 ± 0.003           0.164 ± 0.004  0.652 ± 0.011             0.793 ± 0.004      3
      P1 holdout_c=0.05   rf_filtered_far0.01              0.007 ± 0.001           0.133 ± 0.003  0.174 ± 0.047             0.445 ± 0.049      3
      P1 holdout_c=0.05   rf_filtered_far0.05              0.033 ± 0.001           0.152 ± 0.003  0.582 ± 0.034             0.729 ± 0.039      3
      P1 holdout_c=0.05 target_warmup_far0.01              0.004 ± 0.001           0.131 ± 0.003  0.102 ± 0.028             0.425 ± 0.044      3
      P1 holdout_c=0.05 target_warmup_far0.05              0.025 ± 0.003           0.146 ± 0.001  0.502 ± 0.025             0.691 ± 0.019      3
      P1 holdout_c=0.05   trimmed0.05_far0.01              0.031 ± 0.003           0.150 ± 0.002  0.566 ± 0.023             0.740 ± 0.018      3
      P1 holdout_c=0.05   trimmed0.05_far0.05              0.063 ± 0.002           0.177 ± 0.004  0.677 ± 0.007             0.807 ± 0.006      3
      P1 holdout_c=0.05    trimmed0.2_far0.01              0.145 ± 0.003           0.224 ± 0.006  0.778 ± 0.006             0.875 ± 0.004      3
      P1 holdout_c=0.05    trimmed0.2_far0.05              0.162 ± 0.004           0.235 ± 0.005  0.793 ± 0.011             0.880 ± 0.002      3
      P1  holdout_c=0.2       median5_far0.01              0.011 ± 0.002           0.135 ± 0.003  0.399 ± 0.058             0.621 ± 0.048      3
      P1  holdout_c=0.2       median5_far0.05              0.047 ± 0.003           0.164 ± 0.004  0.652 ± 0.011             0.793 ± 0.004      3
      P1  holdout_c=0.2   rf_filtered_far0.01              0.005 ± 0.001           0.132 ± 0.003  0.101 ± 0.044             0.403 ± 0.057      3
      P1  holdout_c=0.2   rf_filtered_far0.05              0.020 ± 0.002           0.142 ± 0.003  0.339 ± 0.042             0.536 ± 0.041      3
      P1  holdout_c=0.2 target_warmup_far0.01              0.003 ± 0.001           0.131 ± 0.003  0.041 ± 0.009             0.392 ± 0.054      3
      P1  holdout_c=0.2 target_warmup_far0.05              0.012 ± 0.002           0.137 ± 0.002  0.223 ± 0.022             0.501 ± 0.031      3
      P1  holdout_c=0.2   trimmed0.05_far0.01              0.014 ± 0.002           0.138 ± 0.002  0.259 ± 0.018             0.523 ± 0.021      3
      P1  holdout_c=0.2   trimmed0.05_far0.05              0.030 ± 0.003           0.150 ± 0.002  0.414 ± 0.009             0.598 ± 0.022      3
      P1  holdout_c=0.2    trimmed0.2_far0.01              0.078 ± 0.002           0.184 ± 0.003  0.690 ± 0.006             0.813 ± 0.009      3
      P1  holdout_c=0.2    trimmed0.2_far0.05              0.098 ± 0.003           0.198 ± 0.005  0.728 ± 0.003             0.840 ± 0.010      3
      P3  holdout_c=0.0       median5_far0.01              0.006 ± 0.001           0.178 ± 0.018  0.094 ± 0.013             0.331 ± 0.010      3
      P3  holdout_c=0.0       median5_far0.05              0.036 ± 0.003           0.198 ± 0.015  0.116 ± 0.007             0.339 ± 0.006      3
      P3  holdout_c=0.0   rf_filtered_far0.01              0.019 ± 0.008           0.182 ± 0.019  0.100 ± 0.011             0.333 ± 0.009      3
      P3  holdout_c=0.0   rf_filtered_far0.05              0.056 ± 0.009           0.208 ± 0.017  0.129 ± 0.012             0.341 ± 0.006      3
      P3  holdout_c=0.0 target_warmup_far0.01              0.007 ± 0.001           0.178 ± 0.019  0.094 ± 0.013             0.331 ± 0.010      3
      P3  holdout_c=0.0 target_warmup_far0.05              0.039 ± 0.005           0.199 ± 0.016  0.118 ± 0.009             0.339 ± 0.006      3
      P3  holdout_c=0.0   trimmed0.05_far0.01              0.049 ± 0.001           0.206 ± 0.014  0.126 ± 0.012             0.340 ± 0.007      3
      P3  holdout_c=0.0   trimmed0.05_far0.05              0.085 ± 0.008           0.232 ± 0.018  0.178 ± 0.054             0.354 ± 0.014      3
      P3  holdout_c=0.0    trimmed0.2_far0.01              0.177 ± 0.008           0.307 ± 0.019  0.266 ± 0.118             0.385 ± 0.057      3
      P3  holdout_c=0.0    trimmed0.2_far0.05              0.203 ± 0.015           0.330 ± 0.022  0.274 ± 0.115             0.388 ± 0.054      3
      P3 holdout_c=0.05       median5_far0.01              0.006 ± 0.001           0.178 ± 0.018  0.094 ± 0.013             0.331 ± 0.010      3
      P3 holdout_c=0.05       median5_far0.05              0.036 ± 0.003           0.198 ± 0.015  0.117 ± 0.007             0.339 ± 0.006      3
      P3 holdout_c=0.05   rf_filtered_far0.01              0.018 ± 0.009           0.181 ± 0.020  0.055 ± 0.036             0.320 ± 0.012      3
      P3 holdout_c=0.05   rf_filtered_far0.05              0.054 ± 0.011           0.207 ± 0.019  0.128 ± 0.011             0.341 ± 0.007      3
      P3 holdout_c=0.05 target_warmup_far0.01              0.007 ± 0.002           0.178 ± 0.019  0.029 ± 0.015             0.315 ± 0.007      3
      P3 holdout_c=0.05 target_warmup_far0.05              0.037 ± 0.002           0.197 ± 0.014  0.117 ± 0.007             0.340 ± 0.006      3
      P3 holdout_c=0.05   trimmed0.05_far0.01              0.045 ± 0.003           0.204 ± 0.017  0.126 ± 0.013             0.343 ± 0.007      3
      P3 holdout_c=0.05   trimmed0.05_far0.05              0.077 ± 0.006           0.226 ± 0.017  0.168 ± 0.044             0.353 ± 0.014      3
      P3 holdout_c=0.05    trimmed0.2_far0.01              0.174 ± 0.008           0.306 ± 0.016  0.263 ± 0.116             0.386 ± 0.056      3
      P3 holdout_c=0.05    trimmed0.2_far0.05              0.213 ± 0.032           0.338 ± 0.040  0.277 ± 0.107             0.389 ± 0.053      3
      P3  holdout_c=0.2       median5_far0.01              0.006 ± 0.001           0.178 ± 0.018  0.094 ± 0.013             0.331 ± 0.011      3
      P3  holdout_c=0.2       median5_far0.05              0.038 ± 0.005           0.199 ± 0.016  0.117 ± 0.007             0.339 ± 0.006      3
      P3  holdout_c=0.2   rf_filtered_far0.01              0.019 ± 0.010           0.182 ± 0.022  0.042 ± 0.047             0.314 ± 0.012      3
      P3  holdout_c=0.2   rf_filtered_far0.05              0.058 ± 0.017           0.210 ± 0.022  0.130 ± 0.013             0.341 ± 0.008      3
      P3  holdout_c=0.2 target_warmup_far0.01              0.006 ± 0.001           0.178 ± 0.019  0.011 ± 0.009             0.312 ± 0.010      3
      P3  holdout_c=0.2 target_warmup_far0.05              0.035 ± 0.003           0.197 ± 0.015  0.061 ± 0.035             0.329 ± 0.019      3
      P3  holdout_c=0.2   trimmed0.05_far0.01              0.044 ± 0.005           0.203 ± 0.015  0.083 ± 0.051             0.332 ± 0.021      3
      P3  holdout_c=0.2   trimmed0.05_far0.05              0.070 ± 0.013           0.224 ± 0.023  0.144 ± 0.025             0.352 ± 0.014      3
      P3  holdout_c=0.2    trimmed0.2_far0.01              0.182 ± 0.037           0.316 ± 0.044  0.249 ± 0.103             0.388 ± 0.054      3
      P3  holdout_c=0.2    trimmed0.2_far0.05              0.207 ± 0.037           0.331 ± 0.044  0.274 ± 0.090             0.390 ± 0.052      3
```

## E14. RF 2k bin5 with an explicit missing-value token (splits with NF-BoT-IoT-v3)

```
protocol     auroc_ood unknown_recall benign_false_alarm_rate  seeds
      P1 0.955 ± 0.019  0.380 ± 0.135           0.016 ± 0.001      3
      P3 0.476 ± 0.031  0.031 ± 0.048           0.264 ± 0.037      3
```

## E14. MLP 2k bin5 with an explicit missing-value token (splits with NF-BoT-IoT-v3)

```
protocol     auroc_ood unknown_recall benign_false_alarm_rate  seeds
      P1 0.930 ± 0.001  0.278 ± 0.082           0.017 ± 0.003      3
      P3 0.511 ± 0.036  0.026 ± 0.037           0.245 ± 0.016      3
```
