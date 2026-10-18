# Statistical comparison — metric `unknown_recall`, rule `target_warmup_far0.05`, warm-up contamination 0, seeds [0, 1, 2]


### Scope: all splits (P1 + P3)
Blocks (splits) = 14, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.500           0.007      3      6.86
RF 2k|msp           0.479           0.006      3      9.71
MLP 2k bin5|maha    0.461           0.037      3      9.79
RF 2k bin5|msp      0.450           0.028      3     10.07
MLP 2k bin5|energy  0.392           0.043      3     10.86
MLP 2k bin5|knn     0.434           0.037      3     11.64
MLP full|knn        0.437           0.041      3     12.07
SecBERT-kv|maha     0.378           0.048      3     12.14
MLP 2k|knn          0.373           0.078      3     13.07
SecBERT-kv|knn      0.356           0.071      3     13.29
MLP full|maha       0.461           0.026      3     13.39
SecBERT-kv|energy   0.334           0.018      3     13.57
MLP full|energy     0.302           0.059      3     14.00
DistilBERT|maha     0.440           0.031      3     14.21
SecBERT|maha        0.397           0.031      3     14.79
MLP 2k|energy       0.229           0.059      3     15.57
MLP 2k|maha         0.408           0.038      3     15.68
tiny-local|maha     0.314           0.038      3     17.93
DistilBERT|knn      0.330           0.042      3     18.00
DistilBERT|energy   0.277           0.058      3     18.07
tiny-local|knn      0.258           0.057      3     18.21
MLP full|msp        0.168           0.053      3     19.50
MLP 2k bin5|msp     0.222           0.038      3     19.50
SecBERT|energy      0.201           0.058      3     19.71
SecBERT|knn         0.257           0.037      3     19.79
MLP 2k|msp          0.152           0.049      3     20.50
tiny-local|energy   0.183           0.035      3     20.71
SecBERT-kv|msp      0.207           0.060      3     20.86
tiny-local|msp      0.125           0.016      3     23.14
DistilBERT|msp      0.132           0.016      3     24.36
SecBERT|msp         0.114           0.055      3     25.00
```

Friedman chi2 = 109.69, p = 5.16e-11. Nemenyi critical difference (alpha 0.05) = 12.94 ranks. Two combinations differ significantly when their average ranks differ by more than 12.94.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 24.65, p = 3.38e-03, Nemenyi CD = 3.62. Average ranks: RF full|msp 3.14, RF 2k|msp 4.14, MLP 2k bin5|maha 4.50, RF 2k bin5|msp 5.07, SecBERT-kv|maha 5.50, MLP full|maha 5.54, MLP 2k|maha 6.46, DistilBERT|maha 6.50, SecBERT|maha 6.50, tiny-local|maha 7.64

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.1488   -0.2384    -0.0500     1     0      13 -0.8095      0.0052  0.0840
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.1697   -0.2647    -0.0666     1     0      13 -0.8286      0.0040  0.0685
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0435   -0.1589     0.0672     5     0       9 -0.2000      0.5416  1.0000
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0719   -0.0153     0.1718     8     0       6  0.3905      0.2166  1.0000
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0725   -0.0382     0.1958     9     0       5  0.3143      0.3258  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.1101    0.0409     0.1829    11     0       3  0.7143      0.0166  0.2490
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.1054   -0.2048    -0.0144     5     0       9 -0.5048      0.1040  0.9360
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0348   -0.0274     0.1047     6     0       8  0.0857      0.8077  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0387   -0.1120     0.0491     2     0      12 -0.6381      0.0353  0.4939
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0596   -0.1537     0.0391     2     0      12 -0.5619      0.0676  0.8115
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0319   -0.0492     0.1231     7     0       7  0.0667      0.8552  1.0000
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0823   -0.2054     0.0204     3     1      10 -0.5385      0.0788  0.8634
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.1032   -0.2306     0.0082     2     0      12 -0.6000      0.0494  0.6427
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0181   -0.1149     0.0726     7     0       7 -0.0095      1.0000  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.0987   -0.0280     0.2524     9     0       5  0.2571      0.4263  1.0000
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0285   -0.0899     0.0507     5     0       9 -0.5429      0.0785  0.8634
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0524   -0.0262     0.1212    10     0       4  0.4857      0.1189  0.9512
```

