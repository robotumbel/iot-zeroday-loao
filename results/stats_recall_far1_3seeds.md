# Statistical comparison — metric `unknown_recall`, rule `target_warmup_far0.01`, warm-up contamination 0, seeds [0, 1, 2]


### Scope: all splits (P1 + P3)
Blocks (splits) = 14, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.318           0.038      3      6.21
RF 2k bin5|msp      0.234           0.038      3      6.93
RF 2k|msp           0.252           0.034      3     10.46
MLP 2k bin5|maha    0.228           0.026      3     11.36
MLP full|knn        0.208           0.045      3     11.79
SecBERT-kv|maha     0.178           0.044      3     12.07
MLP full|energy     0.132           0.066      3     12.21
MLP 2k bin5|energy  0.131           0.050      3     12.75
MLP full|maha       0.202           0.024      3     14.14
MLP 2k|knn          0.133           0.070      3     14.14
SecBERT-kv|knn      0.143           0.040      3     16.00
SecBERT-kv|energy   0.138           0.037      3     16.00
MLP full|msp        0.075           0.043      3     16.11
MLP 2k bin5|knn     0.156           0.043      3     16.14
MLP 2k|msp          0.065           0.021      3     16.21
SecBERT|maha        0.140           0.014      3     16.25
MLP 2k|maha         0.178           0.023      3     16.29
DistilBERT|energy   0.091           0.024      3     17.14
DistilBERT|maha     0.192           0.056      3     17.18
MLP 2k|energy       0.056           0.024      3     17.21
MLP 2k bin5|msp     0.084           0.009      3     17.39
SecBERT-kv|msp      0.093           0.033      3     17.79
tiny-local|maha     0.087           0.036      3     18.14
SecBERT|msp         0.072           0.042      3     18.50
DistilBERT|knn      0.092           0.070      3     19.25
tiny-local|msp      0.039           0.006      3     19.71
SecBERT|energy      0.039           0.017      3     20.14
SecBERT|knn         0.057           0.015      3     20.93
DistilBERT|msp      0.049           0.018      3     21.43
tiny-local|knn      0.052           0.018      3     21.46
tiny-local|energy   0.045           0.028      3     24.64
```

Friedman chi2 = 87.30, p = 1.68e-07. Nemenyi critical difference (alpha 0.05) = 12.94 ranks. Two combinations differ significantly when their average ranks differ by more than 12.94.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 29.22, p = 5.95e-04, Nemenyi CD = 3.62. Average ranks: RF full|msp 2.93, RF 2k bin5|msp 3.93, RF 2k|msp 4.29, SecBERT-kv|maha 5.07, MLP 2k bin5|maha 5.21, MLP full|maha 6.14, MLP 2k|maha 6.43, SecBERT|maha 6.71, DistilBERT|maha 6.86, tiny-local|maha 7.43

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.1593   -0.3025    -0.0524     2     0      12 -0.8476      0.0031  0.0488
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.2258   -0.3644    -0.1094     1     0      13 -0.9238      0.0009  0.0145
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0409   -0.1269     0.0423     4     0      10 -0.4286      0.1726  1.0000
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0400   -0.0084     0.0910     9     0       5  0.3905      0.2166  1.0000
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0356   -0.0322     0.1073     8     0       6  0.2571      0.4263  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0993    0.0280     0.1879     9     1       4  0.6044      0.0597  0.7756
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.1183   -0.2546    -0.0034     7     0       7 -0.3714      0.2412  1.0000
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0445   -0.0115     0.1180     7     0       7  0.1619      0.6257  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.0600   -0.2053     0.0860     3     0      11 -0.5048      0.1040  1.0000
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.1265   -0.2654     0.0112     2     0      12 -0.6000      0.0494  0.6921
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0139   -0.0925     0.1183     5     0       9 -0.1048      0.7609  1.0000
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.1122   -0.2536     0.0102     4     0      10 -0.5238      0.0906  1.0000
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.1787   -0.3024    -0.0641     1     0      13 -0.8476      0.0031  0.0488
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization     0.0384   -0.0882     0.1671     9     0       5  0.2952      0.3575  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.0858   -0.0212     0.2356     8     0       6  0.1619      0.6257  1.0000
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0179   -0.0834     0.0437     9     0       5 -0.0667      0.8552  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0497   -0.0059     0.1168     8     0       6  0.3714      0.2412  1.0000
```

