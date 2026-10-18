# Statistical comparison — metric `benign_false_alarm_rate`, rule `target_warmup_far0.01`, warm-up contamination 0, seeds [0, 1, 2]


### Scope: all splits (P1 + P3)
Blocks (splits) = 14, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
tiny-local|msp      0.273           0.027      3      5.04
tiny-local|energy   0.273           0.027      3      5.36
tiny-local|knn      0.272           0.027      3      5.36
tiny-local|maha     0.272           0.027      3      5.39
SecBERT|knn         0.268           0.021      3      7.14
SecBERT|maha        0.268           0.021      3      7.14
SecBERT|energy      0.266           0.021      3      8.86
SecBERT|msp         0.265           0.021      3      9.64
DistilBERT|knn      0.231           0.003      3     10.93
DistilBERT|maha     0.230           0.003      3     11.50
DistilBERT|energy   0.229           0.004      3     12.00
DistilBERT|msp      0.228           0.004      3     13.93
MLP 2k|maha         0.217           0.008      3     14.43
MLP 2k|knn          0.216           0.009      3     15.21
MLP 2k|energy       0.214           0.008      3     15.86
MLP 2k|msp          0.214           0.009      3     16.79
SecBERT-kv|maha     0.222           0.015      3     18.86
SecBERT-kv|knn      0.222           0.016      3     19.21
MLP 2k bin5|knn     0.200           0.005      3     19.64
MLP 2k bin5|maha    0.200           0.006      3     20.21
MLP full|knn        0.212           0.016      3     20.36
MLP full|maha       0.211           0.016      3     20.79
MLP full|energy     0.211           0.015      3     20.93
SecBERT-kv|energy   0.220           0.015      3     21.54
SecBERT-kv|msp      0.220           0.015      3     21.75
MLP full|msp        0.210           0.015      3     22.86
MLP 2k bin5|msp     0.198           0.004      3     23.36
MLP 2k bin5|energy  0.198           0.005      3     23.79
RF 2k bin5|msp      0.202           0.012      3     23.79
RF 2k|msp           0.166           0.005      3     26.64
RF full|msp         0.148           0.007      3     27.71
```

Friedman chi2 = 242.16, p = 4.90e-35. Nemenyi critical difference (alpha 0.05) = 12.94 ranks. Two combinations differ significantly when their average ranks differ by more than 12.94.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 75.90, p = 1.05e-12, Nemenyi CD = 3.62. Average ranks: tiny-local|maha 1.86, SecBERT|maha 2.36, DistilBERT|maha 3.64, MLP 2k|maha 4.64, SecBERT-kv|maha 5.79, MLP 2k bin5|maha 6.07, MLP full|maha 6.50, RF 2k bin5|msp 7.14, RF 2k|msp 8.14, RF full|msp 8.86

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0651    0.0433     0.0866    13     0       1  0.9810      0.0002  0.0032
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data     0.0832    0.0489     0.1205    13     0       1  0.9619      0.0004  0.0040
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0153   -0.0152     0.0516     9     0       5  0.3905      0.2166  0.6497
 DistilBERT|knn - tiny-local|knn                    effect of pretraining    -0.0413   -0.0855     0.0064     2     0      12 -0.6571      0.0295  0.1477
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.0374   -0.0897    -0.0032     4     0      10 -0.4476      0.1531  0.6123
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score    -0.0008   -0.0018     0.0003     4     0      10 -0.3905      0.2166  0.6497
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0498    0.0219     0.0780    12     0       2  0.8476      0.0031  0.0244
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0009    0.0002     0.0017    11     0       3  0.7143      0.0166  0.0996
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0643    0.0428     0.0858    13     0       1  0.9810      0.0002  0.0032
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data     0.0824    0.0485     0.1194    13     0       1  0.9619      0.0004  0.0040
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0136   -0.0170     0.0499     9     0       5  0.3714      0.2412  0.6497
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.1025    0.0582     0.1672    14     0       0  1.0000      0.0001  0.0021
      SecBERT|maha - RF full|msp         security encoder vs RF, all data     0.1205    0.0647     0.2022    14     0       0  1.0000      0.0001  0.0021
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0464   -0.0697    -0.0257     0     0      14 -1.0000      0.0001  0.0021
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0465   -0.0705    -0.0252     0     0      14 -1.0000      0.0001  0.0021
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0366    0.0170     0.0572    10     0       4  0.7714      0.0085  0.0598
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0163   -0.0274    -0.0074     3     0      11 -0.8667      0.0023  0.0209
```

