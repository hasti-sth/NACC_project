# Data

**Source:** NACC (National Alzheimer's Coordinating Center), https://www.naccdata.org/about-nacc-data/
The files are a pre-defined subset prepared by the teaching team for Track C. They are **not stored in this repository** (raw data, access terms). Date received: 10 October 2026, from the teaching assistants.

| File | Content | Rows x columns |
|---|---|---|
| `udslong_imputed.csv` | Selected UDS variables (demographic, medical, functional, cognitive, diagnostic); one record per participant; some values already imputed by an unknown method | 1,237 x 180 |
| `mriscanclean.csv` | Regional MRI measures (`GVOL`, `AVGTH`) for 31 cortical regions x 2 hemispheres, plus `NACCID`, `NACCUDSD` | 1,237 x 126 |
| `combined_adjacency_matrix.csv` | Region-by-region adjacency matrix (not used in this project) | 62 x 62 |

## How to rebuild the analytic data set
1. Copy the three CSV files into this folder (`data/`).
2. Run `python src/run_phase1.py` from the repository root.
3. The script links the files by `NACCID` (one-to-one inner join, 1,237 participants), recodes special codes on a working copy, and defines the analytic sample (age >= 65, `NACCLIVS` in 1-4; n = 861). Every step and count is saved in `reports/phase1/tables/` (e.g. `table_linkage_flow.csv`, `table_sample_flow.csv`).

Raw files are never modified.

## Open questions for the teaching team
1. Which visit does each participant's record represent; how far apart are the UDS and MRI data?
2. Which imputation/transformation was applied to the UDS file?
3. Were MRI values processed or replaced? Is this the final analysis-ready version?
4. Is an intracranial-volume measure available? Units provided: `AVGTH` in mm, `GVOL` in mm^3 (to be cross-checked against the RDD).
