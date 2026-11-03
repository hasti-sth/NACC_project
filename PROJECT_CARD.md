# PROJECT_CARD

**Course:** Statistics Project, Fall 1405 (2026)
**Track:** C — NACC (multimodal MRI + UDS)

---

## 1. Dataset and subset

Pre-defined NACC subset provided by the teaching team (files received from the teaching assistants on 10 October 2026):

| File | Content | Size |
|---|---|---|
| `udslong_imputed.csv` | Selected Uniform Data Set (UDS) variables: demographic, medical, functional, cognitive, diagnostic | 1,237 rows x 180 columns |
| `mriscanclean.csv` | Regional MRI measures (cortical thickness `*_AVGTH` and volume `*_GVOL`; 31 regions per hemisphere), plus `NACCID` and `NACCUDSD` | 1,237 rows x 126 columns |

- **Linking key:** `NACCID`. Initial check: 1,237 unique IDs in both files, all shared, no duplicates (to be documented in the Phase 1 flow table).
- `combined_adjacency_matrix.csv` is **not** used in this project.
- **Initial variable scope** (fixed before any inferential analysis; see Section 5):
  - UDS: `NACCLIVS`, `TRAILB`, `NACCAGE`, `SEX`, `EDUC`
  - MRI: mean cortical thickness (`AVGTH`) of selected frontal regions

## 2. Working title

**Living situation, executive function, and frontal cortical thickness in older adults: a multimodal (UDS + MRI) analysis of an NACC subset**

## 3. Main statistical question

> Is living situation (`NACCLIVS`) associated with executive function (`TRAILB`) and with the cortical thickness of selected frontal regions in older adults?

Operationalised as three linked sub-questions:
1. Does executive function (`TRAILB`) differ between living-situation groups, accounting for age, sex and education?
2. Does frontal cortical thickness differ between living-situation groups, accounting for the same variables?
3. (Complementary, associational) Is frontal cortical thickness associated with executive function?

## 4. Unit of observation and interpretable population

- **Unit of observation:** one participant (one row per `NACCID`). Both files appear to contain a single row per participant; which visit was selected when the files were built will be confirmed with the teaching team and documented.
- **Analytic population (draft):** participants with `NACCAGE >= 65`, a valid `NACCLIVS` code (1-4), and a valid value of the analysed outcome.
  - Initial counts, participants aged 65+: **864**.
  - `NACCLIVS` among them: lives alone 195 | with spouse/partner 574 | with relative/friend 56 | with group 36 | other 1 | unknown 2.
  - These numbers are preliminary and will be replaced by the exact flow table in Phase 1.
- **Interpretable population:** participants of the teaching-team NACC subset (all have UDS and MRI data) who are aged 65 or older and have a valid `NACCLIVS` code (1-4); each analysis further requires its outcome to be usable (for `TRAILB` an observed value). This is a non-probability, volunteer-based sample, so results do not generalise to older adults in general.

## 5. Main variables and measurement scale

| Variable | Description | Type / scale | Source |
|---|---|---|---|
| `NACCLIVS` | Living situation: 1 = alone, 2 = with spouse/partner, 3 = with relative/friend, 4 = with group, 5 = other, 9 = unknown | Nominal (categorical) | UDS |
| `TRAILB` | Trail Making Test Part B completion time (seconds); executive-function measure, higher = worse performance. Has a 300 s cap and special codes (995-998) | Quantitative continuous (ratio) | UDS |
| `NACCAGE` | Age at visit (years) | Quantitative continuous | UDS |
| `SEX` | Sex | Binary | UDS |
| `EDUC` | Years of education (`99` = unknown, to be recoded as missing after checking the data dictionary) | Quantitative discrete | UDS |
| Frontal cortical thickness | Mean `AVGTH` (mm) of `CAUDALMIDDLEFRONTAL`, `ROSTRALMIDDLEFRONTAL` and `SUPERIORFRONTAL`, left and right hemispheres | Quantitative continuous | MRI |

The MRI variable is included because Track C requires real use of both UDS and MRI data.

## 6. Roles of the variables

