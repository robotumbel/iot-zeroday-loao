# Statistical comparison — metric `auroc_ood`, rule `target_warmup_far0.01`, warm-up contamination 0, seeds [0, 1, 2]


### Scope: all splits (P1 + P3)
Blocks (splits) = 14, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
MLP full|maha       0.789           0.004      3      7.79
MLP full|knn        0.786           0.015      3      8.43
MLP 2k|maha         0.772           0.003      3      8.64
MLP 2k|knn          0.769           0.015      3      9.50
MLP 2k bin5|maha    0.781           0.010      3      9.57
RF full|msp         0.795           0.012      3      9.71
RF 2k|msp           0.781           0.006      3     10.36
MLP 2k bin5|knn     0.774           0.012      3     10.93
SecBERT-kv|maha     0.741           0.011      3     12.64
RF 2k bin5|msp      0.772           0.000      3     12.79
DistilBERT|maha     0.751           0.006      3     13.86
SecBERT|maha        0.755           0.004      3     14.36
SecBERT-kv|knn      0.729           0.019      3     15.00
DistilBERT|knn      0.741           0.004      3     15.71
SecBERT|knn         0.748           0.009      3     15.79
DistilBERT|energy   0.705           0.022      3     15.86
MLP 2k bin5|energy  0.696           0.024      3     16.64
tiny-local|knn      0.727           0.004      3     18.07
SecBERT-kv|energy   0.681           0.007      3     18.71
tiny-local|maha     0.703           0.025      3     18.93
MLP full|msp        0.657           0.050      3     19.00
SecBERT|energy      0.692           0.019      3     19.14
MLP 2k bin5|msp     0.671           0.039      3     19.79
MLP 2k|msp          0.644           0.010      3     20.07
DistilBERT|msp      0.664           0.019      3     20.14
MLP full|energy     0.616           0.026      3     20.14
MLP 2k|energy       0.601           0.034      3     20.64
SecBERT-kv|msp      0.626           0.024      3     22.14
tiny-local|energy   0.620           0.049      3     22.71
SecBERT|msp         0.634           0.032      3     23.36
tiny-local|msp      0.538           0.013      3     25.57
```

Friedman chi2 = 126.08, p = 9.60e-14. Nemenyi critical difference (alpha 0.05) = 12.94 ranks. Two combinations differ significantly when their average ranks differ by more than 12.94.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 22.69, p = 6.93e-03, Nemenyi CD = 3.62. Average ranks: MLP full|maha 3.86, MLP 2k bin5|maha 4.21, MLP 2k|maha 4.29, RF 2k|msp 4.86, RF full|msp 4.86, SecBERT-kv|maha 5.86, DistilBERT|maha 6.14, RF 2k bin5|msp 6.21, SecBERT|maha 7.00, tiny-local|maha 7.71

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.0399   -0.1135     0.0251     4     0      10 -0.5619      0.0676  0.8115
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0532   -0.1306     0.0038     2     0      12 -0.6000      0.0494  0.7910
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0278   -0.0802     0.0442     3     0      11 -0.5810      0.0580  0.7910
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0148   -0.0471     0.0576    12     0       2  0.6952      0.0203  0.3445
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.0066   -0.0377     0.0221     7     0       7 -0.0095      1.0000  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0096   -0.0116     0.0297    10     0       4  0.2952      0.3575  1.0000
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.0120   -0.0574     0.0270     8     0       6 -0.0095      1.0000  1.0000
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0028   -0.0154     0.0216     8     0       6  0.0857      0.8077  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0302   -0.1108     0.0402     4     0      10 -0.6000      0.0494  0.7910
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0435   -0.1284     0.0180     5     0       9 -0.4095      0.1937  1.0000
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0210   -0.0718     0.0475     4     0      10 -0.5619      0.0676  0.8115
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0262   -0.0997     0.0431     5     0       9 -0.5238      0.0906  0.9058
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.0395   -0.1168     0.0185     3     0      11 -0.6000      0.0494  0.7910
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0146   -0.0705     0.0214     9     0       5  0.1619      0.6257  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0188   -0.0771     0.0257     8     0       6  0.1048      0.7609  1.0000
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0098   -0.0463     0.0242     6     0       8 -0.1429      0.6698  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0090   -0.0329     0.0579     7     0       7 -0.0476      0.9032  1.0000
```