### Scope: P1 only
Blocks (splits) = 10, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
tiny-local|knn      0.253           0.044      3       2.3
tiny-local|msp      0.253           0.043      3       2.4
tiny-local|maha     0.252           0.043      3       2.5
tiny-local|energy   0.253           0.044      3       2.8
SecBERT|maha        0.202           0.006      3       7.4
SecBERT|knn         0.202           0.006      3       7.7
DistilBERT|knn      0.202           0.006      3       9.1
DistilBERT|maha     0.201           0.007      3       9.7
SecBERT|energy      0.199           0.007      3       9.8
DistilBERT|energy   0.200           0.006      3      10.4
SecBERT|msp         0.198           0.006      3      10.6
DistilBERT|msp      0.198           0.007      3      12.9
MLP 2k|maha         0.191           0.003      3      14.2
MLP 2k|knn          0.191           0.004      3      14.5
MLP 2k|energy       0.189           0.003      3      15.6
MLP 2k|msp          0.189           0.004      3      16.8
SecBERT-kv|maha     0.182           0.002      3      18.9
SecBERT-kv|knn      0.182           0.003      3      19.1
MLP 2k bin5|knn     0.182           0.001      3      19.1
MLP 2k bin5|maha    0.181           0.001      3      20.5
SecBERT-kv|msp      0.180           0.004      3      22.3
SecBERT-kv|energy   0.180           0.004      3      22.4
MLP full|knn        0.175           0.003      3      22.9
MLP full|maha       0.175           0.003      3      23.1
MLP 2k bin5|msp     0.179           0.001      3      23.8
MLP full|energy     0.174           0.002      3      23.8
MLP 2k bin5|energy  0.179           0.002      3      24.7
RF 2k bin5|msp      0.176           0.004      3      25.2
MLP full|msp        0.172           0.002      3      26.7
RF full|msp         0.135           0.002      3      27.3
RF 2k|msp           0.145           0.004      3      27.5
```

Friedman chi2 = 236.75, p = 5.37e-34. Nemenyi critical difference (alpha 0.05) = 15.31 ranks. Two combinations differ significantly when their average ranks differ by more than 15.31.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 67.68, p = 4.33e-11, Nemenyi CD = 4.28. Average ranks: tiny-local|maha 1.00, SecBERT|maha 2.50, DistilBERT|maha 3.20, MLP 2k|maha 4.50, SecBERT-kv|maha 5.70, MLP 2k bin5|maha 6.10, MLP full|maha 7.40, RF 2k bin5|msp 7.60, RF 2k|msp 8.30, RF full|msp 8.70

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0575    0.0337     0.0806     9     0       1  0.9636      0.0039  0.0469
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data     0.0668    0.0378     0.0946     9     0       1  0.9273      0.0059  0.0586
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0111    0.0033     0.0192     7     0       3  0.7091      0.0488  0.2441
 DistilBERT|knn - tiny-local|knn                    effect of pretraining    -0.0506   -0.0934    -0.0233     0     0      10 -1.0000      0.0020  0.0332
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0004   -0.0065     0.0075     4     0       6  0.0545      0.9219  0.9219
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score    -0.0009   -0.0021     0.0005     2     0       8 -0.4182      0.2754  0.5508
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0465    0.0244     0.0675     9     0       1  0.9273      0.0059  0.0586
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0003   -0.0003     0.0008     7     0       3  0.5273      0.1602  0.4805
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0566    0.0331     0.0794     9     0       1  0.9636      0.0039  0.0469
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data     0.0659    0.0373     0.0934     9     0       1  0.9273      0.0059  0.0586
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0098    0.0018     0.0182     7     0       3  0.6727      0.0645  0.2578
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.0575    0.0377     0.0763    10     0       0  1.0000      0.0020  0.0332
      SecBERT|maha - RF full|msp         security encoder vs RF, all data     0.0668    0.0416     0.0907    10     0       0  1.0000      0.0020  0.0332
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0205   -0.0271    -0.0141     0     0      10 -1.0000      0.0020  0.0332
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0198   -0.0268    -0.0129     0     0      10 -1.0000      0.0020  0.0332
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0315    0.0148     0.0477     7     0       3  0.7818      0.0273  0.1641
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0101   -0.0153    -0.0050     2     0       8 -0.8909      0.0098  0.0684
```

