# -*- coding: utf-8 -*-
"""Builds reports/phase1/phase1_report.tex from the SAME text, tables and figures as build_report.py.
Run:  python src/build_latex.py   then   cd reports/phase1 && pdflatex phase1_report.tex (twice)
Edit the report text in build_report.py (or the .tex directly) and the student name via STUDENT in build_report.py."""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent / "build_report.py"
text = SRC.read_text(encoding="utf-8")
head, rest = text.split("# ----------------------------------------------------------------------------- title", 1)
content = rest.split("def footer(c, d):", 1)[0]
content = "# --- title" + content if False else content  # content starts right after the title marker

ns = {"__file__": str(SRC)}
exec(head, ns)                      # imports, R, T, fmt, styles
out, cm_pt = [], ns["cm"]

# ----------------------------------------------------------------- markup -> LaTeX
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "{": r"\{", "}": r"\}",
           "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
def esc(s):
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    s = s.replace(">=", "\x01GE\x01").replace("<=", "\x01LE\x01")
    parts = re.split(r"(https?://[^\s,;)]+)", s)
    res = []
    for p in parts:
        if p.startswith("http"):
            res.append(r"\url{" + p.rstrip(".") + "}" + ("." if p.endswith(".") else ""))
            continue
        q = "".join(SPECIAL.get(ch, ch) for ch in p)
        q = q.replace("_", r"\_\allowbreak{}")
        res.append(q)
    s = "".join(res)
    return s.replace("\x01GE\x01", r"$\geq$").replace("\x01LE\x01", r"$\leq$")

TAGS = {"<b>": r"\textbf{", "</b>": "}", "<i>": r"\textit{", "</i>": "}", "</font>": "}", "<super>": r"\textsuperscript{",
        "</super>": "}", "<br/>": r"\\ "}
def conv(s):
    out_ = []
    for tok in re.split(r"(<[^>]+>)", str(s)):
        if re.fullmatch(r"<[^>]+>", tok) and (tok in TAGS or tok.startswith("<font")):
            out_.append(r"\texttt{" if tok.startswith("<font") else TAGS[tok])
        else:
            out_.append(esc(tok))
    return "".join(out_)

# ----------------------------------------------------------------- building blocks
def P(t, s=None):
    t = str(t); small = s is ns["BS"]
    if t.startswith("- "):
        body = r"\noindent\hangindent=1.2em\hangafter=1 $\bullet$\ " + conv(t[2:])
    else:
        body = conv(t)
    out.append(("{\\small " + body + "}" if small else body) + "\n")
def H(t, lvl=1): out.append((r"\section*{" if lvl == 1 else r"\subsection*{") + conv(t) + "}\n")
def NEWPAGE(): out.append(r"\newpage" + "\n")
def TITLE_LATEX(t): out.append(r"\begin{center}{\LARGE\bfseries " + conv(t) + r"}\end{center}" + "\n")
AVAIL_CM = 17.0
def tbl(df, widths=None, caption=None, nd=2, hdr=True):
    n = len(df.columns)
    w = [x / cm_pt for x in widths] if widths else [AVAIL_CM / n] * n
    pad = n * (2 * 2 / 28.45 + 0.03)                      # tabcolsep 2pt on both sides + rules
    k = min(1.0, (AVAIL_CM - pad) / sum(w)); w = [round(x * k, 2) for x in w]
    colspec = "|" + "|".join(r">{\raggedright\arraybackslash}p{%.2fcm}" % x for x in w) + "|"
    fm = ns["fmt"]
    header = " & ".join(r"\textbf{" + conv(c) + "}" for c in df.columns) + r" \\ \hline"
    rows = "\n".join(" & ".join(conv(fm(v, nd)) for v in r.values) + r" \\ \hline" for _, r in df.iterrows())
    long_ = len(df) >= 25
    if long_:
        out.append("{\\scriptsize\\setlength{\\tabcolsep}{2pt}\n\\begin{longtable}{" + colspec + "}\n\\hline\n\\rowcolor{hdr}" + header +
                   "\n\\endfirsthead\n\\hline\n\\rowcolor{hdr}" + header + "\n\\endhead\n" + rows + "\n\\end{longtable}}\n")
        if caption: out.append("{\\small\\textit{" + conv(caption) + "}}\\par\\medskip\n")
    else:
        out.append("\\begin{table}[H]\\centering\n{\\scriptsize\\setlength{\\tabcolsep}{2pt}\n\\begin{tabular}{" + colspec + "}\n\\hline\n\\rowcolor{hdr}" +
                   header + "\n" + rows + "\n\\end{tabular}}\n" +
                   (("\\par\\smallskip\n{\\small\\textit{" + conv(caption) + "}}\n") if caption else "") + "\\end{table}\n")
def fig(name, w=14.5, caption=""):
    out.append("\\begin{figure}[H]\\centering\n\\includegraphics[width=%.1fcm]{../../figures/%s}\\par\\smallskip\n{\\small\\textit{%s}}\n\\end{figure}\n" % (min(w, AVAIL_CM), name, conv(caption)))

ns.update(P=P, H=H, tbl=tbl, fig=fig, TITLE_LATEX=TITLE_LATEX, NEWPAGE=NEWPAGE)
content = re.sub(r'story\.append\(Paragraph\("Phase 1 Report: Study, Data, and Descriptive Statistics".*?\)\)\)\n',
                 'TITLE_LATEX("Phase 1 Report: Study, Data, and Descriptive Statistics")\n', content, flags=re.S, count=1)
content = content.replace("story.append(PageBreak())", "NEWPAGE()")
assert "TITLE_LATEX(" in content and "NEWPAGE()" in content
exec(content, ns)

preamble = r"""\documentclass[10pt,a4paper]{article}
\usepackage[a4paper,margin=2cm]{geometry}
\usepackage[T1]{fontenc}
\IfFileExists{lmodern.sty}{\usepackage{lmodern}}{}
\usepackage{graphicx}
\usepackage{float}
\usepackage{array}
\usepackage{longtable}
\usepackage[table]{xcolor}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\definecolor{hdr}{HTML}{DDE6F2}
\definecolor{navy}{HTML}{1F3A5F}
\usepackage{titlesec}
\titleformat{\section}{\large\bfseries\color{navy}}{}{0pt}{}
\titleformat{\subsection}{\normalsize\bfseries\color{navy}}{}{0pt}{}
\titlespacing*{\section}{0pt}{12pt}{6pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\sloppy
\pagestyle{fancy}\fancyhf{}
\fancyfoot[L]{\footnotesize\color{gray}Phase 1 report -- NACC Track C}
\fancyfoot[R]{\footnotesize\color{gray}Page \thepage}
\renewcommand{\headrulewidth}{0pt}
\begin{document}
"""
tex = preamble + "\n".join(out) + "\n\\end{document}\n"
dest = Path(__file__).resolve().parents[1] / "reports" / "phase1" / "phase1_report.tex"
dest.write_text(tex, encoding="utf-8")
print("wrote", dest, f"({len(tex)//1000} kB)")