### Scope: P1 only
Blocks (splits) = 10, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.408           0.049      3      3.70
RF 2k|msp           0.346           0.048      3      5.05
RF 2k bin5|msp      0.315           0.063      3      5.40
MLP 2k bin5|maha    0.302           0.038      3      9.70
SecBERT-kv|maha     0.236           0.052      3     11.40
MLP full|maha       0.268           0.039      3     12.50
MLP full|knn        0.254           0.065      3     12.50
MLP full|energy     0.173           0.086      3     12.60
MLP 2k|maha         0.245           0.033      3     13.70
MLP 2k bin5|energy  0.157           0.057      3     13.85
SecBERT-kv|energy   0.190           0.051      3     14.00
MLP 2k bin5|knn     0.197           0.063      3     15.30
DistilBERT|maha     0.229           0.075      3     15.50
MLP 2k|knn          0.172           0.095      3     16.10
SecBERT|maha        0.169           0.025      3     16.10
SecBERT-kv|knn      0.187           0.046      3     16.60
MLP full|msp        0.097           0.054      3     16.65
MLP 2k bin5|msp     0.110           0.008      3     16.70
MLP 2k|msp          0.081           0.035      3     17.30
SecBERT-kv|msp      0.127           0.045      3     18.00
SecBERT|msp         0.099           0.059      3     18.20
MLP 2k|energy       0.075           0.032      3     18.20
DistilBERT|knn      0.120           0.093      3     18.60
DistilBERT|energy   0.096           0.009      3     18.90
tiny-local|maha     0.106           0.033      3     20.00
DistilBERT|msp      0.066           0.025      3     21.00
SecBERT|energy      0.050           0.021      3     21.70
tiny-local|knn      0.072           0.024      3     22.55
tiny-local|msp      0.033           0.021      3     24.10
SecBERT|knn         0.046           0.012      3     24.10
tiny-local|energy   0.059           0.039      3     26.00
```

Friedman chi2 = 105.80, p = 2.21e-10. Nemenyi critical difference (alpha 0.05) = 15.31 ranks. Two combinations differ significantly when their average ranks differ by more than 15.31.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 35.98, p = 4.00e-05, Nemenyi CD = 4.28. Average ranks: RF full|msp 2.50, RF 2k|msp 3.10, RF 2k bin5|msp 4.00, MLP 2k bin5|maha 5.00, SecBERT-kv|maha 5.20, MLP 2k|maha 6.10, MLP full|maha 6.40, DistilBERT|maha 6.90, SecBERT|maha 7.20, tiny-local|maha 8.60

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.2253   -0.4030    -0.0935     0     0      10 -1.0000      0.0020  0.0332
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.2874   -0.4488    -0.1585     0     0      10 -1.0000      0.0020  0.0332
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0515   -0.1704     0.0660     4     0       6 -0.3455      0.3750  1.0000
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0488   -0.0198     0.1191     7     0       3  0.4545      0.2324  1.0000
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0747    0.0002     0.1571     8     0       2  0.6000      0.1055  0.9492
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.1092    0.0254     0.2194     7     0       3  0.6727      0.0645  0.7734
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.1739   -0.3494    -0.0217     3     0       7 -0.6364      0.0840  0.8398
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0734   -0.0009     0.1689     7     0       3  0.5636      0.1309  1.0000
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.1162   -0.2968     0.0650     1     0       9 -0.6727      0.0645  0.7734
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.1782   -0.3349    -0.0323     1     0       9 -0.7455      0.0371  0.5195
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0158   -0.1499     0.1098     4     0       6 -0.1636      0.6953  1.0000
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.1771   -0.3559    -0.0206     1     0       9 -0.7455      0.0371  0.5195
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.2392   -0.3796    -0.1146     0     0      10 -1.0000      0.0020  0.0332
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization     0.0673   -0.1060     0.2385     7     0       3  0.5273      0.1602  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.1414    0.0060     0.3356     6     0       4  0.4182      0.2754  1.0000
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0307   -0.1210     0.0557     5     0       5 -0.3091      0.4316  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0569   -0.0181     0.1485     6     0       4  0.3091      0.4316  1.0000
```