### Scope: P1, NF-ToN-IoT-v3 only
Blocks (splits) = 7, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
tiny-local|maha     0.341           0.053      3      2.14
tiny-local|msp      0.341           0.053      3      2.29
tiny-local|knn      0.340           0.054      3      2.57
tiny-local|energy   0.341           0.054      3      3.00
DistilBERT|knn      0.278           0.010      3      7.57
SecBERT|maha        0.275           0.009      3      8.29
SecBERT|knn         0.275           0.009      3      8.57
DistilBERT|maha     0.277           0.010      3      8.71
DistilBERT|energy   0.276           0.010      3      9.14
SecBERT|energy      0.272           0.010      3     10.43
DistilBERT|msp      0.274           0.010      3     10.86
SecBERT|msp         0.271           0.010      3     11.86
MLP 2k|maha         0.266           0.005      3     11.86
MLP 2k|knn          0.265           0.007      3     12.14
MLP 2k|energy       0.262           0.006      3     14.57
MLP 2k|msp          0.261           0.007      3     15.86
MLP 2k bin5|knn     0.253           0.003      3     17.57
MLP 2k bin5|maha    0.252           0.003      3     18.71
SecBERT-kv|knn      0.251           0.004      3     19.57
SecBERT-kv|maha     0.251           0.003      3     19.71
MLP 2k bin5|energy  0.249           0.004      3     22.86
SecBERT-kv|energy   0.249           0.006      3     23.14
MLP full|knn        0.242           0.002      3     23.71
MLP 2k bin5|msp     0.249           0.004      3     23.86
RF 2k bin5|msp      0.246           0.005      3     24.00
SecBERT-kv|msp      0.248           0.006      3     24.14
MLP full|maha       0.242           0.002      3     24.43
MLP full|energy     0.241           0.001      3     25.57
MLP full|msp        0.238           0.001      3     27.86
RF 2k|msp           0.199           0.007      3     30.00
RF full|msp         0.185           0.004      3     31.00
```

Friedman chi2 = 189.19, p = 5.11e-25. Nemenyi critical difference (alpha 0.05) = 18.30 ranks. Two combinations differ significantly when their average ranks differ by more than 18.30.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 58.64, p = 2.45e-09, Nemenyi CD = 5.12. Average ranks: tiny-local|maha 1.00, DistilBERT|maha 2.71, SecBERT|maha 2.71, MLP 2k|maha 3.86, MLP 2k bin5|maha 5.43, SecBERT-kv|maha 6.00, RF 2k bin5|msp 6.86, MLP full|maha 7.43, RF 2k|msp 9.00, RF full|msp 10.00

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0794    0.0631     0.0953     7     0       0  1.0000      0.0156  0.2656
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data     0.0939    0.0744     0.1108     7     0       0  1.0000      0.0156  0.2656
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0131    0.0026     0.0240     5     0       2  0.7143      0.1094  0.5469
 DistilBERT|knn - tiny-local|knn                    effect of pretraining    -0.0620   -0.1188    -0.0253     0     0       7 -1.0000      0.0156  0.2656
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining     0.0037   -0.0054     0.0123     4     0       3  0.2857      0.5781  0.8906
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score    -0.0016   -0.0027     0.0002     1     0       6 -0.5000      0.2969  0.8906
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0663    0.0494     0.0775     7     0       0  1.0000      0.0156  0.2656
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0002   -0.0005     0.0008     5     0       2  0.4286      0.3750  0.8906
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0778    0.0611     0.0940     7     0       0  1.0000      0.0156  0.2656
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data     0.0923    0.0726     0.1096     7     0       0  1.0000      0.0156  0.2656
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0113    0.0002     0.0226     5     0       2  0.6429      0.1562  0.6250
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.0760    0.0623     0.0871     7     0       0  1.0000      0.0156  0.2656
      SecBERT|maha - RF full|msp         security encoder vs RF, all data     0.0905    0.0736     0.1033     7     0       0  1.0000      0.0156  0.2656
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0240   -0.0315    -0.0159     0     0       7 -1.0000      0.0156  0.2656
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0233   -0.0315    -0.0145     0     0       7 -1.0000      0.0156  0.2656
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0465    0.0329     0.0552     7     0       0  1.0000      0.0156  0.2656
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0137   -0.0186    -0.0081     1     0       6 -0.9286      0.0312  0.2656
```

