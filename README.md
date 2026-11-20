# Statistics Project (Fall 1405): NACC Track C (MRI + UDS)

**Question:** Is living situation (`NACCLIVS`) associated with executive function (`TRAILB`) and with the cortical thickness of selected frontal regions in older adults?
See [`PROJECT_CARD.md`](PROJECT_CARD.md) for the full statistical framework.

## Status
| Phase | Status | Deliverable |
|---|---|---|
| 1 Study, data, descriptive statistics | done | `reports/phase1/phase1_report.pdf`, tag `phase-1` |
| 2 Probability | - | |
| 3 Inference | - | |
| 4 Regression | - | |
| 5 Robustness and final report | - | |

## Repository structure
```
README.md
PROJECT_CARD.md
requirements.txt / environment.yml
data/                 # raw CSVs are NOT in Git (see data/README.md)
src/
  run_phase1.py       # full Phase 1 pipeline: tables + figures
    # builds the Phase 1 PDF from tables + figures
    # builds reports/phase1/phase1_report.tex (same content, LaTeX)
notebooks/
  phase1_analysis.ipynb   # same analysis as run_phase1.py, step by step
figures/              # fig1-fig13 (PNG)
reports/phase1/
  phase1_report.pdf
  tables/             # all CSV tables + key_numbers.json
```

## Reproducing Phase 1
1. Put the three delivered CSV files in `data/` (see `data/README.md`).
2. `pip install -r requirements.txt`  (or `conda env create -f environment.yml`)
3. `python src/run_phase1.py`  -> writes `figures/*.png` and `reports/phase1/tables/*`
4. open `notebooks/phase1_analysis.ipynb` and run all cells
5. LaTeX version: `reports/phase1  Figures are read from `../../figures/`.

No random numbers are used in Phase 1, so results are identical on every run.

## Tags
`phase-1`, `phase-2`, `phase-3`, `phase-4`, `final-5-phase`


## Phase 2: probability 
| Phase | Status | Deliverable |
|---|---|---|
| 2 Probability | done | `reports/phase2.pdf`, tag `phase-2` |

Reproduce: place the CSV files in `data/`, then
1. `python src/run_phase2.py`  -> `figures/p2_fig*.png`, `reports/phase2/tables/p2_*.csv` (fixed seed 1405)
2. `cd reports/phase2`  -> `phase2_report.pdf` (copy to `reports/phase2.pdf`)
