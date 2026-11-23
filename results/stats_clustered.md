# Dataset-aware planned comparisons (P1)

Balanced mean: average of the two per-dataset means. CI: stratified bootstrap over splits within each dataset. W/L: splits won/lost by the first detector.

## auroc_ood (target_warmup_far0.01)

```
                      comparison  ton_mean ton_WL  bot_mean bot_WL  balanced_mean  ci_low  ci_high  same_sign_both
      DistilBERT|knn - RF 2k|msp   -0.0561    0/7   -0.0011    2/1        -0.0286 -0.0401  -0.0194            True
    DistilBERT|knn - RF full|msp   -0.0498    0/7   -0.0251    0/3        -0.0375 -0.0579  -0.0197            True
     DistilBERT|knn - MLP 2k|knn   -0.0565    0/7   -0.0352    1/2        -0.0458 -0.0849  -0.0156            True
 DistilBERT|knn - tiny-local|knn    0.0420    7/0    0.0053    2/1         0.0236  0.0160   0.0314            True
    DistilBERT|knn - SecBERT|knn    0.0031    4/3    0.0040    1/2         0.0035 -0.0130   0.0219            True
DistilBERT|maha - DistilBERT|knn    0.0345    7/0   -0.0055    2/1         0.0145  0.0004   0.0267           False
          MLP 2k|knn - RF 2k|msp    0.0003    4/3    0.0341    2/1         0.0172 -0.0134   0.0581            True
        MLP 2k|maha - MLP 2k|knn    0.0116    5/2    0.0016    2/1         0.0066 -0.0045   0.0194            True
     DistilBERT|maha - RF 2k|msp   -0.0217    0/7   -0.0066    2/1        -0.0141 -0.0261  -0.0040            True
   DistilBERT|maha - RF full|msp   -0.0153    2/5   -0.0306    1/2        -0.0230 -0.0525  -0.0014            True
   DistilBERT|maha - MLP 2k|maha   -0.0336    1/6   -0.0423    2/1        -0.0379 -0.0854  -0.0036            True
        SecBERT|maha - RF 2k|msp   -0.0293    1/6   -0.0132    2/1        -0.0213 -0.0379  -0.0054            True
      SecBERT|maha - RF full|msp   -0.0229    1/6   -0.0373    0/3        -0.0301 -0.0619  -0.0077            True
  SecBERT-kv|maha - SecBERT|maha    0.0147    5/2   -0.0045    2/1         0.0051 -0.0095   0.0204           False
    SecBERT-kv|knn - SecBERT|knn    0.0395    6/1   -0.0086    1/2         0.0154  0.0013   0.0301           False
      RF 2k bin5|msp - RF 2k|msp   -0.0246    2/5    0.0233    1/2        -0.0007 -0.0415   0.0441           False
  MLP 2k bin5|maha - MLP 2k|maha   -0.0105    3/4   -0.0464    2/1        -0.0284 -0.0769   0.0025            True
```

## unknown_recall (target_warmup_far0.01)