### Scope: P1, NF-BoT-IoT-v3 only
Blocks (splits) = 3, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
tiny-local|knn      0.048           0.022      3      1.67
tiny-local|energy   0.048           0.022      3      2.33
tiny-local|msp      0.047           0.022      3      2.67
tiny-local|maha     0.046           0.021      3      3.33
SecBERT|maha        0.032           0.007      3      5.33
SecBERT|knn         0.032           0.009      3      5.67
SecBERT|msp         0.027           0.006      3      7.67
SecBERT|energy      0.027           0.007      3      8.33
DistilBERT|maha     0.025           0.000      3     12.00
DistilBERT|knn      0.024           0.002      3     12.67
DistilBERT|energy   0.023           0.004      3     13.33
SecBERT-kv|maha     0.020           0.002      3     17.00
DistilBERT|msp      0.021           0.003      3     17.67
MLP 2k|energy       0.020           0.006      3     18.00
SecBERT-kv|msp      0.020           0.001      3     18.00
SecBERT-kv|knn      0.020           0.001      3     18.00
RF full|msp         0.021           0.003      3     18.67
MLP 2k|msp          0.019           0.001      3     19.00
MLP 2k|maha         0.019           0.003      3     19.67
MLP full|energy     0.019           0.006      3     19.67
MLP full|maha       0.018           0.005      3     20.00
MLP 2k|knn          0.018           0.004      3     20.00
SecBERT-kv|energy   0.019           0.002      3     20.67
MLP full|knn        0.019           0.007      3     21.00
RF 2k|msp           0.018           0.004      3     21.67
MLP 2k bin5|knn     0.018           0.004      3     22.67
MLP 2k bin5|msp     0.017           0.005      3     23.67
MLP full|msp        0.016           0.005      3     24.00
MLP 2k bin5|maha    0.017           0.003      3     24.67
RF 2k bin5|msp      0.015           0.002      3     28.00
MLP 2k bin5|energy  0.015           0.002      3     29.00
```

Friedman chi2 = 66.72, p = 1.32e-04. Nemenyi critical difference (alpha 0.05) = 27.95 ranks. Two combinations differ significantly when their average ranks differ by more than 27.95.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 19.15, p = 2.40e-02, Nemenyi CD = 7.82. Average ranks: tiny-local|maha 1.00, SecBERT|maha 2.00, DistilBERT|maha 4.33, SecBERT-kv|maha 5.00, RF full|msp 5.67, MLP 2k|maha 6.00, RF 2k|msp 6.67, MLP full|maha 7.33, MLP 2k bin5|maha 7.67, RF 2k bin5|msp 9.33

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses    r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0064   -0.0026     0.0176     2     0       1  0.6667        0.50     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data     0.0037   -0.0081     0.0147     2     0       1  0.3333        0.75     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0062   -0.0003     0.0152     2     0       1  0.6667        0.50     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining    -0.0238   -0.0448    -0.0119     0     0       3 -1.0000        0.25     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.0073   -0.0093    -0.0050     0     0       3 -1.0000        0.25     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score     0.0006   -0.0006     0.0026     1     0       2  0.0000        1.00     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0002   -0.0023     0.0024     2     0       1  0.3333        0.75     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0004   -0.0002     0.0013     2     0       1  0.6667        0.50     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0070   -0.0032     0.0174     2     0       1  0.6667        0.50     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data     0.0043   -0.0087     0.0145     2     0       1  0.3333        0.75     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0063   -0.0022     0.0148     2     0       1  0.6667        0.50     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.0143    0.0061     0.0239     3     0       0  1.0000        0.25     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data     0.0116    0.0006     0.0210     3     0       0  1.0000        0.25     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.0124   -0.0168    -0.0092     0     0       3 -1.0000        0.25     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.0115   -0.0135    -0.0105     0     0       3 -1.0000        0.25     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF    -0.0033   -0.0060    -0.0000     0     0       3 -1.0000        0.25     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0019   -0.0050     0.0006     1     0       2 -0.6667        0.50     1.0
```