### Scope: P1 only
Blocks (splits) = 10, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.653           0.013      3      4.60
RF 2k|msp           0.632           0.004      3      5.80
MLP 2k bin5|maha    0.606           0.025      3      7.30
RF 2k bin5|msp      0.601           0.031      3      7.90
DistilBERT|maha     0.571           0.038      3     10.60
MLP 2k bin5|knn     0.539           0.046      3     10.90
MLP full|maha       0.596           0.061      3     11.65
MLP 2k|maha         0.562           0.051      3     11.65
MLP 2k bin5|energy  0.479           0.032      3     12.00
SecBERT-kv|maha     0.490           0.050      3     12.20
SecBERT-kv|energy   0.442           0.028      3     12.30
MLP 2k|knn          0.494           0.104      3     12.50
SecBERT|maha        0.503           0.048      3     12.80
MLP full|energy     0.399           0.069      3     13.10
MLP full|knn        0.561           0.061      3     13.10
SecBERT-kv|knn      0.462           0.081      3     13.90
MLP 2k|energy       0.304           0.090      3     16.00
DistilBERT|knn      0.419           0.049      3     17.20
DistilBERT|energy   0.333           0.064      3     19.30
tiny-local|maha     0.393           0.050      3     19.30
tiny-local|knn      0.346           0.083      3     20.40
MLP 2k bin5|msp     0.276           0.058      3     20.50
MLP full|msp        0.218           0.066      3     20.90
SecBERT|knn         0.309           0.056      3     20.90
MLP 2k|msp          0.191           0.078      3     21.60
SecBERT-kv|msp      0.276           0.084      3     21.80
SecBERT|energy      0.227           0.058      3     22.80
tiny-local|energy   0.216           0.060      3     23.90
DistilBERT|msp      0.179           0.021      3     25.70
SecBERT|msp         0.153           0.081      3     26.10
tiny-local|msp      0.127           0.033      3     27.30
```

Friedman chi2 = 140.88, p = 2.71e-16. Nemenyi critical difference (alpha 0.05) = 15.31 ranks. Two combinations differ significantly when their average ranks differ by more than 15.31.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 28.78, p = 7.05e-04, Nemenyi CD = 4.28. Average ranks: RF full|msp 2.90, RF 2k|msp 3.50, MLP 2k bin5|maha 4.20, RF 2k bin5|msp 5.10, MLP full|maha 5.75, MLP 2k|maha 5.85, DistilBERT|maha 6.00, SecBERT-kv|maha 6.20, SecBERT|maha 6.60, tiny-local|maha 8.90

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.2130   -0.2972    -0.1277     0     0      10 -1.0000      0.0020  0.0332
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.2340   -0.3269    -0.1432     0     0      10 -1.0000      0.0020  0.0332
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0752   -0.2203     0.0645     4     0       6 -0.2727      0.4922  1.0000
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0726   -0.0415     0.2018     6     0       4  0.3818      0.3223  1.0000
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.1095   -0.0329     0.2644     7     0       3  0.4909      0.1934  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.1519    0.0709     0.2365     9     0       1  0.8909      0.0098  0.1465
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.1378   -0.2627    -0.0154     2     0       8 -0.6727      0.0645  0.6445
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0683   -0.0086     0.1558     6     0       4  0.4545      0.2324  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0611   -0.1054    -0.0249     1     0       9 -0.8909      0.0098  0.1465
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0821   -0.1682    -0.0165     1     0       9 -0.7091      0.0488  0.5371
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0084   -0.0802     0.1053     6     0       4 -0.0182      1.0000  1.0000
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.1282   -0.2750    -0.0126     1     1       8 -0.7333      0.0430  0.5156
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.1492   -0.3007    -0.0214     1     0       9 -0.7455      0.0371  0.4824
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0133   -0.1433     0.1039     4     0       6 -0.0909      0.8457  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.1532   -0.0165     0.3509     7     0       3  0.4909      0.1934  1.0000
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0302   -0.1128     0.0799     3     0       7 -0.5273      0.1602  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0435   -0.0592     0.1319     7     0       3  0.4182      0.2754  1.0000
```