### Scope: P1, NF-ToN-IoT-v3 only
Blocks (splits) = 7, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF 2k|msp           0.369           0.066      3      3.71
RF 2k bin5|msp      0.305           0.088      3      4.29
RF full|msp         0.347           0.042      3      4.57
MLP 2k bin5|maha    0.268           0.026      3     10.29
SecBERT-kv|maha     0.255           0.041      3     10.86
SecBERT-kv|energy   0.229           0.059      3     11.71
MLP full|energy     0.139           0.067      3     13.43
MLP full|maha       0.248           0.028      3     14.29
MLP 2k bin5|energy  0.131           0.045      3     14.29
MLP full|knn        0.228           0.085      3     15.00
SecBERT-kv|knn      0.243           0.051      3     15.43
MLP 2k|maha         0.206           0.021      3     15.71
MLP 2k bin5|knn     0.167           0.068      3     16.00
SecBERT|msp         0.106           0.038      3     16.14
MLP 2k|msp          0.092           0.053      3     16.14
MLP full|msp        0.090           0.035      3     16.57
SecBERT-kv|msp      0.145           0.076      3     16.86
MLP 2k bin5|msp     0.085           0.009      3     17.29
SecBERT|maha        0.100           0.019      3     17.43
DistilBERT|energy   0.103           0.051      3     17.43
DistilBERT|maha     0.137           0.070      3     17.71
MLP 2k|energy       0.062           0.011      3     17.86
MLP 2k|knn          0.145           0.088      3     18.71
DistilBERT|msp      0.088           0.032      3     19.14
SecBERT|energy      0.055           0.026      3     19.57
DistilBERT|knn      0.087           0.041      3     20.00
tiny-local|maha     0.045           0.006      3     21.71
tiny-local|knn      0.069           0.043      3     22.00
tiny-local|msp      0.026           0.016      3     23.57
SecBERT|knn         0.052           0.010      3     23.57
tiny-local|energy   0.069           0.038      3     24.71
```

Friedman chi2 = 70.16, p = 4.61e-05. Nemenyi critical difference (alpha 0.05) = 18.30 ranks. Two combinations differ significantly when their average ranks differ by more than 18.30.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 34.36, p = 7.74e-05, Nemenyi CD = 5.12. Average ranks: RF 2k|msp 2.29, RF full|msp 2.86, RF 2k bin5|msp 3.14, SecBERT-kv|maha 4.71, MLP 2k bin5|maha 5.14, MLP 2k|maha 6.29, MLP full|maha 6.57, SecBERT|maha 7.43, DistilBERT|maha 7.86, tiny-local|maha 8.71

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.2817   -0.5198    -0.1121     0     0       7 -1.0000      0.0156  0.2656
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.2597   -0.4973    -0.0985     0     0       7 -1.0000      0.0156  0.2656
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0580   -0.1919     0.0747     3     0       4 -0.3571      0.4688  1.0000
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0181   -0.0595     0.1039     4     0       3  0.1429      0.8125  1.0000
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0347   -0.0332     0.1223     5     0       2  0.3571      0.4688  1.0000
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0499   -0.0015     0.1063     5     0       2  0.5714      0.2188  1.0000
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.2237   -0.4559    -0.0207     1     0       6 -0.7143      0.1094  1.0000
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0614    0.0174     0.1105     6     0       1  0.8571      0.0469  0.5156
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample    -0.2318   -0.4252    -0.0944     0     0       7 -1.0000      0.0156  0.2656
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.2098   -0.3990    -0.0781     0     0       7 -1.0000      0.0156  0.2656
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis    -0.0694   -0.2313     0.0809     2     0       5 -0.5000      0.2969  1.0000
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample    -0.2686   -0.4800    -0.0891     0     0       7 -1.0000      0.0156  0.2656
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.2466   -0.4315    -0.0874     0     0       7 -1.0000      0.0156  0.2656
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization     0.1555    0.0191     0.3368     5     0       2  0.7143      0.1094  1.0000
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.1908    0.0051     0.4575     4     0       3  0.4286      0.3750  1.0000
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0636   -0.1673     0.0053     3     0       4 -0.5714      0.2188  1.0000
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0614   -0.0246     0.1829     5     0       2  0.4286      0.3750  1.0000
```

