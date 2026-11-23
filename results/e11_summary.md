# Four-network benchmark (E11), 1% warm-up budget, clean window

## P1 per dataset (mean over splits, then over seeds)

```
                             auroc_ood  auroc_unknown_vs_benign  unknown_recall  benign_false_alarm_rate
src        detector                                                                                     
bot_iot    Autoencoder           0.556                    0.923           0.332                    0.010
           DistilBERT            0.924                      NaN           0.446                    0.025
           Isolation Forest      0.657                    0.769           0.066                    0.009
           LightGBM              0.940                    0.849           0.172                    0.019
           MLP 2k                0.966                      NaN           0.336                    0.019
           MLP full              0.974                      NaN           0.315                    0.018
           RF 2k                 0.930                      NaN           0.292                    0.018
           RF full               0.954                      NaN           0.550                    0.021
           SecBERT               0.917                      NaN           0.328                    0.032
           k-NN raw              0.976                    0.952           0.385                    0.008
           tiny-local            0.892                      NaN           0.247                    0.046
cicids2018 Autoencoder           0.536                    0.890           0.066                    0.012
           DistilBERT            0.921                      NaN           0.136                    0.297
           Isolation Forest      0.508                    0.824           0.026                    0.012
           LightGBM              0.718                    0.491           0.057                    0.228
           MLP 2k                0.929                      NaN           0.101                    0.298
           MLP full              0.958                      NaN           0.087                    0.288
           RF 2k                 0.878                    0.769           0.238                    0.228
           RF full               0.865                    0.780           0.312                    0.181
           SecBERT               0.921                      NaN           0.133                    0.310
           k-NN raw              0.963                    0.875           0.057                    0.012
           tiny-local            0.865                      NaN           0.034                    0.358
ton_iot    Autoencoder           0.613                    0.887           0.312                    0.008
           DistilBERT            0.833                      NaN           0.137                    0.277
           Isolation Forest      0.596                    0.870           0.263                    0.010
           LightGBM              0.703                    0.660           0.044                    0.221
           MLP 2k                0.867                      NaN           0.206                    0.266
           MLP full              0.868                      NaN           0.248                    0.242
           RF 2k                 0.855                      NaN           0.369                    0.199
           RF full               0.848                      NaN           0.347                    0.185
           SecBERT               0.825                      NaN           0.100                    0.275
           k-NN raw              0.843                    0.870           0.295                    0.009
           tiny-local            0.716                      NaN           0.045                    0.341
unsw_nb15  Autoencoder           0.614                    0.998           1.000                    0.012
           DistilBERT            0.589                      NaN           0.026                    0.012
           Isolation Forest      0.586                    0.883           0.067                    0.008
           LightGBM              0.645                    0.999           1.000                    0.011
           MLP 2k                0.613                      NaN           0.112                    0.012
           MLP full              0.634                      NaN           0.185                    0.012
           RF 2k                 0.643                    0.985           0.923                    0.009
           RF full               0.659                    0.977           0.932                    0.009
           SecBERT               0.606                      NaN           0.049                    0.011
           k-NN raw              0.578                    0.515           0.039                    0.011
           tiny-local            0.521                      NaN           0.004                    0.010
```

## P1 all 21 splits

```
                 auroc_ood        auroc_unknown_vs_benign        unknown_recall        benign_false_alarm_rate       
                      mean    std                    mean    std           mean    std                    mean    std
detector                                                                                                             
Autoencoder          0.587  0.008                   0.925  0.002          0.453  0.016                   0.010  0.002
DistilBERT           0.797  0.003                     NaN    NaN          0.149  0.033                   0.170  0.008
Isolation Forest     0.581  0.005                   0.848  0.002          0.123  0.009                   0.010  0.001
LightGBM             0.724  0.009                   0.744  0.023          0.338  0.014                   0.134  0.001
MLP 2k               0.823  0.002                     NaN    NaN          0.173  0.020                   0.165  0.003
MLP full             0.838  0.002                     NaN    NaN          0.201  0.017                   0.155  0.002
RF 2k                0.811  0.007                   0.886  0.011          0.485  0.035                   0.126  0.003
RF full              0.814  0.004                   0.887  0.013          0.535  0.052                   0.110  0.001
SecBERT              0.799  0.007                     NaN    NaN          0.126  0.011                   0.173  0.007
k-NN raw             0.815  0.002                   0.781  0.002          0.178  0.002                   0.010  0.002
tiny-local           0.721  0.018                     NaN    NaN          0.060  0.016                   0.208  0.030
```

## P3 all splits

```
                 auroc_ood        auroc_unknown_vs_benign        unknown_recall        benign_false_alarm_rate       
                      mean    std                    mean    std           mean    std                    mean    std
detector                                                                                                             
Autoencoder          0.445  0.005                   0.415  0.015          0.032  0.011                   0.010  0.001
DistilBERT           0.478  0.032                     NaN    NaN          0.073  0.016                   0.627  0.025
Isolation Forest     0.453  0.007                   0.429  0.013          0.004  0.001                   0.010  0.000
LightGBM             0.540  0.035                   0.547  0.028          0.023  0.003                   0.469  0.068
MLP 2k               0.471  0.006                     NaN    NaN          0.020  0.004                   0.528  0.011
MLP full             0.501  0.006                     NaN    NaN          0.030  0.006                   0.475  0.048
RF 2k                0.543  0.013                   0.580  0.009          0.035  0.014                   0.495  0.015
RF full              0.528  0.025                   0.572  0.030          0.056  0.017                   0.403  0.025
SecBERT              0.516  0.011                     NaN    NaN          0.051  0.008                   0.683  0.051
k-NN raw             0.443  0.002                   0.425  0.001          0.047  0.007                   0.010  0.001
tiny-local           0.503  0.022                     NaN    NaN          0.023  0.005                   0.677  0.027
```

