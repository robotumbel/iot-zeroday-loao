# Datasets

Place raw files as below (paths match `configs/datasets.json`). Check each licence and cite the dataset paper.

| Dataset | Folder | Source | Notes |
|---|---|---|---|
| NF-ToN-IoT-v3 | `data/raw/NF-ToN-IoT-v3/` | University of Queensland, "ML-based NIDS Datasets" (https://staff.itee.uq.edu.au/marius/NIDS_datasets/, record https://researchdata.edu.au/nf-ton-iot-v3/3485175) | 53 NetFlow v3 features, `Attack` column |
| NF-BoT-IoT-v3 | `data/raw/NF-BoT-IoT-v3/` | same UQ collection | same feature set |
| CICIoT2023 (CSV) | `data/raw/CICIoT2023/` | Canadian Institute for Cybersecurity (https://www.unb.ca/cic/datasets/iotdataset-2023.html) | native 46 features, `label` column; P1 only |
| CICIoT2023 (NetFlow v3) | `data/interim/NF-CICIoT2023-v3/` | built by us from the CICIoT2023 PCAPs | needed for P2/P3; see below |
| Edge-IIoTset | `data/raw/Edge-IIoTset/` | Ferrag et al., IEEE DataPort / Kaggle | `ML-EdgeIIoT-dataset.csv`, `Attack_type` column; P1 only unless re-extracted |

## Building NF-CICIoT2023-v3

CICIoT2023 CSVs are packet-window features, not NetFlow, so they cannot be mixed with NF-ToN-IoT-v3 directly. Re-extract flows from the PCAPs with the same exporter and template the UQ team used (nProbe NetFlow v3 template). If nProbe is not available, NFStream is an open alternative, but then the NF-ToN-IoT/NF-BoT-IoT PCAPs must also be re-extracted with NFStream so all three share one feature space. Label each flow from the attack folder of its PCAP and write an `Attack` column with the original CICIoT2023 label names.

## Sizes

The full NF-v3 files are tens of millions of rows. `loao.cli prepare --cap N` keeps at most N rows per raw label with deterministic sampling, so a laptop can run the pipeline (e.g. `--cap 50000`).