### Scope: P1 only
Blocks (splits) = 10, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
MLP full|maha       0.900           0.005      3       5.7
MLP 2k|maha         0.896           0.001      3       6.4
MLP full|knn        0.896           0.003      3       6.5
MLP 2k bin5|maha    0.875           0.006      3       7.9
MLP 2k|knn          0.888           0.005      3       7.9
RF full|msp         0.880           0.006      3       8.0
RF 2k|msp           0.877           0.014      3       8.6
DistilBERT|maha     0.860           0.005      3      11.3
SecBERT-kv|maha     0.862           0.009      3      11.3
MLP 2k bin5|knn     0.861           0.004      3      11.5
RF 2k bin5|msp      0.867           0.009      3      11.9
SecBERT-kv|knn      0.859           0.011      3      12.7
SecBERT|maha        0.853           0.007      3      13.1
DistilBERT|knn      0.838           0.003      3      16.4
DistilBERT|energy   0.809           0.021      3      16.8
SecBERT-kv|energy   0.808           0.014      3      17.1
SecBERT|knn         0.834           0.008      3      17.3
MLP 2k bin5|energy  0.763           0.014      3      18.0
MLP 2k bin5|msp     0.756           0.035      3      19.6
SecBERT|energy      0.772           0.012      3      19.9
tiny-local|knn      0.807           0.009      3      20.0
DistilBERT|msp      0.769           0.017      3      20.5
SecBERT-kv|msp      0.771           0.023      3      20.6
tiny-local|maha     0.769           0.022      3      21.2
MLP 2k|msp          0.724           0.020      3      21.6
MLP full|energy     0.692           0.011      3      21.6
MLP full|msp        0.716           0.038      3      21.8
MLP 2k|energy       0.687           0.032      3      21.9
SecBERT|msp         0.738           0.022      3      23.4
tiny-local|energy   0.651           0.068      3      26.9
tiny-local|msp      0.581           0.021      3      28.6
```

Friedman chi2 = 147.92, p = 1.56e-17. Nemenyi critical difference (alpha 0.05) = 15.31 ranks. Two combinations differ significantly when their average ranks differ by more than 15.31.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 31.68, p = 2.26e-04, Nemenyi CD = 4.28. Average ranks: MLP full|maha 3.70, MLP 2k|maha 3.90, MLP 2k bin5|maha 4.00, RF 2k|msp 4.40, RF full|msp 4.50, SecBERT-kv|maha 5.60, DistilBERT|maha 5.80, RF 2k bin5|msp 6.50, SecBERT|maha 7.30, tiny-local|maha 9.30

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.0396   -0.0621    -0.0195     2     0       8 -0.8909      0.0098  0.1465
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0424   -0.0674    -0.0230     0     0      10 -1.0000      0.0020  0.0332
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0501   -0.0772    -0.0225     1     0       9 -0.8545      0.0137  0.1777
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0310    0.0180     0.0435     9     0       1  0.9273      0.0059  0.0938
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0034   -0.0161     0.0259     5     0       5  0.0545      0.9219  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0225    0.0055     0.0383     9     0       1  0.7091      0.0488  0.5371
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0105   -0.0143     0.0411     6     0       4  0.1273      0.7695  1.0000
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0086   -0.0056     0.0261     7     0       3  0.3455      0.3750  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0171   -0.0269    -0.0069     2     0       8 -0.8545      0.0137  0.1777
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0199   -0.0417    -0.0026     3     0       7 -0.6000      0.1055  0.7383
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0362   -0.0682    -0.0092     3     0       7 -0.6727      0.0645  0.5801
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0245   -0.0413    -0.0068     3     0       7 -0.7091      0.0488  0.5371
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.0272   -0.0500    -0.0095     1     0       9 -0.8909      0.0098  0.1465
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization     0.0090   -0.0072     0.0285     7     0       3  0.2727      0.4922  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.0250    0.0041     0.0488     7     0       3  0.6364      0.0840  0.6719
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0102   -0.0540     0.0300     3     0       7 -0.1636      0.6953  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0213   -0.0546     0.0012     5     0       5 -0.2364      0.5566  1.0000
```

