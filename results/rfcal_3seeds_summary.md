# RF threshold-rule analyses over seeds 0-2

## P1 family level, pseudo-unknown Youden, per held-out family (mean, std over seeds)

```
               auroc_ood        unknown_recall        unknown_flagged_malicious        benign_false_alarm_rate       
                    mean    std           mean    std                      mean    std                    mean    std
src holdout                                                                                                          
bot FLOOD          0.991  0.001          1.000  0.000                     1.000  0.000                   0.080  0.016
    RECON          0.875  0.009          0.752  0.026                     0.753  0.024                   0.027  0.004
    THEFT          0.996  0.000          0.936  0.091                     0.996  0.006                   0.040  0.006
ton BACKDOOR       0.997  0.002          0.998  0.001                     0.999  0.001                   0.284  0.005
    BRUTEFORCE     0.796  0.055          0.249  0.017                     0.920  0.007                   0.261  0.005
    FLOOD          0.865  0.005          0.652  0.139                     0.829  0.143                   0.284  0.002
    MITM_SPOOF     0.964  0.006          0.920  0.011                     0.998  0.001                   0.279  0.010
    RANSOMWARE     0.973  0.010          0.893  0.045                     0.981  0.022                   0.274  0.005
    RECON          0.432  0.006          0.068  0.010                     0.068  0.010                   0.059  0.001
    WEB            0.912  0.004          0.701  0.028                     0.856  0.033                   0.286  0.003
```
- mean over families, auroc_ood: 0.880 ± 0.006
- mean over families, unknown_recall: 0.717 ± 0.024
- mean over families, unknown_flagged_malicious: 0.840 ± 0.020
- mean over families, benign_false_alarm_rate: 0.187 ± 0.004

- subfamily mean AUROC-OOD: 0.844 ± 0.004
- BoT subfamily DOS: AUROC 0.563 ± 0.027, unknown recall 0.011 ± 0.000, flagged malicious 1.000 ± 0.000
- BoT subfamily DDOS: AUROC 0.624 ± 0.012, unknown recall 0.092 ± 0.025, flagged malicious 1.000 ± 0.000
- ToN RECON family: AUROC 0.432 ± 0.006, flagged malicious 0.068 ± 0.010

## P1 family, threshold rules (split mean per seed, then mean ± std)

- benign_far0.01: benign→unknown 0.011 ± 0.003; unknown recall 0.399 ± 0.058; benign→known attack 0.125 ± 0.005; known macro-F1 0.790 ± 0.000
- benign_far0.05: benign→unknown 0.047 ± 0.003; unknown recall 0.653 ± 0.013; benign→known attack 0.117 ± 0.004; known macro-F1 0.784 ± 0.001
- pseudo_youden: benign→unknown 0.087 ± 0.004; unknown recall 0.717 ± 0.024; benign→known attack 0.101 ± 0.006; known macro-F1 0.779 ± 0.001

## P2 (family, norm none)

- bot→ton benign_far0.01: benign→unknown 0.440 ± 0.172, benign→known 0.253 ± 0.038, known macro-F1 0.197 ± 0.045
- bot→ton benign_far0.05: benign→unknown 0.925 ± 0.016, benign→known 0.062 ± 0.011, known macro-F1 0.024 ± 0.013
- bot→ton pseudo_youden: benign→unknown 0.881 ± 0.059, benign→known 0.097 ± 0.053, known macro-F1 0.056 ± 0.037
- bot→ton target_warmup_far0.01: benign→unknown 0.007 ± 0.002, benign→known 0.376 ± 0.051, known macro-F1 0.199 ± 0.011
- bot→ton target_warmup_far0.05: benign→unknown 0.045 ± 0.013, benign→known 0.369 ± 0.054, known macro-F1 0.215 ± 0.042
- ton→bot benign_far0.01: benign→unknown 0.420 ± 0.041, benign→known 0.081 ± 0.021, known macro-F1 0.043 ± 0.006
- ton→bot benign_far0.05: benign→unknown 0.584 ± 0.036, benign→known 0.021 ± 0.012, known macro-F1 0.040 ± 0.002
- ton→bot pseudo_youden: benign→unknown 0.815 ± 0.098, benign→known 0.010 ± 0.006, known macro-F1 0.020 ± 0.010
- ton→bot target_warmup_far0.01: benign→unknown 0.004 ± 0.005, benign→known 0.205 ± 0.029, known macro-F1 0.041 ± 0.005
- ton→bot target_warmup_far0.05: benign→unknown 0.034 ± 0.014, benign→known 0.188 ± 0.017, known macro-F1 0.044 ± 0.003

## P3 AUROC-OOD (norm none), mean over splits

- family: 0.581 ± 0.026
  - with per-network rank normalisation: 0.419 ± 0.050
- subfamily: 0.542 ± 0.008
  - with per-network rank normalisation: 0.488 ± 0.027
- ToN→BoT RECON (family): AUROC 0.028 ± 0.003

## Threshold rules across networks (family, norm none, contamination 0.05)

```
protocol                  rule     auroc_ood unknown_recall benign_rejected_as_unknown benign_as_known_attack
      P2        benign_far0.01     nan ± nan      nan ± nan              0.430 ± 0.074          0.167 ± 0.029
      P2        benign_far0.05     nan ± nan      nan ± nan              0.755 ± 0.026          0.042 ± 0.008
      P2         pseudo_youden     nan ± nan      nan ± nan              0.848 ± 0.070          0.054 ± 0.029
      P2 target_warmup_far0.01     nan ± nan      nan ± nan              0.005 ± 0.003          0.290 ± 0.018
      P2 target_warmup_far0.05     nan ± nan      nan ± nan              0.040 ± 0.012          0.279 ± 0.022
      P3        benign_far0.01 0.581 ± 0.026  0.544 ± 0.014              0.470 ± 0.052          0.106 ± 0.007
      P3        benign_far0.05 0.581 ± 0.026  0.723 ± 0.007              0.773 ± 0.069          0.054 ± 0.002
      P3         pseudo_youden 0.581 ± 0.026  0.740 ± 0.016              0.874 ± 0.011          0.037 ± 0.012
      P3 target_warmup_far0.01 0.581 ± 0.026  0.046 ± 0.025              0.006 ± 0.002          0.171 ± 0.018
      P3 target_warmup_far0.05 0.581 ± 0.026  0.116 ± 0.007              0.035 ± 0.004          0.162 ± 0.014
```

## Ranges used in the text

- target_warmup_far0.01, contamination 0.05, benign→unknown over protocol × level × norm: 0.004–0.008
- target_warmup_far0.05, contamination 0.05, benign→unknown over protocol × level × norm: 0.035–0.047
- target_warmup_far0.01, contamination 0.20, benign→unknown: max 0.005
- source benign_far0.01, benign→unknown over protocol × level: 0.430–0.470
- P3 warm-up unknown recall (none): 0.025–0.127
- P3 warm-up unknown recall (per_network): 0.005–0.084
- P3 source-calibrated unknown recall: 0.544–0.804; benign→unknown 0.452–0.916
- P2 known macro-F1: 0.015–0.129
- benign→known attack under warm-up rules: 0.159–0.410