Note: with 3 blocks the smallest attainable two-sided Wilcoxon p-value is 0.250; treat this scope as descriptive.

### Scope: P3 only
Blocks (splits) = 4, method x score combinations = 31, seeds = 3

```
                     mean  std_over_seeds  seeds  avg_rank
combo                                                     
SecBERT|knn         0.434           0.059      3      5.75
SecBERT|energy      0.433           0.057      3      6.50
SecBERT|maha        0.433           0.059      3      6.50
SecBERT|msp         0.432           0.060      3      7.25
tiny-local|msp      0.323           0.029      3     11.62
tiny-local|energy   0.323           0.029      3     11.75
tiny-local|maha     0.322           0.029      3     12.62
tiny-local|knn      0.321           0.029      3     13.00
MLP full|msp        0.304           0.050      3     13.25
MLP full|energy     0.304           0.050      3     13.75
MLP full|knn        0.305           0.050      3     14.00
MLP 2k|maha         0.279           0.022      3     15.00
MLP full|maha       0.303           0.049      3     15.00
DistilBERT|knn      0.302           0.011      3     15.50
DistilBERT|maha     0.302           0.013      3     16.00
DistilBERT|energy   0.301           0.013      3     16.00
MLP 2k|energy       0.277           0.023      3     16.50
DistilBERT|msp      0.301           0.015      3     16.50
MLP 2k|msp          0.276           0.020      3     16.75
MLP 2k|knn          0.277           0.022      3     17.00
SecBERT-kv|maha     0.322           0.048      3     18.75
SecBERT-kv|energy   0.321           0.046      3     19.38
SecBERT-kv|knn      0.321           0.048      3     19.50
MLP 2k bin5|maha    0.248           0.019      3     19.50
RF 2k bin5|msp      0.268           0.037      3     20.25
SecBERT-kv|msp      0.321           0.045      3     20.38
MLP 2k bin5|knn     0.245           0.016      3     21.00
MLP 2k bin5|energy  0.245           0.014      3     21.50
MLP 2k bin5|msp     0.244           0.015      3     22.25
RF 2k|msp           0.218           0.009      3     24.50
RF full|msp         0.178           0.019      3     28.75
```

Friedman chi2 = 41.15, p = 8.44e-02. Nemenyi critical difference (alpha 0.05) = 24.20 ranks. Two combinations differ significantly when their average ranks differ by more than 24.20.