### Scope: P1, NF-ToN-IoT-v3 only
Blocks (splits) = 7, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
MLP full|maha       0.868           0.007      3      4.71
MLP full|knn        0.865           0.004      3      4.86
MLP 2k|maha         0.867           0.001      3      5.71
MLP 2k bin5|maha    0.856           0.007      3      6.14
RF 2k|msp           0.855           0.000      3      6.43
MLP 2k|knn          0.855           0.007      3      7.29
RF full|msp         0.848           0.007      3      8.57
SecBERT-kv|maha     0.840           0.004      3      9.86
SecBERT-kv|knn      0.835           0.007      3     10.29
RF 2k bin5|msp      0.830           0.010      3     10.86
DistilBERT|maha     0.833           0.007      3     11.29
MLP 2k bin5|knn     0.831           0.002      3     11.43
SecBERT|maha        0.825           0.011      3     13.00
DistilBERT|energy   0.785           0.018      3     16.43
DistilBERT|knn      0.799           0.009      3     17.00
SecBERT-kv|energy   0.780           0.016      3     17.00
SecBERT|knn         0.796           0.010      3     17.71
MLP 2k bin5|energy  0.747           0.025      3     18.57
SecBERT|energy      0.757           0.019      3     18.86
DistilBERT|msp      0.740           0.018      3     20.43
tiny-local|knn      0.757           0.020      3     21.43
MLP 2k bin5|msp     0.704           0.055      3     21.57
SecBERT-kv|msp      0.735           0.029      3     21.57
MLP 2k|msp          0.678           0.046      3     22.29
MLP 2k|energy       0.659           0.050      3     22.29
MLP full|energy     0.666           0.029      3     22.57
SecBERT|msp         0.715           0.024      3     23.00
MLP full|msp        0.666           0.046      3     23.43
tiny-local|maha     0.716           0.042      3     23.71
tiny-local|energy   0.617           0.093      3     28.29
tiny-local|msp      0.574           0.056      3     29.43
```

Friedman chi2 = 133.32, p = 5.55e-15. Nemenyi critical difference (alpha 0.05) = 18.30 ranks. Two combinations differ significantly when their average ranks differ by more than 18.30.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 34.79, p = 6.48e-05, Nemenyi CD = 5.12. Average ranks: MLP full|maha 2.86, MLP 2k|maha 3.43, MLP 2k bin5|maha 3.57, RF 2k|msp 3.71, SecBERT-kv|maha 5.43, RF full|msp 5.43, RF 2k bin5|msp 6.14, DistilBERT|maha 6.57, SecBERT|maha 7.86, tiny-local|maha 10.00

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.0561   -0.0785    -0.0382     0     0       7 -1.0000      0.0156  0.2656
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0498   -0.0807    -0.0270     0     0       7 -1.0000      0.0156  0.2656
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0565   -0.0798    -0.0312     0     0       7 -1.0000      0.0156  0.2656
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0420    0.0323     0.0522     7     0       0  1.0000      0.0156  0.2656
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0031   -0.0229     0.0340     4     0       3  0.0714      0.9375  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0345    0.0228     0.0495     7     0       0  1.0000      0.0156  0.2656
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0003   -0.0222     0.0227     4     0       3  0.0000      1.0000  1.0000
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0116   -0.0078     0.0358     5     0       2  0.3571      0.4688  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0217   -0.0308    -0.0126     0     0       7 -1.0000      0.0156  0.2656
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0153   -0.0324    -0.0003     2     0       5 -0.6429      0.1562  1.0000
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0336   -0.0582    -0.0116     1     0       6 -0.8571      0.0469  0.4219
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0293   -0.0483    -0.0072     1     0       6 -0.7857      0.0781  0.6250
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.0229   -0.0383    -0.0084     1     0       6 -0.9286      0.0312  0.3438
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization     0.0147   -0.0052     0.0398     5     0       2  0.5000      0.2969  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.0395    0.0162     0.0651     6     0       1  0.9286      0.0312  0.3438
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0246   -0.0772     0.0143     2     0       5 -0.2143      0.6875  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0105   -0.0272     0.0030     3     0       4 -0.2857      0.5781  1.0000
```