### Scope: P1, NF-ToN-IoT-v3 only
Blocks (splits) = 7, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.538           0.020      3      5.57
RF 2k|msp           0.563           0.043      3      5.86
MLP 2k bin5|maha    0.553           0.072      3      6.71
RF 2k bin5|msp      0.524           0.048      3      7.00
SecBERT-kv|energy   0.529           0.038      3      7.43
MLP 2k bin5|knn     0.482           0.071      3     10.71
SecBERT-kv|maha     0.487           0.050      3     10.86
DistilBERT|maha     0.492           0.022      3     11.29
MLP 2k bin5|energy  0.446           0.021      3     11.43
MLP full|energy     0.387           0.085      3     11.71
SecBERT-kv|knn      0.488           0.032      3     12.00
MLP 2k|knn          0.437           0.132      3     12.57
MLP 2k|energy       0.318           0.071      3     13.86
SecBERT|maha        0.410           0.050      3     14.00
MLP full|knn        0.495           0.042      3     14.29
MLP 2k|maha         0.462           0.039      3     14.29
MLP full|maha       0.483           0.062      3     14.57
DistilBERT|energy   0.356           0.078      3     18.00
DistilBERT|knn      0.342           0.064      3     18.43
MLP 2k|msp          0.199           0.081      3     20.29
SecBERT-kv|msp      0.308           0.118      3     20.57
SecBERT|energy      0.249           0.035      3     21.43
MLP full|msp        0.169           0.044      3     21.57
tiny-local|maha     0.270           0.070      3     22.14
MLP 2k bin5|msp     0.200           0.055      3     22.57
tiny-local|knn      0.261           0.062      3     22.71
SecBERT|knn         0.234           0.004      3     22.86
tiny-local|energy   0.215           0.077      3     24.86
DistilBERT|msp      0.211           0.044      3     25.00
SecBERT|msp         0.170           0.064      3     25.14
tiny-local|msp      0.152           0.024      3     26.29
```

Friedman chi2 = 105.34, p = 2.62e-10. Nemenyi critical difference (alpha 0.05) = 18.30 ranks. Two combinations differ significantly when their average ranks differ by more than 18.30.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 25.54, p = 2.43e-03, Nemenyi CD = 5.12. Average ranks: RF full|msp 3.29, RF 2k|msp 3.43, MLP 2k bin5|maha 3.71, RF 2k bin5|msp 4.29, SecBERT-kv|maha 5.00, DistilBERT|maha 6.14, MLP 2k|maha 6.43, MLP full|maha 6.57, SecBERT|maha 6.71, tiny-local|maha 9.43

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.2210   -0.3147    -0.1245     0     0       7 -1.0000      0.0156  0.2656
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.1963   -0.3035    -0.0968     0     0       7 -1.0000      0.0156  0.2656
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0950   -0.2563     0.0672     2     0       5 -0.5000      0.2969  1.0000
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0807   -0.0070     0.2231     4     0       3  0.5000      0.2969  1.0000
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.1077   -0.0101     0.2787     5     0       2  0.5714      0.2188  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.1503    0.0511     0.2531     6     0       1  0.8571      0.0469  0.6562
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.1259   -0.2999     0.0376     2     0       5 -0.5714      0.2188  1.0000
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0254   -0.0495     0.1086     3     0       4  0.0714      0.9375  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0707   -0.1292    -0.0221     1     0       6 -0.8571      0.0469  0.6562
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0461   -0.0884     0.0113     1     0       6 -0.5714      0.2188  1.0000
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0298   -0.0795     0.1524     5     0       2  0.2143      0.6875  1.0000
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.1525   -0.3557     0.0079     1     0       6 -0.6429      0.1562  1.0000
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.1278   -0.3011     0.0041     1     0       6 -0.6429      0.1562  1.0000
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization     0.0767    0.0066     0.1809     4     0       3  0.5714      0.2188  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.2540    0.0621     0.4853     6     0       1  0.9286      0.0312  0.4688
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0391   -0.0691    -0.0123     2     0       5 -0.7857      0.0781  0.9375
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0903    0.0194     0.1733     6     0       1  0.7857      0.0781  0.9375
```

