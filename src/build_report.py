# -*- coding: utf-8 -*-
"""Builds reports/phase1/phase1_report.pdf from the tables/figures produced by run_phase1.py.
Edit STUDENT and the text strings below, then run:  python src/build_report.py"""
import json
from pathlib import Path
import pandas as pd
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

STUDENT = "Hasti Mirshamsi, student ID 403100281"
ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT/"reports/phase1/tables"; FIG = ROOT/"figures"; OUT = ROOT/"reports/phase1/phase1_report.pdf"
R = json.load(open(TAB/"key_numbers.json"))
T = lambda n: pd.read_csv(TAB/f"{n}.csv")

ss = getSampleStyleSheet()
B  = ParagraphStyle("B", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
BS = ParagraphStyle("BS", parent=B, fontSize=8.5, leading=11)
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=14, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1F3A5F"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#1F3A5F"))
CAP = ParagraphStyle("CAP", parent=B, fontSize=8.5, leading=11, textColor=colors.HexColor("#333333"), spaceAfter=8)
TC = ParagraphStyle("TC", parent=B, fontSize=7.5, leading=9, spaceAfter=0)
TCB = ParagraphStyle("TCB", parent=TC, fontName="Helvetica-Bold")
story = []
P = lambda t, s=B: story.append(Paragraph(t, s))
def H(t, lvl=1): story.append(Paragraph(t, H1 if lvl == 1 else H2))
def fmt(x, nd=2):
    if isinstance(x, float):
        return f"{x:.{nd}f}".rstrip("0").rstrip(".") if abs(x) < 1000 and x != int(x) else f"{int(x)}" if x == int(x) else f"{x:.{nd}f}"
    return str(x)