### Scope: P1, NF-BoT-IoT-v3 only
Blocks (splits) = 3, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.954           0.003      3      6.67
MLP full|maha       0.974           0.004      3      8.00
MLP 2k|maha         0.966           0.002      3      8.00
MLP 2k|knn          0.964           0.003      3      9.33
MLP full|knn        0.968           0.001      3     10.33
DistilBERT|maha     0.924           0.001      3     11.33
MLP 2k bin5|knn     0.930           0.011      3     11.67
MLP 2k bin5|maha    0.920           0.009      3     12.00
SecBERT|maha        0.917           0.005      3     13.33
RF 2k|msp           0.930           0.046      3     13.67
RF 2k bin5|msp      0.953           0.018      3     14.33
SecBERT-kv|maha     0.912           0.021      3     14.67
MLP 2k bin5|msp     0.878           0.015      3     15.00
DistilBERT|knn      0.929           0.012      3     15.00
tiny-local|maha     0.892           0.044      3     15.33
SecBERT|knn         0.925           0.006      3     16.33
MLP 2k bin5|energy  0.798           0.019      3     16.67
tiny-local|knn      0.924           0.017      3     16.67
SecBERT-kv|energy   0.871           0.013      3     17.33
DistilBERT|energy   0.867           0.030      3     17.67
MLP full|msp        0.831           0.020      3     18.00
SecBERT-kv|knn      0.917           0.021      3     18.33
SecBERT-kv|msp      0.855           0.012      3     18.33
MLP full|energy     0.751           0.034      3     19.33
MLP 2k|msp          0.830           0.040      3     20.00
DistilBERT|msp      0.837           0.013      3     20.67
MLP 2k|energy       0.752           0.018      3     21.00
SecBERT|energy      0.807           0.020      3     22.33
tiny-local|energy   0.729           0.086      3     23.67
SecBERT|msp         0.792           0.026      3     24.33
tiny-local|msp      0.596           0.067      3     26.67
```

Friedman chi2 = 27.01, p = 6.23e-01. Nemenyi critical difference (alpha 0.05) = 27.95 ranks. Two combinations differ significantly when their average ranks differ by more than 27.95.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 7.07, p = 6.30e-01, Nemenyi CD = 7.82. Average ranks: RF full|msp 2.33, DistilBERT|maha 4.00, MLP 2k|maha 5.00, MLP 2k bin5|maha 5.00, MLP full|maha 5.67, RF 2k|msp 6.00, SecBERT-kv|maha 6.00, SecBERT|maha 6.00, RF 2k bin5|msp 7.33, tiny-local|maha 7.67

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.0011   -0.0062     0.0028     2     0       1  0.0000        1.00     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0251   -0.0588    -0.0067     0     0       3 -1.0000        0.25     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0352   -0.1178     0.0189     1     0       2 -0.3333        0.75     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0053   -0.0072     0.0188     2     0       1  0.3333        0.75     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0040   -0.0149     0.0281     1     0       2  0.0000        1.00     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score    -0.0055   -0.0349     0.0109     2     0       1  0.0000        1.00     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0341   -0.0186     0.1206     2     0       1  0.3333        0.75     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0016   -0.0086     0.0127     2     0       1  0.3333        0.75     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0066   -0.0321     0.0112     2     0       1  0.0000        1.00     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.0306   -0.0938     0.0042     1     0       2 -0.3333        0.75     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0423   -0.1442     0.0171     2     0       1  0.0000        1.00     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0132   -0.0451     0.0044     2     0       1  0.0000        1.00     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.0373   -0.1067    -0.0025     0     0       3 -1.0000        0.25     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0045   -0.0280     0.0136     2     0       1  0.0000        1.00     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0086   -0.0268     0.0013     1     0       2 -0.3333        0.75     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0233   -0.0316     0.1139     1     0       2  0.0000        1.00     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0464   -0.1488     0.0073     2     0       1  0.0000        1.00     1.0
```