### Scope: P1, NF-BoT-IoT-v3 only
Blocks (splits) = 3, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.919           0.007      3      2.33
MLP full|maha       0.862           0.061      3      4.83
MLP 2k|maha         0.795           0.079      3      5.50
RF 2k|msp           0.792           0.110      3      5.67
MLP 2k bin5|maha    0.729           0.087      3      8.67
DistilBERT|maha     0.753           0.155      3      9.00
SecBERT|maha        0.720           0.090      3     10.00
RF 2k bin5|msp      0.782           0.096      3     10.00
MLP full|knn        0.714           0.162      3     10.33
MLP 2k bin5|knn     0.673           0.013      3     11.33
MLP 2k|knn          0.627           0.092      3     12.33
tiny-local|maha     0.680           0.026      3     12.67
MLP 2k bin5|energy  0.554           0.068      3     13.33
DistilBERT|knn      0.598           0.219      3     14.33
tiny-local|knn      0.544           0.215      3     15.00
SecBERT-kv|maha     0.497           0.052      3     15.33
MLP 2k bin5|msp     0.451           0.065      3     15.67
MLP full|energy     0.426           0.150      3     16.33
SecBERT|knn         0.484           0.190      3     16.33
SecBERT-kv|knn      0.402           0.199      3     18.33
MLP full|msp        0.333           0.134      3     19.33
MLP 2k|energy       0.272           0.169      3     21.00
tiny-local|energy   0.219           0.140      3     21.67
DistilBERT|energy   0.280           0.119      3     22.33
SecBERT-kv|energy   0.240           0.009      3     23.67
MLP 2k|msp          0.173           0.104      3     24.67
SecBERT-kv|msp      0.200           0.014      3     24.67
SecBERT|energy      0.174           0.116      3     26.00
DistilBERT|msp      0.104           0.051      3     27.33
SecBERT|msp         0.114           0.125      3     28.33
tiny-local|msp      0.070           0.055      3     29.67
```

Friedman chi2 = 61.12, p = 6.73e-04. Nemenyi critical difference (alpha 0.05) = 27.95 ranks. Two combinations differ significantly when their average ranks differ by more than 27.95.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 13.00, p = 1.62e-01, Nemenyi CD = 7.82. Average ranks: RF full|msp 2.00, RF 2k|msp 3.67, MLP full|maha 3.83, MLP 2k|maha 4.50, MLP 2k bin5|maha 5.33, DistilBERT|maha 5.67, SecBERT|maha 6.33, RF 2k bin5|msp 7.00, tiny-local|maha 7.67, SecBERT-kv|maha 9.00

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.1943   -0.3970    -0.0444     0     0       3 -1.0000        0.25     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.3218   -0.4196    -0.1415     0     0       3 -1.0000        0.25     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0289   -0.3820     0.1477     2     0       1  0.0000        1.00     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0536   -0.2360     0.3874     2     0       1  0.3333        0.75     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.1137   -0.2809     0.4714     2     0       1  0.3333        0.75     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.1557    0.0193     0.3071     3     0       0  1.0000        0.25     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.1654   -0.2892    -0.0150     0     0       3 -1.0000        0.25     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.1684    0.0187     0.3312     3     0       0  1.0000        0.25     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0386   -0.0899    -0.0009     0     0       3 -1.0000        0.25     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.1661   -0.4003    -0.0007     0     0       3 -1.0000        0.25     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0416   -0.1642     0.1330     1     0       2 -0.3333        0.75     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0714   -0.1936     0.0000     0     1       2 -1.0000        0.50     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.1990   -0.5688    -0.0075     0     0       3 -1.0000        0.25     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.2231   -0.4672    -0.0637     0     0       3 -1.0000        0.25     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0821   -0.1873     0.0849     1     0       2 -0.6667        0.50     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0096   -0.2172     0.3806     1     0       2  0.0000        1.00     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0658   -0.3261     0.1324     1     0       2 -0.3333        0.75     1.0
```