## P3 AUROC-OOD per split

```
detector                          Autoencoder  DistilBERT  Isolation Forest  LightGBM  MLP 2k  MLP full  RF 2k  RF full  SecBERT  k-NN raw  tiny-local
src        tgt        holdout                                                                                                                         
bot_iot    cicids2018 FLOOD             0.717       0.681             0.686     0.695   0.633     0.638  0.720    0.718    0.561     0.552       0.644
           ton_iot    FLOOD             0.703       0.820             0.702     0.327   0.466     0.516  0.528    0.643    0.832     0.831       0.824
                      RECON             0.298       0.266             0.323     0.765   0.397     0.520  0.707    0.775    0.317     0.123       0.360
           unsw_nb15  FLOOD             0.437       0.486             0.434     0.455   0.447     0.429  0.401    0.433    0.570     0.446       0.471
                      RECON             0.137       0.200             0.222     0.501   0.272     0.304  0.318    0.378    0.230     0.122       0.639
cicids2018 bot_iot    FLOOD             0.630       0.697             0.759     0.704   0.550     0.498  0.711    0.613    0.576     0.715       0.314
           ton_iot    BRUTEFORCE        0.326       0.518             0.379     0.506   0.461     0.463  0.706    0.731    0.558     0.387       0.613
                      FLOOD             0.799       0.648             0.709     0.816   0.718     0.623  0.689    0.640    0.416     0.770       0.358
                      WEB               0.340       0.536             0.347     0.221   0.449     0.400  0.503    0.542    0.588     0.342       0.368
           unsw_nb15  FLOOD             0.169       0.207             0.100     0.420   0.146     0.241  0.268    0.127    0.180     0.180       0.241
ton_iot    bot_iot    FLOOD             0.876       0.784             0.883     0.741   0.913     0.943  0.900    0.877    0.854     0.890       0.917
                      RECON             0.058       0.043             0.080     0.038   0.068     0.060  0.030    0.028    0.039     0.021       0.053
           cicids2018 BRUTEFORCE        0.447       0.598             0.517     0.731   0.494     0.627  0.466    0.695    0.964     0.180       0.283
                      FLOOD             0.623       0.452             0.565     0.437   0.476     0.413  0.520    0.494    0.392     0.768       0.539
                      WEB               0.330       0.362             0.256     0.724   0.596     0.661  0.517    0.528    0.524     0.278       0.344
           unsw_nb15  BACKDOOR          0.449       0.363             0.564     0.514   0.392     0.493  0.427    0.462    0.485     0.442       0.417
                      FLOOD             0.450       0.428             0.445     0.566   0.445     0.469  0.531    0.443    0.507     0.460       0.484
                      RECON             0.174       0.498             0.285     0.564   0.263     0.348  0.564    0.457    0.562     0.120       0.392
unsw_nb15  bot_iot    FLOOD             0.862       0.575             0.904     0.632   0.879     0.947  0.769    0.837    0.663     0.993       0.728
                      RECON             0.238       0.355             0.079     0.246   0.070     0.074  0.451    0.208    0.257     0.106       0.479
           cicids2018 FLOOD             0.400       0.358             0.340     0.598   0.603     0.648  0.518    0.535    0.663     0.529       0.671
           ton_iot    BACKDOOR          0.262       0.677             0.191     0.824   0.554     0.508  0.918    0.717    0.820     0.204       0.594
                      FLOOD             0.248       0.636             0.416     0.421   0.536     0.615  0.418    0.457    0.604     0.682       0.794
                      RECON             0.711       0.275             0.686     0.503   0.489     0.589  0.443    0.335    0.226     0.482       0.547
```

- P1 auroc_ood: 21 splits, 11 detectors: Friedman chi2 = 86.36, p = 2.81e-14, Nemenyi CD = 3.29. Average ranks: MLP full 3.52, MLP 2k 3.90, RF full 4.38, RF 2k 4.48, k-NN raw 4.57, DistilBERT 5.19, SecBERT 5.76, LightGBM 7.76, tiny-local 8.52, Autoencoder 8.71, Isolation Forest 9.19
- P1 unknown_recall: 21 splits, 11 detectors: Friedman chi2 = 72.57, p = 1.41e-11, Nemenyi CD = 3.29. Average ranks: RF full 2.76, RF 2k 3.19, Autoencoder 4.29, MLP full 5.67, LightGBM 5.90, MLP 2k 6.36, DistilBERT 6.88, SecBERT 6.98, k-NN raw 7.07, Isolation Forest 7.83, tiny-local 9.07
- P3 auroc_ood: 24 splits, 11 detectors: Friedman chi2 = 13.57, p = 1.94e-01, Nemenyi CD = 3.08. Average ranks: LightGBM 4.83, RF 2k 5.12, tiny-local 5.21, SecBERT 5.54, MLP full 5.67, RF full 5.79, MLP 2k 6.54, DistilBERT 6.67, Isolation Forest 6.67, Autoencoder 6.96, k-NN raw 7.00
- P3 unknown_recall: 24 splits, 11 detectors: Friedman chi2 = 28.56, p = 1.47e-03, Nemenyi CD = 3.08. Average ranks: SecBERT 4.31, DistilBERT 5.04, LightGBM 5.48, RF full 5.60, MLP full 5.69, tiny-local 5.83, k-NN raw 6.02, Autoencoder 6.17, RF 2k 6.33, MLP 2k 6.79, Isolation Forest 8.73

Splits available per detector: Autoencoder 45, DistilBERT 45, Isolation Forest 45, LightGBM 45, MLP 2k 45, MLP full 45, RF 2k 45, RF full 45, SecBERT 45, k-NN raw 45, tiny-local 45