def tbl(df, widths=None, caption=None, nd=2, hdr=True):
    data = [[Paragraph(str(c), TCB) for c in df.columns]] if hdr else []
    for _, r in df.iterrows(): data.append([Paragraph(fmt(v, nd), TC) for v in r.values])
    t = Table(data, colWidths=widths, repeatRows=1 if hdr else 0)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DDE6F2")),("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#999999")),
                           ("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2)]))
    block = [t] + ([Paragraph(caption, CAP)] if caption else [Spacer(1, 6)])
    story.append(KeepTogether(block) if len(df) < 25 else t)
    if len(df) >= 25 and caption: story.append(Paragraph(caption, CAP))
def fig(name, w=14.5, caption=""):
    im = PILImage.open(FIG/name); h = w*im.height/im.width
    story.append(KeepTogether([Image(str(FIG/name), width=w*cm, height=h*cm), Paragraph(caption, CAP)]))

# ----------------------------------------------------------------------------- title
story.append(Paragraph("Phase 1 Report: Study, Data, and Descriptive Statistics", ParagraphStyle("T", parent=ss["Title"], fontSize=19)))
P("<b>Living situation, executive function, and frontal cortical thickness in older adults: a multimodal (UDS + MRI) analysis of an NACC subset</b>", B)
P(f"Statistics Project, Fall 1405 (2026) | Track C (NACC, MRI + UDS) | Phase 1 | {STUDENT}", BS)
P("<b>Main question (PROJECT_CARD.md).</b> Is living situation (<font face='Courier'>NACCLIVS</font>) associated with executive function (<font face='Courier'>TRAILB</font>) and with the cortical thickness of selected frontal regions in older adults? "
  "This phase is purely descriptive: it documents where the data come from, what a row means, how UDS and MRI were linked, how good the data are, and how the main variables are distributed. No hypothesis tests are performed.", B)

gc = T("table_group_comparison").set_index("group"); qs = T("table_quantitative_summary").set_index("variable")
fl = T("table_sample_flow"); A_n = R["n_A"]

# ----------------------------------------------------------------------------- 1
H("1. Data source and collection mechanism")
P("<b>Source.</b> The data are a subset of the National Alzheimer's Coordinating Center (NACC) database that the teaching team prepared for Track C; the files were received from the teaching assistants on 10 October 2026. According to the NACC website, the database holds data on more than 56,000 participants collected over 25+ years at more than 40 Alzheimer's Disease Research Centers (ADRCs) funded by the National Institute on Aging, and is available to researchers on request. "
  "The <b>UDS</b> (Uniform Data Set) component contains standardized clinical information (demographics, medical history, medications, functional status, neuropsychological tests, clinical diagnosis); the <b>MRI</b> component contains regional brain measures for the participants in the subset.")
P(f"<b>Files used.</b> <font face='Courier'>udslong_imputed.csv</font> ({R['n_uds']} rows x {R['n_cols_uds']} columns) and <font face='Courier'>mriscanclean.csv</font> ({R['n_mri']} rows x {R['n_cols_mri']} columns). "
  "A third file (<font face='Courier'>combined_adjacency_matrix.csv</font>, a region-by-region adjacency matrix) is not used in this project.")
P("<b>Type of study.</b> The data come from clinical research centres, not from a probability survey and not from an experiment: this is an <b>observational</b> data set. Participants were not assigned to living situations, so any association we later find describes who lives how and how they perform, and cannot be read as an effect of living situation.")
P("<b>Access limits.</b> The raw files were provided by the teaching team and are not redistributed in the repository (see <font face='Courier'>data/README.md</font>). "
  "The file name says <i>imputed</i>, and decimals in whole-number variables suggest prior imputation or transformation by an unknown procedure (Section 6). The criteria that selected these 1,237 participants out of the full NACC database are not documented in the files; they must be treated as unknown.")

# ----------------------------------------------------------------------------- 2
H("2. Unit of observation and data structure")
P("<b>One row = one participant</b> (<font face='Courier'>NACCID</font>). Both files contain exactly one row per participant:")
tbl(T("table_rows_per_participant"), widths=[5*cm, 4*cm], caption="Table 1. Rows per participant in the UDS file (the MRI file has the same structure).")
P("Structure: UDS file (1,237 x 180) &lt;-- <font face='Courier'>NACCID</font>, one-to-one --&gt; MRI file (1,237 x 126). There is no hierarchy inside the delivered files (no repeated visit rows). "
  "However, the UDS is longitudinal by design and the file name (<i>udslong</i>) suggests it was derived from a long file with several visits per person. Neither file has a visit number or date, so <b>we cannot count visits per participant or say which visit was kept</b>. "
  "<b>Rule for the following phases:</b> the single delivered record per participant is the independent observation (so each person enters every analysis once). Which visit this record represents, and how close in time the UDS and MRI are, will be requested from the teaching team; until then this is stated as an open limitation.")

# ----------------------------------------------------------------------------- 3
H("3. Sampling, selection, and generalisability")
P("ADRC participants are volunteers who come to specialised centres, many through memory-clinic referral, community outreach, or family history. The sample is therefore <b>not random</b> and not representative of older adults in general. The data themselves show typical features of such a sample "
  f"(sample A: aged 65+ with a valid living situation, n = {A_n}; 864 participants are 65+ before excluding the 3 with NACCLIVS = 5 or 9): median education {qs.loc['Education (years)','median']:.0f} years, 57.1% women, 66.7% living with a spouse or partner, and 65.5% with normal cognition (Table 8a). "
  "Only people who have an MRI are included, which may add another layer of selection (people able and willing to be scanned). "
  "<b>Interpretable population:</b> NACC participants of this subset who are aged 65+ and have the required data. Statements about older adults in general are not supported.")

# ----------------------------------------------------------------------------- 4
H("4. Variable map and classification (C.1, task 4)")
P("The complete maps are in <font face='Courier'>reports/phase1/tables/variable_map_uds.csv</font> and <font face='Courier'>variable_map_mri.csv</font>. Table 2 summarises the UDS variables by domain; the <i>scale</i> of each column was inferred from its values and must be confirmed in the RDD (variable guide).")
dc = T("table_uds_domain_counts").rename(columns={"n_variables":"n variables"})
tbl(dc, widths=[3*cm, 7*cm, 3*cm], caption="Table 2. UDS variables by domain and sub-domain (179 variables besides NACCID). 'Medical' also holds behavioural (NPI-Q) and mood (GDS) items.")
P(f"<b>MRI.</b> {R['n_mri_vars']} columns = {R['n_mri_regions']} cortical regions x 2 hemispheres (LH/RH) x 2 measures: <font face='Courier'>GVOL</font> (gray-matter volume, mm<super>3</super>) and <font face='Courier'>AVGTH</font> (average cortical thickness, mm); these units were provided for this data set and are to be cross-checked against the RDD. "
  "The region names (e.g. CAUDALMIDDLEFRONTAL, ENTORHINAL) follow a FreeSurfer-style cortical parcellation; units and processing details must be confirmed in the RDD. By lobe: 10 frontal, 5 parietal, 7 temporal, 4 occipital, 4 cingulate and 1 insular region.")
mv = T("table_main_variables")
tbl(mv.rename(columns={"type / scale":"type / scale","role (from PROJECT_CARD)":"role"}), widths=[2.2*cm,1.7*cm,3.3*cm,3.3*cm,3*cm,3*cm],
    caption="Table 3. Main variables, scale of measurement, role, and the summaries/plots this classification implies.")
P("<b>Frontal thickness composite.</b> FRONTAL_THK is the simple mean of six values: AVGTH of caudal middle frontal, rostral middle frontal and superior frontal regions in the left and right hemispheres. "
  f"The left and right means correlate at r = {R['front_lh_rh_r']:.2f} in the analytic sample, which supports combining them. The regions were fixed in the project card before looking at any group comparison.")

# ----------------------------------------------------------------------------- 5
H("5. Linking UDS and MRI (C.3) and analytic sample")
tbl(T("table_linkage_flow"), widths=[9*cm, 3*cm], caption="Table 4. Linkage of the two files by NACCID.")
P("The two files contain the same 1,237 participants, with no unmatched records and no duplicate IDs. The diagnosis variable <font face='Courier'>NACCUDSD</font>, present in both files, is identical for every participant after linking (a useful check that the link is correct). "
  "<b>All 1,237 delivered participants therefore have both modalities.</b>")
tbl(fl, widths=[11*cm, 2.5*cm], caption="Table 5. Flow from the linked data to the analytic sample A (age >= 65, valid NACCLIVS in 1-4) and availability of the main variables.")
ex = T("table_exclusions")
P(f"Exclusions from the linked data: {int(ex.n_excluded[0])} participants younger than 65 (age range of the file {R['age_min']:.0f}-{R['age_max']:.0f}); "
  f"{int(ex.n_excluded[1])} participant with NACCLIVS = 5 (other), too small to analyse as a group; {int(ex.n_excluded[2])} with NACCLIVS = 9 (unknown). "
  "The 65+ threshold is the pre-declared definition of 'older adults' in the project card (a threshold of 60 will be used as a sensitivity analysis in Phase 5).")

# ----------------------------------------------------------------------------- 6
H("6. Data-quality audit (task 5)")
P("Expected ranges and special codes below follow NACC conventions and should be double-checked against the RDD; the code only counts and flags and never deletes participants.")
au = T("table_audit_main_variables").rename(columns={"n_non_integer(imputed?)":"n non-integer","n_non_integer_out_of_range":"n non-int. out of range","n_integer_out_of_range":"n int. out of range","n_special_code":"n special code"})
tbl(au, widths=[1.9*cm,1.7*cm,2.8*cm,1.2*cm,1.6*cm,1.7*cm,2.3*cm,2.3*cm], caption="Table 6a. Audit of the variables used in the project (+ MARISTAT, MOCATOTS, NACCAPOE).")
P(f"<b>Missing values.</b> There are no NaN cells in either file (UDS {R['nan_uds']}, MRI {R['nan_mri']}), but this does not mean complete data: unknown/not-done answers are stored as special codes (for example 995-998 for the trail-making tests, 99 for education, 9 for living situation, 278 participants with APOE = 9).")
P(f"<b>Imputation.</b> Questionnaire and test variables that should only contain whole numbers contain decimals: <b>{R['n_imputed_cols']} columns, {R['n_imputed_cells']:,} cells, {R['n_part_with_imputed']} of {R['n_uds']} participants</b> have at least one such value (table_suspected_imputed_columns.csv). "
  "<b>Suspected prior imputation or transformation; the exact procedure is unknown.</b> Decimals in whole-number variables do not prove a specific method. Some of these values are impossible for the instrument (e.g. a Trails B time of 523.6 s when the test stops at 300 s). The method, whether MRI values were also processed, and whether the file is the final analysis-ready version must be asked from the teaching team (Section 13).")
tc = T("table_trail_value_classes"); tc.columns = ["value class","TRAILB n","TRAILA n","TRAILB %","TRAILA %"]
tbl(tc, widths=[4.5*cm,2.2*cm,2.2*cm,2.2*cm,2.2*cm], caption="Table 6b. Classification of all Trail Making values in the file (TRAILB limit 300 s, TRAILA limit 150 s).")
P(f"<b>TRAILB.</b> 87.2% of TRAILB values are ordinary observed times; 4.4% are at the 300 s limit (true time is at least 300 s: <i>censored</i>); 4.4% are special codes (test not completed: physical, cognitive or other problem, or refusal); and 3.9% are non-integer values judged to be imputed (9 beyond 300 s). "
  f"In sample A, {R['n_A_trailb']} of {A_n} participants have an observed TRAILB (<b>{100*R['n_A_trailb']/A_n:.1f}%</b>); allowing in-range imputed values would add {R['n_A_trailb_imp']-R['n_A_trailb']}. "
  "The primary definition uses observed values only; the version with in-range imputed values is kept for the Phase 5 sensitivity analysis.")
lg = T("table_logic_checks")
tbl(lg, widths=[8*cm,1.2*cm,5.5*cm], caption="Table 6c. Logical-consistency checks.")
P("No contradictory diagnosis/CDR pairs and no impossible ages or education were found. The flagged living situation vs marital status combinations (for example living alone while married or in a domestic partnership) are plausible and kept.")
P(f"<b>MRI.</b> No NaN. Volumes: {R['mri_gvol_le0']} zero values (LH entorhinal, LH posterior cingulate), not used in this project. Thickness below 1 mm is biologically unlikely and probably a segmentation error: {R['mri_th_lt1_cells']} such cells in {R['mri_th_lt1_part']} participants across all regions; "
  f"in the six frontal values used here, {R['front_lt1_cells']} cells in {R['front_lt1_part']} participants ({R['front_flag_A']} in sample A). They are flagged (FRONTAL_flag_lt1mm), not deleted; their influence will be examined in Phases 4-5.")
dec = T("table_data_decisions")
tbl(dec.rename(columns={"how many":"how many"}), widths=[3.7*cm,3.2*cm,4.3*cm,4.3*cm], caption="Table 6d. Decision for every data problem and the reason.")

cv = pd.DataFrame([
 ("NACCLIVS: 1 alone, 2 spouse/partner, 3 relative/friend, 4 group, 5 other, 9 unknown","Verified","Variable page of the RDD provided for NACCLIVS (derived variable, numeric longitudinal)."),
 ("NACCUDSD: 1 normal, 2 impaired-not-MCI, 3 MCI, 4 dementia","Verified (secondary check)","NACC documentation lists NACCUDSD as 'Cognitive status at UDS visit'; the four labels and numeric order match a published coding supplement. Confirm order in the RDD."),
 ("TRAILB: 0-300 s, 300 = not finished by 300 s; 995 physical, 996 cognitive/behaviour, 997 other problem, 998 verbal refusal","Verified","Official NACC UDS Form C2 (and C1) instructions."),
 ("TRAILA: 0-150 s, 150 = not finished by 150 s; same codes 995-998; TRAILARR/TRAILALI = commission errors (0-40) / correct lines (0-24)","Verified","Official NACC UDS Form C2 (and C1) instructions."),
 ("SEX (1 male, 2 female), EDUC (0-36, 99 unknown), MARISTAT labels, MOCATOTS (0-30, 88), NACCAPOE (9 missing)","Not yet verified","Based on NACC conventions; remain a limitation until checked in the RDD."),
 ("MRI units: AVGTH in mm, GVOL in mm^3","Provided, to cross-check","Units provided for this data set; to be confirmed in the RDD."),
], columns=["coding used in this report","status","source / note"])
tbl(cv, widths=[6.8*cm,2.6*cm,6.2*cm], caption="Table 6e. Verification status of the variable coding used in this report.")

# ----------------------------------------------------------------------------- 7
H("7. Missing data and selection of the multimodal sample (C.4)")
mt = T("table_missingness_main").rename(columns={"n_unavailable_all":"n (all 1,237)","pct_all":"% (all)","n_unavailable_A":f"n (A, {A_n})","pct_A":"% (A)"})
tbl(mt, widths=[5.6*cm,2.3*cm,1.6*cm,2.5*cm,1.6*cm], caption="Table 7a. Unavailable values in the main variables (NaN, special code, or not usable under the primary definition).")
P("Only TRAILB has a noticeable amount of unavailable data. In the MRI file nothing is missing. <b>We cannot compare participants with and without MRI</b>, because both delivered files describe the same 1,237 participants (the UDS file is also restricted to people with MRI), so there is no UDS-only comparison group; the possible selection into the MRI subset therefore remains a limitation we can describe but not measure. "
  "What we can examine is who has an unusable TRAILB:")
sel = T("table_selection_trailb_usable").set_index("TRAILB_status").T.reset_index().rename(columns={"index":"(sample A)"})
tbl(sel, widths=[4*cm,3.2*cm,3.2*cm], caption="Table 7b. Participants in A with and without a usable TRAILB (descriptive).")
P("People without a usable TRAILB are similar in age, sex and education, but <b>44.4% of them have dementia versus 7.5% of those with a usable TRAILB</b>. The availability of TRAILB is therefore associated with the observed cognitive diagnosis, suggesting that the data are not Missing Completely At Random (MCAR). The missingness may be explainable by observed variables such as diagnosis (MAR), although MNAR mechanisms cannot be ruled out; this analysis cannot tell MAR from MNAR. Later results for TRAILB mostly describe participants able to complete the test.")

# ----------------------------------------------------------------------------- 8
H("8. Frequency tables, centre and spread (tasks 6-7)")
ft = T("table_frequencies")
ftA = ft[ft.variable.isin(["NACCLIVS (sample A)","SEX (sample A)","NACCUDSD (sample A)"])][["variable","category","n","pct"]]
tbl(ftA, widths=[4.5*cm,4.5*cm,2*cm,2*cm], caption="Table 8a. Frequency tables for the sample A (percentages sum to 100 within each variable).")
ftl = ft[ft.variable=="NACCLIVS (all 1,237)"][["category","n","pct"]]
P(f"<b>Reading the tables.</b> About two thirds live with a spouse or partner (66.7%) and 22.6% live alone, while 'relative/friend' (n = 56) and 'group' (n = 36) are small; the 'other' category (n = 1) and 'unknown' (n = 2) could not be analysed. "
  "Women are 57.1% of the sample. Nearly one third are impaired in some way (23.6% MCI, 10.2% dementia); the 'impaired-not-MCI' group has only 6 people and cannot be analysed as a separate group.")
qq = qs.reset_index().rename(columns={"index":"variable","n_unavailable":"missing","n_outliers_1.5IQR":"Tukey outliers"})
qq = qq[["variable","n","missing","mean","sd","min","Q1","median","Q3","max","IQR","skewness","Tukey outliers"]]
tbl(qq, widths=[3.1*cm,0.9*cm,1.1*cm,1.2*cm,1*cm,1*cm,1*cm,1.2*cm,1*cm,1*cm,1*cm,1.3*cm,1.3*cm], caption="Table 8b. Summary of the quantitative variables (sample A). TRAILB is based on observed values only.")
P(f"<b>Which measure suits which variable.</b> <i>Age</i> (mean {qs.loc['Age (years)','mean']:.1f}, SD {qs.loc['Age (years)','sd']:.1f}; median {qs.loc['Age (years)','median']:.0f}) is mildly right-skewed (skewness {qs.loc['Age (years)','skewness']:.2f}); mean/SD and median/IQR agree closely, either can be used. "
  f"<i>Education</i> is left-skewed with a ceiling (median {qs.loc['Education (years)','median']:.0f}, IQR {qs.loc['Education (years)','IQR']:.0f}) so median/IQR is more appropriate. "
  f"<i>TRAILB</i> is strongly right-skewed (skewness {qs.loc['TRAILB, observed (s)','skewness']:.2f}; mean {qs.loc['TRAILB, observed (s)','mean']:.0f} s versus median {qs.loc['TRAILB, observed (s)','median']:.0f} s), with a pile-up at the 300 s limit; the median/IQR ({qs.loc['TRAILB, observed (s)','Q1']:.0f}-{qs.loc['TRAILB, observed (s)','Q3']:.0f} s) describes a typical participant, and the log scale reduces skewness to {qs.loc['log10 TRAILB','skewness']:.2f}, which is why a log transform will be considered in Phases 3-4. "
  f"<i>Frontal thickness</i> is nearly symmetric in the centre (mean {qs.loc['Frontal thickness (mm)','mean']:.2f} mm, SD {qs.loc['Frontal thickness (mm)','sd']:.2f}) but has a long left tail from a few implausibly low values (minimum {qs.loc['Frontal thickness (mm)','min']:.2f} mm; skewness {qs.loc['Frontal thickness (mm)','skewness']:.2f}); mean/SD are sensitive to these, so median/IQR will be reported alongside.")

# ----------------------------------------------------------------------------- 9
H("9. Figures (task 8)")
fig("fig1_living_situation.png", 10.5, "Figure 1. Counts and percentages of the four living-situation groups. The two small groups (relative/friend, group) limit any later comparison involving them.")
fig("fig2_trailb_hist.png", 15.5, "Figure 2. Distribution of observed TRAILB times. The spike at 300 s is the test time limit (censoring); the log scale (b) makes the shape more symmetric.")
fig("fig3_trailb_by_living.png", 11.5, "Figure 3. TRAILB by living situation. Boxes overlap strongly; many outliers are high times, several at the 300 s limit. Descriptive only.")
fig("fig4_frontal_thickness_hist.png", 10.5, "Figure 4. Frontal thickness composite (mean of 6 regional values). The x-axis extends to 1.0 mm because of a few implausibly low values (visible as isolated points in Figure 5).")
fig("fig5_thickness_by_living.png", 11.5, "Figure 5. Frontal thickness by living situation. The y-axis does not start at 0 because the box position, not its length from zero, carries the information. The medians are nearly the same in all groups.")
fig("fig6_scatter_trailb_thickness.png", 10.5, "Figure 6. TRAILB (log scale) versus frontal thickness; each point is one participant (n = 798). The horizontal line of points at 300 s is the censoring limit. The two points far left are the implausibly thin values.")
fig("fig7_age_by_living.png", 11.5, "Figure 7. Age by living situation. The minimum is 65 by definition of sample A. Age is similar across groups.")
fig("fig8_missingness.png", 12.5, "Figure 8. Percentage of participants in A with an unavailable value in each main variable.")

# ----------------------------------------------------------------------------- 10
H("10. Descriptive comparison across living situations (task 9)")
g = gc
cmp_ = pd.DataFrame({
 "": ["n","Age, mean (SD)","Women, %","MCI, %","Dementia, %","TRAILB: n with observed value","TRAILB median [Q1-Q3], s","TRAILB mean (SD), s","TRAILB at 300 s limit, %","Frontal thickness, mean (SD), mm"]})
for grp in g.index:
    r = g.loc[grp]
    cmp_[grp] = [f"{int(r.n)}", f"{r.age_mean:.1f} ({r.age_sd:.1f})", f"{r.pct_female:.0f}", f"{r.pct_MCI:.0f}", f"{r.pct_dementia:.0f}", f"{int(r.TRAILB_n)}",
                 f"{r.TRAILB_median:.0f} [{r.TRAILB_Q1:.0f}-{r.TRAILB_Q3:.0f}]", f"{r.TRAILB_mean:.0f} ({r.TRAILB_sd:.0f})", f"{r.pct_TRAILB_at_300:.1f}", f"{r.THK_mean:.2f} ({r.THK_sd:.2f})"]
cmp_ = cmp_[["", "Alone","Spouse/partner","Relative/friend","Group"]]
tbl(cmp_, widths=[5.4*cm,2.5*cm,2.8*cm,2.8*cm,2.2*cm], caption="Table 10. Descriptive comparison of sample A by living situation (no tests, no inference).")
P(f"<b>What the numbers show.</b> Median TRAILB time was {g.loc['Alone','TRAILB_median']:.0f} s (alone), {g.loc['Spouse/partner','TRAILB_median']:.0f} s (spouse/partner), {g.loc['Relative/friend','TRAILB_median']:.0f} s (relative/friend) and {g.loc['Group','TRAILB_median']:.0f} s (group), with large spread inside each group (interquartile ranges overlap heavily). "
  f"The two small groups have the higher medians, but they contain only {int(g.loc['Relative/friend','TRAILB_n'])} and {int(g.loc['Group','TRAILB_n'])} participants with an observed TRAILB. Mean frontal thickness is {g.loc['Alone','THK_mean']:.2f}-{g.loc['Relative/friend','THK_mean']:.2f} mm in all groups: practically identical in this sample.")
P(f"<b>Groups differ in who they contain.</b> {g.loc['Alone','pct_female']:.0f}% of those living alone are women compared with {g.loc['Spouse/partner','pct_female']:.0f}% of those living with a spouse/partner; dementia is recorded for {g.loc['Alone','pct_dementia']:.1f}% of those living alone but {g.loc['Spouse/partner','pct_dementia']:.1f}% of those living with a spouse/partner. "
  "Sex, cognitive status and living situation are thus entangled. Any later difference in TRAILB between groups may reflect these other factors, which is why sex, age and education (and, in sensitivity analyses, diagnosis) matter in Phases 3-4. This phase does not claim that any difference exists in the population.")

nd = T("table_living_by_diagnosis_n_pct")
tbl(nd, widths=[3.2*cm,2.6*cm,3*cm,2.8*cm,2.8*cm,1.6*cm], caption="Table 10b. Cognitive diagnosis (NACCUDSD) by living situation in sample A: number of participants (row percentage).")
P(f"<b>Why diagnosis matters for the research question.</b> Cognitive status is distributed very differently across living situations: dementia is recorded for {g.loc['Alone','pct_dementia']:.1f}% of participants living alone versus {g.loc['Spouse/partner','pct_dementia']:.1f}% living with a spouse/partner, {g.loc['Relative/friend','pct_dementia']:.1f}% with a relative/friend and {g.loc['Group','pct_dementia']:.1f}% in a group setting (the 'impaired-not-MCI' category has too few people to interpret). "
  "Because diagnosis is also strongly related to whether TRAILB can be obtained (Table 7b), it could confound a living situation - TRAILB association, or lie on its pathway (for example, cognitive decline leading to a change in living arrangements). The project card keeps age, sex and education as the initial adjusting variables; diagnosis is planned as a stratification or sensitivity variable in later phases, and its role must be stated explicitly in any interpretation.")

# ----------------------------------------------------------------------------- 11
H("11. Joint cognitive and imaging summary (C.5)")
js = T("table_joint_summary").rename(columns={"n_unavailable":"missing","n_outliers_1.5IQR":"Tukey outliers"})
js = js[["variable","n","mean","sd","min","Q1","median","Q3","max","IQR","skewness","Tukey outliers"]]
tbl(js, widths=[3.3*cm,1*cm,1.3*cm,1.1*cm,1.1*cm,1.1*cm,1.3*cm,1.1*cm,1.1*cm,1.1*cm,1.4*cm,1.3*cm], caption=f"Table 11. TRAILB (UDS) and frontal thickness (MRI) in the {R['n_joint']} participants of A who have both.")
P(f"TRAILB ranges from 28 to 300 s (median 82, IQR 51) and is strongly right-skewed with 69 Tukey outliers (46 of them the censored values at 300 s). Frontal thickness is tightly concentrated (mean 2.38 mm, SD 0.12) with 14 Tukey outliers (12 unusually thin, 2 unusually thick). "
  "The two measures live on different scales and have different uncertainty, which is why they are summarised separately here. Figure 6 shows no obvious pattern by eye; the covariance and correlation will be examined formally in Phase 2 and Phase 4, and nothing causal can be concluded from such a plot.")

# ----------------------------------------------------------------------------- 11b
H("11b. Exploratory component: 12 frontal MRI measures (descriptive only)")
P("<b>Purpose and rules.</b> Before any test, we looked at how the frontal MRI measures relate to each other, to age and education, and to the Trail Making tests. "
  "The 12 MRI measures are thickness (AVGTH) and gray-matter volume (GVOL) of caudal middle frontal, rostral middle frontal and superior frontal regions in both hemispheres. "
  "This part is <b>exploratory and descriptive</b>: Spearman rank correlations (robust to the skewness of TRAILA/TRAILB and to extreme thickness values) with pairwise-complete data, <b>no p-values</b>, and it was <b>not used to choose the confirmatory question</b>, which was fixed in the project card.")
ex = T("table_exploratory_mri_vs_others")
tbl(ex, widths=[4.5*cm,2.5*cm,2.5*cm,2.5*cm,2.5*cm], caption="Table 12. Spearman correlation of each frontal MRI measure with TRAILB, TRAILA, age and education (sample A; TRAILA/TRAILB observed values only).")
fig("fig9_correlation_matrix.png", 16.5, "Figure 9. Exploratory correlation matrix of the 12 MRI measures, TRAILA, TRAILB, education and age. Values are descriptive rank correlations.")
P("<b>What the matrix shows.</b>")
for t in [
 f"MRI measures and TRAILB: all correlations are weak ({R['rho_mri_trailb_range'][0]:.2f} to {R['rho_mri_trailb_range'][1]:.2f}). Gray-matter volumes (-0.14 to -0.18) are slightly more strongly related to TRAILB than thickness (-0.04 to -0.12). The sign is the same everywhere: smaller or thinner frontal regions go with a longer (worse) TRAILB time.",
 f"Background variables matter as much as the MRI: TRAILB correlates {R['rho_age_trailB']:.2f} with age and {R['rho_educ_trailB']:.2f} with education, and TRAILA and TRAILB correlate {R['rho_trailA_trailB']:.2f}. Volumes also correlate with education (0.07 to 0.16), so part of the volume-TRAILB association may be shared with these variables.",
 "Strong overlap among MRI measures: thickness measures correlate 0.46-0.86 with one another and volumes 0.53-0.86; left and right values of the same region correlate 0.66-0.86. Entering all 12 as separate predictors in a regression would therefore cause multicollinearity (Phase 4), which supports using a small number of composites.",
 "Thickness and volume of the same region are only weakly related (0.13-0.29), so they carry different information. Volume also depends on head size, and no intracranial volume is available in the files.",
]: P("- " + t, B)
fig("fig10_mri_vs_trailb.png", 13.5, "Figure 10. Each frontal MRI measure against TRAILB (rows: left thickness, right thickness, left volume, right volume; columns: three regions). Spearman rho in each panel title; exploratory.")
fig("fig11_mri_vs_age.png", 13.5, "Figure 11. Each frontal MRI measure against age (exploratory).")
fig("fig12_thickness_volume_lr.png", 15.5, "Figure 12. Top: thickness vs volume per region; bottom: right vs left thickness (dashed line y = x).")
fig("fig13_mri_by_living.png", 13.5, "Figure 13. All 12 MRI measures by living situation (alone, spouse/partner, relative/friend, group). Descriptive; the code 5 participant is excluded and code 9 is treated as missing.")
P(f"<b>MRI measures by living situation.</b> Median thickness is almost identical in the four groups (for example left superior frontal 2.48-2.52 mm). Median volumes differ by up to about 6% between groups (right superior frontal 22,547-23,893 mm<super>3</super>) without a consistent pattern; with 56 and 36 participants in two groups and no head-size adjustment, these differences should not be over-read. "
  f"Frontal volumes also contain a few very low values (minimum {R['gvol_frontal_min']:.0f} against a median of roughly 5,400 for caudal middle frontal), probably segmentation errors that will be examined with influence diagnostics in Phases 4-5.")
P("<b>Cautions and consequences.</b> With 16 variables there are 120 pairs; even small correlations can look 'interesting' by chance, and picking the strongest pair and then testing it would be circular. Any later test of these variables will be pre-declared and, if many are tested, adjusted for multiplicity (e.g. FDR). "
  "<b>Decisions:</b> (1) the confirmatory plan keeps the pre-specified thickness composite and TRAILB; (2) a volume composite of the same six regions is declared now as a Phase 5 sensitivity definition, so that it is not a result-driven choice; (3) living situation is examined across all four groups descriptively, while the primary contrast stays alone versus spouse/partner.")

# ----------------------------------------------------------------------------- 12
H("12. Final statistical question and why these data fit (task 10)")
P("<b>Question (unchanged from the project card).</b> Is living situation (NACCLIVS) associated with executive function (TRAILB) and with the cortical thickness of selected frontal regions (mean AVGTH of caudal middle frontal, rostral middle frontal and superior frontal regions) among participants aged 65 or older in the NACC subset?")
P("<b>Precision gained from this phase.</b> (i) Analytic sample A (n = 861: subset participants aged 65+ with valid NACCLIVS 1-4; 864 are 65+ before excluding NACCLIVS 5 and 9); usable-outcome subsamples: TRAILB n = 798, frontal thickness n = 861. (ii) Primary contrast: alone (n = 195) versus with spouse/partner (n = 574); the two other groups (n = 56 and 36) are described and used only in secondary, exploratory comparisons. (iii) Primary TRAILB definition: observed values only (n = 798); the 300 s limit is a censoring problem: a log transformation alone is not enough, so rank-based methods and a sensitivity analysis excluding or censoring the capped values will be considered. (iv) Covariates: age, sex, education. "
  "(v) The primary imaging outcome is the six-value frontal composite; individual regions are exploratory.")
P("<b>Sub-questions (so that the question, the analysis and the models match).</b> (1) Does executive function (TRAILB) differ between living-situation groups, accounting for age, sex and education? (2) Does frontal cortical thickness differ between living-situation groups, accounting for the same variables? (3) Complementary, associational: is frontal cortical thickness associated with executive function? "
  "<b>Planned models (Phase 4):</b> (A) response TRAILB: only-UDS (living situation + age, sex, education), only-MRI (frontal thickness) and combined models; (B) response frontal thickness: living situation + age, sex, education.")
P("<b>Why the data are suitable.</b> Both modalities are available for every participant, the key variables are measured with standard instruments, one record per person guarantees independent observations, and the two largest groups are big enough for a comparison. "
  "<b>Where they are not ideal:</b> non-random sample, unknown imputation, cross-sectional living situation, small subgroups, and missing TRAILB linked to dementia.")

# ----------------------------------------------------------------------------- 13
H("13. Limitations noted in this phase")
for t in [
 "<b>Selection and generalisability:</b> volunteers in research centres, only participants with MRI, and unknown criteria for building the subset; no statement about older adults in general.",
 "<b>Observational data:</b> living situation is not assigned; reverse causation (cognitive decline changing living arrangements) and confounding by sex, age, health and marital status are plausible.",
 "<b>Unknown visit selection:</b> the delivered record per participant has no visit date; the time gap between UDS and MRI is unknown.",
 f"<b>Imputation:</b> {R['n_imputed_cols']} columns contain decimal values that suggest prior imputation or transformation; the procedure is unknown. In TRAILB these were excluded from the primary definition.",
 "<b>TRAILB:</b> censored at 300 s, special codes for not completed, and unusable results more common in dementia (44% vs 7.5%).",
 "<b>MRI:</b> no scanner/site or intracranial volume information (so volumes are not head-size adjusted); the frontal composite is an unweighted mean; a few thickness values below 1 mm and very low volumes are probably segmentation errors; the 12 MRI measures are strongly inter-correlated.",
 "<b>Coding not fully cross-checked:</b> SEX, EDUC, MARISTAT, MOCATOTS and NACCAPOE codes and the MRI units are not yet verified against the RDD (Table 6e); they remain a limitation until confirmed.",
 "<b>Small groups:</b> 'relative/friend' (n = 56) and 'group' (n = 36); 'other' (n = 1) excluded.",
]: P("- " + t, B)


P("<b>Open questions for the teaching team</b> (answers will be added to the report):")
for t in ["Which visit does the single record per participant represent, and how far apart in time are the UDS and MRI data?",
          "Which imputation or transformation was applied to the UDS file, and for which variables?",
          "Were the MRI values also processed or replaced? Is the delivered file the final, analysis-ready version?",
          "Is an intracranial-volume (head-size) measure available, and do the RDD units (AVGTH in mm, GVOL in mm^3) match those provided?"]:
    P("- " + t, B)

# ----------------------------------------------------------------------------- 14
H("14. Reproducibility")
P("All numbers and figures in this report are produced by <font face='Courier'>src/run_phase1.py</font> (same code as <font face='Courier'>notebooks/phase1_analysis.ipynb</font>) from the two CSV files placed in <font face='Courier'>data/</font>; the report is built by <font face='Courier'>src/build_report.py</font>. "
  "Environment: Python 3 with pandas, numpy, scipy, matplotlib (see requirements.txt). Fixed seed is not needed in this phase (no randomness). Tables are in <font face='Courier'>reports/phase1/tables/</font>, figures in <font face='Courier'>figures/</font>.")
P("<b>References.</b> NACC, About NACC Data, https://www.naccdata.org/about-nacc-data/ (accessed for this report); NACC Researcher's Guide and Data Forms (RDD) for variable definitions; NACC UDS Forms C1/C2 (Neuropsychological Battery), https://files.alz.washington.edu/documentation/uds3-ivp-c2.pdf and NACC UDS derived variables, https://files.alz.washington.edu/documentation/uds2-dervar.pdf; Wonnacott and Wonnacott, <i>Introductory Statistics</i>, 5th ed., Wiley.", BS)


# ----------------------------------------------------------------------------- appendix
story.append(PageBreak())
H("Appendix A. Variable map of the UDS file (C.1)")
P("Domain and sub-domain were assigned by variable name and must be confirmed in the RDD; 'see RDD' means no description was written. The full table with inferred scale, range and number of distinct values is in <font face='Courier'>reports/phase1/tables/variable_map_uds.csv</font>.", BS)
vm = T("variable_map_uds")[["variable","domain","subdomain","description"]]
tbl(vm, widths=[2.6*cm,2.2*cm,4.2*cm,8*cm], caption="Table A1. UDS variables (179) with domain, sub-domain and description.")
H("Appendix B. Variable map of the MRI file (C.1)")
mm = T("variable_map_mri")
lob = mm.groupby("lobe").region.apply(lambda x: ", ".join(sorted(set(x)))).reset_index().rename(columns={"region":"regions (each has LH/RH x GVOL/AVGTH)"})
tbl(lob, widths=[2.4*cm,13.2*cm], caption="Table B1. The 31 cortical regions by lobe. GVOL = gray-matter volume (mm^3); AVGTH = average cortical thickness (mm); units as provided for this data set, to be cross-checked against the RDD. Column names: {LH|RH}_{REGION}_{GVOL|AVGTH}.")

def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
    c.drawString(1.8*cm, 1.1*cm, "Phase 1 report - NACC Track C"); c.drawRightString(A4[0]-1.8*cm, 1.1*cm, f"Page {d.page}"); c.restoreState()
doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=1.8*cm, rightMargin=1.8*cm, topMargin=1.6*cm, bottomMargin=1.8*cm,
                        title="Phase 1 Report - NACC Track C", author=STUDENT)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