### Scope: P1, NF-BoT-IoT-v3 only
Blocks (splits) = 3, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
RF full|msp         0.550           0.067      3      1.67
MLP full|knn        0.314           0.095      3      6.67
RF 2k bin5|msp      0.338           0.129      3      8.00
RF 2k|msp           0.292           0.139      3      8.17
MLP full|maha       0.315           0.102      3      8.33
MLP 2k bin5|maha    0.383           0.070      3      8.33
MLP 2k|maha         0.336           0.156      3      9.00
MLP 2k|knn          0.235           0.122      3     10.00
DistilBERT|maha     0.446           0.090      3     10.33
MLP full|energy     0.251           0.172      3     10.67
SecBERT-kv|maha     0.190           0.133      3     12.67
MLP 2k bin5|energy  0.217           0.098      3     12.83
SecBERT|maha        0.328           0.081      3     13.00
MLP 2k bin5|knn     0.265           0.063      3     13.67
MLP 2k bin5|msp     0.168           0.047      3     15.33
DistilBERT|knn      0.198           0.218      3     15.33
tiny-local|maha     0.247           0.095      3     16.00
MLP full|msp        0.112           0.101      3     16.83
MLP 2k|energy       0.104           0.084      3     19.00
SecBERT-kv|energy   0.099           0.072      3     19.33
SecBERT-kv|knn      0.056           0.046      3     19.33
MLP 2k|msp          0.057           0.007      3     20.00
SecBERT-kv|msp      0.086           0.036      3     20.67
DistilBERT|energy   0.080           0.095      3     22.33
SecBERT|msp         0.082           0.119      3     23.00
tiny-local|knn      0.078           0.045      3     23.83
DistilBERT|msp      0.013           0.011      3     25.33
tiny-local|msp      0.048           0.040      3     25.33
SecBERT|knn         0.030           0.019      3     25.33
SecBERT|energy      0.038           0.041      3     26.67
tiny-local|energy   0.035           0.051      3     29.00
```

Friedman chi2 = 53.78, p = 4.86e-03. Nemenyi critical difference (alpha 0.05) = 27.95 ranks. Two combinations differ significantly when their average ranks differ by more than 27.95.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 8.82, p = 4.54e-01, Nemenyi CD = 7.82. Average ranks: RF full|msp 1.67, DistilBERT|maha 4.67, MLP 2k bin5|maha 4.67, RF 2k|msp 5.00, MLP 2k|maha 5.67, MLP full|maha 6.00, RF 2k bin5|msp 6.00, SecBERT-kv|maha 6.33, SecBERT|maha 6.67, tiny-local|maha 8.33

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample    -0.0938   -0.2472    -0.0125     0     0       3 -1.0000        0.25     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.3520   -0.4264    -0.2551     0     0       3 -1.0000        0.25     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0363   -0.2996     0.2209     1     0       2 -0.3333        0.75     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.1206    0.0052     0.1948     3     0       0  1.0000        0.25     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.1681    0.0045     0.2902     3     0       0  1.0000        0.25     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.2474   -0.0002     0.5065     2     0       1  0.6667        0.50     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence    -0.0576   -0.2333     0.0524     2     0       1  0.0000        1.00     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.1016   -0.0974     0.4192     1     0       2  0.0000        1.00     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.1536   -0.0221     0.4940     1     0       2  0.0000        1.00     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data    -0.1046   -0.4266     0.2514     1     0       2 -0.3333        0.75     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.1095   -0.0133     0.3082     2     0       1  0.6667        0.50     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.0364   -0.0936     0.2281     1     0       2  0.0000        1.00     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.2218   -0.4299    -0.0145     0     0       3 -1.0000        0.25     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.1385   -0.5272     0.0899     2     0       1  0.0000        1.00     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)     0.0260   -0.0147     0.0787     2     0       1  0.3333        0.75     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0462   -0.1386     0.2436     2     0       1  0.3333        0.75     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0466   -0.0580     0.2097     1     0       2  0.0000        1.00     1.0
```