- **Main explanatory / grouping variable:** `NACCLIVS`.
- **Cognitive response (UDS):** `TRAILB`.
- **Imaging response (MRI):** frontal cortical thickness composite (also used in later phases as an explanatory variable for `TRAILB`).
- **Initial adjusting variables:** `NACCAGE`, `SEX`, `EDUC`.
- **Planned model structure (Phase 4, may be refined with justification):** (A) response `TRAILB` (possibly transformed): only-UDS model (`NACCLIVS` + age, sex, education), only-MRI model (frontal thickness) and combined MRI + UDS model; (B) response frontal thickness: `NACCLIVS` + age, sex, education.

## 7. Type of question

Mainly **comparative** (executive function and frontal thickness across living-situation groups) with a secondary **associational** component (frontal thickness vs. `TRAILB`). The question is neither causal nor predictive.

## 8. Initial hypothesis

Older adults with different living situations, especially those living alone versus those living with a spouse/partner, may differ in executive-function performance and in frontal cortical thickness. Prior evidence on the direction is mixed, so tests will be two-sided. Formal null and alternative hypotheses will be written in Phase 3.

- **Pre-specified primary contrast:** lives alone vs. lives with spouse/partner (largest groups).
- **Secondary / exploratory:** comparison across all four groups and any single-region analyses; these will be labelled exploratory.

## 9. Initial limitations

1. **Sampling:** NACC participants are volunteers from research centres, not a random sample, so generalisability to older adults overall is limited.
2. **Observational and cross-sectional:** associations cannot be read as causal, and reverse causation is plausible (cognitive decline may change living situation). Living situation is also entangled with age, sex, marital status and health.
3. **Subgroup sizes:** the "relative/friend" and "group" categories are small and "other" has a single participant; `NACCLIVS = 9` is treated as missing.
4. **Measurement and missing data:** `TRAILB` is capped at 300 s and has special codes for non-completion. Failure to complete the test is more common in participants with dementia, so the availability of `TRAILB` is associated with observed diagnosis (not missing completely at random); the missingness may be explainable by observed variables (MAR), but MNAR mechanisms cannot be ruled out, and results may be biased towards participants able to complete the test.
5. **Imputed file:** the UDS file contains fractional values in whole-number variables, which suggests prior imputation or transformation by an unknown procedure; this is audited and documented in Phase 1.
6. **MRI:** no scanner/site information or total intracranial volume is available, the frontal composite is a simple mean of regional thickness, and a few implausible values (e.g. zero volume) exist.
7. **Multiplicity:** two outcomes and several regions raise multiple-testing concerns; the regions and the primary outcome are fixed in advance to limit this.

## 10. Pre-declared analytic decisions

- Population: `NACCAGE >= 65`; a `>= 60` threshold will be used as a sensitivity analysis in Phase 5.
- `NACCLIVS = 9` is treated as missing; category 5 (n = 1) is excluded or merged from group comparisons, with the reason documented.
- Special codes in `TRAILB` (and `EDUC = 99`) are recoded to missing on a working copy before analysis; the 300 s cap is treated as censoring: a log transformation alone is not enough, so rank-based methods and a sensitivity analysis excluding or censoring the capped values will be considered.
- Non-integer `TRAILB` values (a sign of prior imputation; some exceed the 300 s limit) are excluded from the primary definition of `TRAILB` and kept only in the Phase 5 sensitivity analysis (in-range values only).
- Phase 1 exploratory component (descriptive only, no tests): 12 frontal MRI measures (thickness and gray-matter volume of the same three regions, both hemispheres), `TRAILA`, `TRAILB`, `EDUC` and `NACCAGE` are examined with a Spearman correlation matrix and scatter plots, and the MRI measures are shown for all four living-situation groups. This does not change the confirmatory question or its pre-specified primary outcome; any later use of these variables (for example a volume composite) is declared in advance as a sensitivity analysis.
- The three frontal regions and the primary outcome (`TRAILB`) are fixed before any group comparison. Alternative definitions (e.g. `TRAILB - TRAILA`, `ANIMALS`, other frontal regions) are reserved for Phase 5 sensitivity analyses.
- Marital status (`MARISTAT`) and diagnostic group (`NACCUDSD`) are not in the initial adjustment set; they may be examined later, with justification, as confounders or sensitivity checks.
- Any substantive change to the main question after Phase 1 will be coordinated with the teaching team.