```
                      comparison  ton_mean ton_WL  bot_mean bot_WL  balanced_mean  ci_low  ci_high  same_sign_both
      DistilBERT|knn - RF 2k|msp   -0.2817    0/7   -0.0938    0/3        -0.1878 -0.3219  -0.0805            True
    DistilBERT|knn - RF full|msp   -0.2597    0/7   -0.3520    0/3        -0.3058 -0.4317  -0.2104            True
     DistilBERT|knn - MLP 2k|knn   -0.0580    3/4   -0.0363    1/2        -0.0471 -0.1843   0.0877            True
 DistilBERT|knn - tiny-local|knn    0.0181    4/3    0.1206    3/0         0.0693  0.0051   0.1275            True
    DistilBERT|knn - SecBERT|knn    0.0347    5/2    0.1681    3/0         0.1014  0.0217   0.1766            True
DistilBERT|maha - DistilBERT|knn    0.0499    5/2    0.2474    2/1         0.1487  0.0314   0.2711            True
          MLP 2k|knn - RF 2k|msp   -0.2237    1/6   -0.0576    2/1        -0.1406 -0.2758  -0.0171            True
        MLP 2k|maha - MLP 2k|knn    0.0614    6/1    0.1016    1/2         0.0815 -0.0200   0.2331            True
     DistilBERT|maha - RF 2k|msp   -0.2318    0/7    0.1536    1/2        -0.0391 -0.1876   0.1225           False
   DistilBERT|maha - RF full|msp   -0.2098    0/7   -0.1046    1/2        -0.1572 -0.3324   0.0183            True
   DistilBERT|maha - MLP 2k|maha   -0.0694    2/5    0.1095    2/1         0.0200 -0.0870   0.1384           False
        SecBERT|maha - RF 2k|msp   -0.2686    0/7    0.0364    1/2        -0.1161 -0.2417   0.0069           False
      SecBERT|maha - RF full|msp   -0.2466    0/7   -0.2218    0/3        -0.2342 -0.3665  -0.1110            True
  SecBERT-kv|maha - SecBERT|maha    0.1555    5/2   -0.1385    2/1         0.0085 -0.1709   0.1672           False
    SecBERT-kv|knn - SecBERT|knn    0.1908    4/3    0.0260    2/1         0.1084  0.0100   0.2431            True
      RF 2k bin5|msp - RF 2k|msp   -0.0636    3/4    0.0462    2/1        -0.0087 -0.1060   0.0875           False
  MLP 2k bin5|maha - MLP 2k|maha    0.0614    5/2    0.0466    1/2         0.0540 -0.0235   0.1455            True
```

## benign_false_alarm_rate (target_warmup_far0.01)

```
                      comparison  ton_mean ton_WL  bot_mean bot_WL  balanced_mean  ci_low  ci_high  same_sign_both
      DistilBERT|knn - RF 2k|msp    0.0794    7/0    0.0064    2/1         0.0429  0.0336   0.0521            True
    DistilBERT|knn - RF full|msp    0.0939    7/0    0.0037    2/1         0.0488  0.0382   0.0586            True
     DistilBERT|knn - MLP 2k|knn    0.0131    5/2    0.0062    2/1         0.0097  0.0033   0.0162            True
 DistilBERT|knn - tiny-local|knn   -0.0620    0/7   -0.0238    0/3        -0.0429 -0.0728  -0.0218            True
    DistilBERT|knn - SecBERT|knn    0.0037    4/3   -0.0073    0/3        -0.0018 -0.0065   0.0026           False
DistilBERT|maha - DistilBERT|knn   -0.0016    1/6    0.0006    1/2        -0.0005 -0.0015   0.0007           False
          MLP 2k|knn - RF 2k|msp    0.0663    7/0    0.0002    2/1         0.0332  0.0244   0.0390            True
        MLP 2k|maha - MLP 2k|knn    0.0002    5/2    0.0004    2/1         0.0003 -0.0001   0.0008            True
     DistilBERT|maha - RF 2k|msp    0.0778    7/0    0.0070    2/1         0.0424  0.0327   0.0516            True
   DistilBERT|maha - RF full|msp    0.0923    7/0    0.0043    2/1         0.0483  0.0371   0.0587            True
   DistilBERT|maha - MLP 2k|maha    0.0113    5/2    0.0063    2/1         0.0088  0.0020   0.0155            True
        SecBERT|maha - RF 2k|msp    0.0760    7/0    0.0143    3/0         0.0452  0.0374   0.0523            True
      SecBERT|maha - RF full|msp    0.0905    7/0    0.0116    3/0         0.0510  0.0415   0.0593            True
  SecBERT-kv|maha - SecBERT|maha   -0.0240    0/7   -0.0124    0/3        -0.0182 -0.0225  -0.0140            True
    SecBERT-kv|knn - SecBERT|knn   -0.0233    0/7   -0.0115    0/3        -0.0174 -0.0218  -0.0130            True
      RF 2k bin5|msp - RF 2k|msp    0.0465    7/0   -0.0033    0/3         0.0216  0.0145   0.0263           False
  MLP 2k bin5|maha - MLP 2k|maha   -0.0137    1/6   -0.0019    1/2        -0.0078 -0.0106  -0.0047            True
```