Note: with 3 blocks the smallest attainable two-sided Wilcoxon p-value is 0.250; treat this scope as descriptive.

### Scope: P3 only
Blocks (splits) = 4, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
MLP 2k bin5|energy  0.175           0.073      3      8.00
MLP full|knn        0.129           0.049      3      9.50
SecBERT-kv|knn      0.091           0.051      3     11.75
SecBERT-kv|maha     0.099           0.066      3     12.00
SecBERT|energy      0.137           0.128      3     12.00
RF full|msp         0.118           0.009      3     12.50
tiny-local|msp      0.119           0.027      3     12.75
tiny-local|knn      0.038           0.021      3     12.75
tiny-local|energy   0.100           0.052      3     12.75
MLP 2k bin5|knn     0.171           0.096      3     13.50
tiny-local|maha     0.115           0.058      3     14.50
MLP 2k|energy       0.042           0.025      3     14.50
MLP 2k|knn          0.073           0.013      3     14.50
DistilBERT|energy   0.137           0.055      3     15.00
RF 2k bin5|msp      0.073           0.069      3     15.50
MLP full|msp        0.042           0.022      3     16.00
MLP 2k bin5|maha    0.098           0.091      3     16.00
MLP full|energy     0.061           0.034      3     16.25
SecBERT-kv|energy   0.064           0.018      3     16.75
SecBERT|knn         0.128           0.077      3     17.00
MLP 2k bin5|msp     0.087           0.051      3     17.00
MLP full|maha       0.121           0.078      3     17.75
MLP 2k|msp          0.053           0.029      3     17.75
SecBERT-kv|msp      0.035           0.016      3     18.50
RF 2k|msp           0.097           0.014      3     19.50
SecBERT|maha        0.129           0.043      3     19.75
DistilBERT|knn      0.108           0.040      3     20.00
DistilBERT|msp      0.016           0.008      3     21.00
SecBERT|msp         0.016           0.009      3     22.25
DistilBERT|maha     0.114           0.032      3     23.25
MLP 2k|maha         0.024           0.004      3     25.75
```

Friedman chi2 = 23.40, p = 7.99e-01. Nemenyi critical difference (alpha 0.05) = 24.20 ranks. Two combinations differ significantly when their average ranks differ by more than 24.20.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 8.56, p = 4.78e-01, Nemenyi CD = 6.77. Average ranks: RF full|msp 3.75, SecBERT-kv|maha 3.75, tiny-local|maha 4.50, MLP full|maha 5.00, RF 2k bin5|msp 5.00, MLP 2k bin5|maha 5.25, RF 2k|msp 5.75, SecBERT|maha 6.25, DistilBERT|maha 7.75, MLP 2k|maha 8.00

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses  r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0116   -0.1639     0.2007     1     0       3  -0.2       0.875     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0091   -0.2040     0.1939     1     0       3  -0.4       0.625     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0358   -0.0572     0.1803     1     0       3  -0.2       0.875     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0703   -0.0308     0.1906     2     0       2   0.4       0.625     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.0199   -0.1665     0.1106     2     0       2  -0.2       0.875     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0058   -0.0742     0.0919     2     0       2   0.0       1.000     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.0243   -0.1025     0.0219     3     0       1   0.2       0.875     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)    -0.0490   -0.1159    -0.0086     0     0       4  -1.0       0.125     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0173   -0.2386     0.2932     1     0       3  -0.2       0.875     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0033   -0.2787     0.2864     1     0       3  -0.2       0.875     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0906   -0.0205     0.2963     1     0       3  -0.2       0.875     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.0324   -0.1169     0.2133     2     0       2   0.2       0.875     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data     0.0117   -0.1582     0.2078     1     0       3  -0.2       0.875     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0304   -0.1606     0.0525     3     0       1   0.2       0.875     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0375   -0.0911     0.0161     2     0       2  -0.4       0.625     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0243   -0.0768     0.0106     2     0       2  -0.4       0.625     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0748   -0.0019     0.1516     3     0       1   0.6       0.375     1.0
```

Note: with 4 blocks the smallest attainable two-sided Wilcoxon p-value is 0.125; treat this scope as descriptive.