Note: with 3 blocks the smallest attainable two-sided Wilcoxon p-value is 0.250; treat this scope as descriptive.

### Scope: P3 only
Blocks (splits) = 4, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
tiny-local|msp      0.054           0.033      3      8.75
MLP 2k|knn          0.037           0.009      3      9.25
MLP full|knn        0.095           0.057      3     10.00
MLP 2k bin5|energy  0.066           0.050      3     10.00
RF 2k bin5|msp      0.031           0.046      3     10.75
MLP full|energy     0.030           0.016      3     11.25
RF full|msp         0.094           0.013      3     12.50
DistilBERT|energy   0.081           0.066      3     12.75
SecBERT|knn         0.085           0.057      3     13.00
MLP 2k|msp          0.024           0.033      3     13.50
tiny-local|maha     0.041           0.047      3     13.50
SecBERT-kv|maha     0.033           0.036      3     13.75
SecBERT-kv|knn      0.032           0.027      3     14.50
MLP 2k|energy       0.009           0.003      3     14.75
MLP full|msp        0.020           0.017      3     14.75
MLP 2k bin5|maha    0.041           0.028      3     15.50
SecBERT|energy      0.013           0.011      3     16.25
SecBERT|maha        0.067           0.016      3     16.62
SecBERT-kv|msp      0.008           0.003      3     17.25
MLP 2k bin5|knn     0.053           0.016      3     18.25
MLP full|maha       0.038           0.055      3     18.25
tiny-local|knn      0.005           0.004      3     18.75
MLP 2k bin5|msp     0.020           0.015      3     19.12
SecBERT|msp         0.004           0.001      3     19.25
DistilBERT|knn      0.023           0.015      3     20.88
SecBERT-kv|energy   0.009           0.005      3     21.00
tiny-local|energy   0.009           0.010      3     21.25
DistilBERT|maha     0.097           0.012      3     21.38
DistilBERT|msp      0.007           0.002      3     22.50
MLP 2k|maha         0.009           0.010      3     22.75
RF 2k|msp           0.017           0.011      3     24.00
```

Friedman chi2 = 27.70, p = 5.87e-01. Nemenyi critical difference (alpha 0.05) = 24.20 ranks. Two combinations differ significantly when their average ranks differ by more than 24.20.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 6.38, p = 7.01e-01, Nemenyi CD = 6.77. Average ranks: RF 2k bin5|msp 3.75, RF full|msp 4.00, tiny-local|maha 4.50, SecBERT-kv|maha 4.75, SecBERT|maha 5.50, MLP full|maha 5.50, MLP 2k bin5|maha 5.75, DistilBERT|maha 6.75, RF 2k|msp 7.25, MLP 2k|maha 7.25

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0058   -0.0246     0.0426     2     0       2  0.0000       1.000     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data    -0.0717   -0.2525     0.0431     1     0       3 -0.4000       0.625     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score    -0.0146   -0.0305    -0.0037     0     0       4 -1.0000       0.125     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining     0.0180   -0.0060     0.0420     2     0       2  0.4000       0.625     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.0623   -0.1726    -0.0008     0     0       4 -1.0000       0.125     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0745   -0.0208     0.2442     2     1       1  0.3333       0.750     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0204    0.0033     0.0507     4     0       0  1.0000       0.125     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)    -0.0280   -0.0504    -0.0056     0     0       4 -1.0000       0.125     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0803   -0.0454     0.2868     2     0       2  0.0000       1.000     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data     0.0028   -0.2733     0.2873     1     0       3 -0.2000       0.875     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0879   -0.0060     0.2700     1     0       3 -0.2000       0.875     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.0502   -0.0006     0.1459     3     0       1  0.6000       0.375     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data    -0.0274   -0.2223     0.1460     1     0       3 -0.4000       0.625     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0337   -0.0961     0.0028     2     0       2 -0.4000       0.625     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0532   -0.1429     0.0010     2     0       2 -0.4000       0.625     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0139    0.0044     0.0234     4     0       0  1.0000       0.125     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP     0.0317   -0.0040     0.0851     2     0       2  0.4000       0.625     1.0
```

Note: with 4 blocks the smallest attainable two-sided Wilcoxon p-value is 0.125; treat this scope as descriptive.