Primary-score analysis (10 detectors, one score each): Friedman chi2 = 16.04, p = 6.61e-02, Nemenyi CD = 6.77. Average ranks: SecBERT|maha 2.00, tiny-local|maha 4.00, MLP full|maha 4.25, DistilBERT|maha 4.75, MLP 2k|maha 5.00, SecBERT-kv|maha 6.00, MLP 2k bin5|maha 6.00, RF 2k bin5|msp 6.00, RF 2k|msp 7.75, RF full|msp 9.25

Planned comparisons (positive mean_diff = first method higher; Holm over the 17 comparisons in this table; r_rb = matched-pairs rank-biserial effect size):

```
                      comparison                                 question  mean_diff  ci95_low  ci95_high  wins  ties  losses  r_rb  p_wilcoxon  p_holm
      DistilBERT|knn - RF 2k|msp          LLM vs RF, same training sample     0.0841    0.0444     0.1238     4     0       0   1.0       0.125     1.0
    DistilBERT|knn - RF full|msp         LLM vs RF with all training data     0.1240    0.0299     0.2181     4     0       0   1.0       0.125     1.0
     DistilBERT|knn - MLP 2k|knn  language model vs plain MLP, same score     0.0257   -0.0805     0.1320     2     0       2   0.2       0.875     1.0
 DistilBERT|knn - tiny-local|knn                    effect of pretraining    -0.0181   -0.1346     0.1008     2     0       2   0.0       1.000     1.0
    DistilBERT|knn - SecBERT|knn   general vs security-domain pretraining    -0.1318   -0.2674    -0.0504     0     0       4  -1.0       0.125     1.0
DistilBERT|maha - DistilBERT|knn                 Mahalanobis vs kNN score    -0.0004   -0.0017     0.0011     2     0       2  -0.2       0.875     1.0
          MLP 2k|knn - RF 2k|msp      embedding distance vs RF confidence     0.0583   -0.0252     0.1346     3     0       1   0.6       0.375     1.0
        MLP 2k|maha - MLP 2k|knn           Mahalanobis vs kNN score (MLP)     0.0026    0.0010     0.0036     4     0       0   1.0       0.125     1.0
     DistilBERT|maha - RF 2k|msp    best encoder score vs RF, same sample     0.0837    0.0448     0.1226     4     0       0   1.0       0.125     1.0
   DistilBERT|maha - RF full|msp       best encoder score vs RF, all data     0.1236    0.0303     0.2170     4     0       0   1.0       0.125     1.0
   DistilBERT|maha - MLP 2k|maha         encoder vs MLP, both Mahalanobis     0.0228   -0.0833     0.1289     2     0       2   0.2       0.875     1.0
        SecBERT|maha - RF 2k|msp      security encoder vs RF, same sample     0.2149    0.1168     0.3829     4     0       0   1.0       0.125     1.0
      SecBERT|maha - RF full|msp         security encoder vs RF, all data     0.2548    0.1066     0.4592     4     0       0   1.0       0.125     1.0
  SecBERT-kv|maha - SecBERT|maha       raw-value vs 5-level serialization    -0.1111   -0.1192    -0.1013     0     0       4  -1.0       0.125     1.0
    SecBERT-kv|knn - SecBERT|knn raw-value vs 5-level serialization (kNN)    -0.1134   -0.1213    -0.1026     0     0       4  -1.0       0.125     1.0
      RF 2k bin5|msp - RF 2k|msp               5-level discretization, RF     0.0492   -0.0037     0.1002     3     0       1   0.6       0.375     1.0
  MLP 2k bin5|maha - MLP 2k|maha              5-level discretization, MLP    -0.0318   -0.0572    -0.0063     1     0       3  -0.8       0.250     1.0
```

Note: with 4 blocks the smallest attainable two-sided Wilcoxon p-value is 0.125; treat this scope as descriptive.