Note: with 3 blocks the smallest attainable two-sided Wilcoxon p-value is 0.250; treat this scope as descriptive.

### Scope: P3 only
Blocks (splits) = 4, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
MLP 2k bin5|knn     0.556           0.052      3      9.50
MLP full|msp        0.511           0.081      3     12.00
SecBERT|knn         0.532           0.018      3     12.00
tiny-local|energy   0.542           0.027      3     12.25
MLP full|maha       0.510           0.022      3     13.00
tiny-local|knn      0.526           0.028      3     13.25
MLP full|knn        0.513           0.052      3     13.25
MLP 2k bin5|energy  0.530           0.052      3     13.25
tiny-local|maha     0.538           0.061      3     13.25
MLP 2k|knn          0.473           0.053      3     13.50
DistilBERT|energy   0.443           0.024      3     13.50
MLP 2k bin5|maha    0.546           0.027      3     13.75
DistilBERT|knn      0.501           0.021      3     14.00
RF full|msp         0.581           0.026      3     14.00
MLP 2k|maha         0.461           0.008      3     14.25
RF 2k|msp           0.541           0.013      3     14.75
RF 2k bin5|msp      0.532           0.023      3     15.00
SecBERT-kv|maha     0.437           0.018      3     16.00
MLP 2k|msp          0.446           0.017      3     16.25
MLP full|energy     0.428           0.062      3     16.50
SecBERT|energy      0.493           0.061      3     17.25
SecBERT|maha        0.511           0.009      3     17.50
MLP 2k|energy       0.385           0.065      3     17.50
tiny-local|msp      0.430           0.080      3     18.00
DistilBERT|msp      0.400           0.032      3     19.25
MLP 2k bin5|msp     0.457           0.049      3     20.25
DistilBERT|maha     0.478           0.014      3     20.25
SecBERT-kv|knn      0.404           0.038      3     20.75
SecBERT-kv|energy   0.366           0.040      3     22.75
SecBERT|msp         0.373           0.127      3     23.25
SecBERT-kv|msp      0.264           0.063      3     26.00
```

Friedman chi2 = 21.12, p = 8.84e-01. Nemenyi critical difference (alpha 0.05) = 24.20 ranks. Two combinations differ significantly when their average ranks differ by more than 24.20.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 4.09, p = 9.05e-01, Nemenyi CD = 6.77. Average ranks: tiny-local|maha 3.75, MLP full|maha 4.25, MLP 2k bin5|maha 4.75, MLP 2k|maha 5.25, RF 2k bin5|msp 5.50, RF full|msp 5.75, RF 2k|msp 6.00, SecBERT|maha 6.25, SecBERT-kv|maha 6.50, DistilBERT|maha 7.00

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses  r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.0405   -0.3026     0.1734     2     0       2   0.0       1.000     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0801   -0.3529     0.0926     2     0       2   0.0       1.000     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0278   -0.1375     0.2540     2     0       2   0.0       1.000     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining    -0.0257   -0.2327     0.1208     3     0       1   0.2       0.875     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.0316   -0.1113     0.0480     2     0       2  -0.2       0.875     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score    -0.0225   -0.0685     0.0289     1     0       3  -0.4       0.625     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.0683   -0.1775     0.0408     2     0       2  -0.4       0.625     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)    -0.0118   -0.0579     0.0372     1     0       3  -0.4       0.625     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0630   -0.3273     0.1898     2     0       2  -0.2       0.875     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.1026   -0.3775     0.1090     2     0       2  -0.2       0.875     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0171   -0.1300     0.2332     1     0       3  -0.2       0.875     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.0305   -0.2899     0.2165     2     0       2  -0.2       0.875     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.0701   -0.3401     0.1357     2     0       2  -0.2       0.875     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0736   -0.2431     0.0342     2     0       2   0.0       1.000     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.1284   -0.2392    -0.0185     1     0       3  -0.8       0.250     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0087   -0.0833     0.0504     3     0       1   0.2       0.875     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0847   -0.0173     0.1914     2     0       2   0.4       0.625     1.0
```

Note: with 4 blocks the smallest attainable two-sided Wilcoxon p-value is 0.125; treat this scope as descriptive.
