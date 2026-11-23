# Label collisions and near duplicates

## Full files

### NF-UNSW-NB15-v3: 2,365,424 flows
- identifiers removed (model features): 1.3% of rows have a feature vector seen with more than one label (30,907 rows; 993 distinct vectors)
  - most affected label sets: Backdoor / Generic: 13,210 rows, Backdoor / DoS / Exploits / Fuzzers / Generic / Reconnaissance / Shellcode: 7,560 rows, Backdoor / DoS / Exploits / Fuzzers / Reconnaissance: 4,548 rows, Exploits / Fuzzers: 922 rows, Exploits / Generic: 871 rows
  - share of each label's rows in conflicting vectors: Generic 71.4%, Reconnaissance 31.6%, Backdoor 24.9%, Fuzzers 20.1%, DoS 10.3%, Exploits 6.6%, Worms 5.1%, Shellcode 3.2%
- IP addresses and ports kept, timestamps removed: 0.1% of rows have a feature vector seen with more than one label (1,921 rows; 69 distinct vectors)
  - most affected label sets: Backdoor / Generic: 1,782 rows, Exploits / Fuzzers: 41 rows, Exploits / Reconnaissance: 18 rows, DoS / Fuzzers: 16 rows, Fuzzers / Reconnaissance: 16 rows
  - share of each label's rows in conflicting vectors: Generic 7.9%, Backdoor 5.0%, DoS 0.3%, Reconnaissance 0.1%, Fuzzers 0.1%, Shellcode 0.1%, Exploits 0.1%
- all columns kept (timestamps make rows unique): 0.0% of rows have a feature vector seen with more than one label (0 rows; 0 distinct vectors)
### NF-CICIDS2018-v3: 20,115,529 flows
- identifiers removed (model features): 26.5% of rows have a feature vector seen with more than one label (5,333,994 rows; 21,465 distinct vectors)
  - most affected label sets: Benign / Infilteration: 4,795,155 rows, DoS_attacks-SlowHTTPTest / FTP-BruteForce / SSH-Bruteforce: 492,330 rows, Benign / Brute_Force_-Web: 30,550 rows, Benign / DDoS_attacks-LOIC-HTTP: 8,519 rows, Benign / Brute_Force_-Web / Brute_Force_-XSS / SQL_Injection: 3,774 rows
  - share of each label's rows in conflicting vectors: DoS_attacks-SlowHTTPTest 100.0%, Brute_Force_-XSS 100.0%, FTP-BruteForce 100.0%, SQL_Injection 88.6%, Infilteration 74.8%, Brute_Force_-Web 41.8%, Benign 26.8%, DDoS_attacks-LOIC-HTTP 2.9%, SSH-Bruteforce 0.0%, DoS_attacks-Hulk 0.0%
- IP addresses and ports kept, timestamps removed: 0.1% of rows have a feature vector seen with more than one label (12,008 rows; 473 distinct vectors)
  - most affected label sets: Benign / Infilteration: 7,789 rows, Benign / Brute_Force_-Web / Brute_Force_-XSS / SQL_Injection: 2,564 rows, Benign / Brute_Force_-Web / SQL_Injection: 1,072 rows, Benign / Brute_Force_-Web: 146 rows, Benign / Brute_Force_-XSS: 146 rows
  - share of each label's rows in conflicting vectors: Brute_Force_-XSS 100.0%, SQL_Injection 87.5%, Brute_Force_-Web 20.5%, Infilteration 1.2%, Benign 0.0%
- all columns kept (timestamps make rows unique): 0.0% of rows have a feature vector seen with more than one label (880 rows; 440 distinct vectors)
  - most affected label sets: Brute_Force_-XSS / SQL_Injection: 544 rows, Brute_Force_-Web / Brute_Force_-XSS: 336 rows
  - share of each label's rows in conflicting vectors: Brute_Force_-XSS 91.7%, SQL_Injection 61.8%, Brute_Force_-Web 10.4%

## Near duplicates (seed 0)

### Near duplicates in nf_unsw_nb15_v3__cap20000__seed0.parquet (after de-duplication)
- BACKDOOR: 0.0% of flows have a benign nearest neighbour (median distance 0.129)
- EXPLOIT: 0.0% of flows have a benign nearest neighbour (median distance 0.142)
- FLOOD: 0.1% of flows have a benign nearest neighbour (median distance 0.163)
- FUZZING: 0.0% of flows have a benign nearest neighbour (median distance 0.083)
- GENERIC: 0.0% of flows have a benign nearest neighbour (median distance 0.138)
- RECON: 0.0% of flows have a benign nearest neighbour (median distance 0.061)
- WORM: 0.0% of flows have a benign nearest neighbour (median distance 0.171)
- BENIGN: 99.9% of benign flows have a benign nearest neighbour
### Near duplicates in nf_cicids2018_v3__cap20000__seed0.parquet (after de-duplication)
- BOTNET: 0.0% of flows have a benign nearest neighbour (median distance 0.028)
- BRUTEFORCE: 0.0% of flows have a benign nearest neighbour (median distance 0.014)
- FLOOD: 0.0% of flows have a benign nearest neighbour (median distance 0.012)
- INFILTRATION: 31.2% of flows have a benign nearest neighbour (median distance 0.071)
- WEB: 2.6% of flows have a benign nearest neighbour (median distance 0.023)
- BENIGN: 77.8% of benign flows have a benign nearest neighbour
