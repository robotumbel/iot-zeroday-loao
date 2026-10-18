# Label collisions and near duplicates

## Full files

### NF-ToN-IoT-v3: 27,520,260 flows
- identifiers removed (model features): 49.2% of rows have a feature vector seen with more than one label (13,543,510 rows; 184,757 distinct vectors)
  - most affected label sets: Benign / scanning: 7,851,265 rows, Benign / ddos / injection / xss: 2,157,114 rows, Benign / ddos / injection / password / xss: 988,204 rows, Benign / password: 596,129 rows, Benign / ddos: 554,550 rows
  - share of each label's rows in conflicting vectors: scanning 94.3%, ddos 77.7%, dos 44.1%, Benign 43.0%, xss 41.0%, password 33.4%, injection 10.6%, mitm 9.4%, ransomware 9.0%, Backdoor 1.2%
- IP addresses and ports kept, timestamps removed: 0.0% of rows have a feature vector seen with more than one label (10,429 rows; 1,786 distinct vectors)
  - most affected label sets: ddos / injection: 7,762 rows, injection / xss: 1,058 rows, Benign / dos: 910 rows, Benign / ddos: 339 rows, Benign / injection: 178 rows
  - share of each label's rows in conflicting vectors: injection 0.3%, dos 0.2%, ddos 0.2%, xss 0.0%, Benign 0.0%, password 0.0%
- all columns kept (timestamps make rows unique): 0.0% of rows have a feature vector seen with more than one label (0 rows; 0 distinct vectors)
### NF-BoT-IoT-v3: 16,933,808 flows
- identifiers removed (model features): 4.0% of rows have a feature vector seen with more than one label (681,097 rows; 7,009 distinct vectors)
  - most affected label sets: Benign / Reconnaissance: 408,113 rows, DDoS / DoS: 272,961 rows, DDoS / DoS / Reconnaissance: 23 rows
  - share of each label's rows in conflicting vectors: Benign 57.6%, Reconnaissance 22.3%, DoS 2.0%, DDoS 1.6%
- IP addresses and ports kept, timestamps removed: 0.2% of rows have a feature vector seen with more than one label (31,526 rows; 15,432 distinct vectors)
  - most affected label sets: DDoS / DoS: 31,526 rows
  - share of each label's rows in conflicting vectors: DDoS 0.2%, DoS 0.2%
- all columns kept (timestamps make rows unique): 0.0% of rows have a feature vector seen with more than one label (0 rows; 0 distinct vectors)

## Near duplicates (seed 0)

### Near duplicates in nf_ton_iot_v3__cap20000__seed0.parquet (after de-duplication)
- BACKDOOR: 0.1% of flows have a benign nearest neighbour (median distance 0.001)
- BRUTEFORCE: 0.5% of flows have a benign nearest neighbour (median distance 0.015)
- FLOOD: 0.2% of flows have a benign nearest neighbour (median distance 0.021)
- MITM_SPOOF: 0.4% of flows have a benign nearest neighbour (median distance 0.276)
- RANSOMWARE: 0.4% of flows have a benign nearest neighbour (median distance 0.048)
- RECON: 23.0% of flows have a benign nearest neighbour (median distance 0.000)
- WEB: 0.4% of flows have a benign nearest neighbour (median distance 0.068)
- BENIGN: 79.1% of benign flows have a benign nearest neighbour
### Near duplicates in nf_bot_iot_v3__cap20000__seed0.parquet (after de-duplication)
- FLOOD: 0.0% of flows have a benign nearest neighbour (median distance 0.001)
- RECON: 1.9% of flows have a benign nearest neighbour (median distance 0.001)
- THEFT: 0.9% of flows have a benign nearest neighbour (median distance 0.028)
- BENIGN: 97.3% of benign flows have a benign nearest neighbour
