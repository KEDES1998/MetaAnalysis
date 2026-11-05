# CLAUDE.md – Projektkontext

Seminararbeit im MA-Seminar «Meta-Analysis» (Prof. Rainer Winkelmann, UZH, HS 2026).
Wir **replizieren und erweitern** die Meta-Analyse von Zschirnt & Ruedin (2016) zu ethnischer Diskriminierung bei Bewerbungen.
Der Arbeitsplan mit allen Schritten und Fristen steht in **`PLAN.md`** – vor grösseren Arbeiten dort nachschauen und erledigte Punkte abhaken.

---

## Team, Fristen, Abgabe

- Team: Kevin de Silva und Vanessa Allenspach, Group 4
- **Bericht:** Fr 13.11.2026, bis Mitternacht, per E-Mail an rainer.winkelmann@econ.uzh.ch. Dateiname `group4.pdf`. Ca. 10, max. 15 Seiten ohne Anhang. Titelseite mit Titel und beiden Namen. Vollständige Liste aller untersuchten Studien im Literaturverzeichnis.
- **Präsentation:** Di 24.11.2026 (Gruppen 4–6; Gruppen 1–3 am 17.11.), 20 Min. + 10 Min. Diskussion, beide präsentieren. Folien (PDF/PPT) spätestens am Präsentationstag an den Prof mailen.
- Note: Bericht 50 %, Präsentation 40 %, Mitarbeit 10 %.
- KI-Agenten dürfen laut Prof frei verwendet werden.

## Sprache und Stil

- **Mit dem Team:** Deutsch. Einfach und Schritt für Schritt erklären; bei schwierigen Konzepten lieber ausführlicher.
- **Bericht, Folien, Code, Kommentare, Plot-Beschriftungen:** Englisch.
- **Formeln** immer als LaTeX (`$...$` bzw. `$$...$$`), nie als Code-String wie `log(OR)/SE`.
- Keine erfundenen Zahlen, Studien oder Zitate. Wenn eine Angabe unklar ist: als offen markieren und das Team fragen.

---

## Ordnerstruktur

```
01_data/
  Zschirnt_Ruedin_2016.pdf        Original-Paper (Preprint, EconStor; gitignored wie alle PDFs)
  raw_files/                      Dataverse-Download, NIE verändern:
                                    meta-clean.csv (Daten), meta-replication.Rmd/.pdf (R-Code + Output),
                                    meta-supplement.pdf (S1–S13), worldbank*.csv
  update_papers/                  PDFs der neuen Studien fürs Update
  zr2016_studies.csv              34 Studien mit Callback-Zählungen (Output 01)
  zr2016_subgroups.csv            215 Subgruppen mit Zählungen (Output 01)
  zr2016_studies_no_counts.csv    9 Studien ohne Zählungen (nicht in der OR-Analyse)
  update_studies.csv              neue Studien – von Hand erfasst, mit Quellen
  combined_studies.csv            Original + neue Studien (Output 03, nur wenn Update vorhanden)
02_code/
  utils_meta.py                   alle Meta-Funktionen (FE, RE, UWLS, Power, WAAP, ESS, FAT-PET, Plots, LaTeX)
  01_prepare_data.py              Schritt 1
  02_replication.py               Schritt 2
  03_update.py                    Schritte 3–4 (+ Tabelle der Evidenz)
  04_power_bias.py                Schritte 5–6
  05_meta_regression.py           Schritt 7
  run_all.py                      alles in der richtigen Reihenfolge
03_tmp/                           Zwischenstände, Experimente (gitignored)
04_report/
  figures/                        Plots als PDF (Overleaf) und PNG (Folien)
  tables/                         Tabellen als .tex (Overleaf) und .csv, LaTeX-Makros macros_*.tex
  slides/                         Präsentation
  group4.pdf                      finaler Bericht
venv/                             Python-Umgebung (gitignored)
PLAN.md                           Arbeitsplan (Deutsch, für das Team)
CLAUDE.md                         diese Datei
```

### Code ausführen

```bash
source venv/bin/activate          # einmalig vorher: pip install -r requirements.txt
python 02_code/run_all.py         # alle Schritte; oder einzeln: python 02_code/02_replication.py
```

---

## Die Original-Studie

- **Zitat:** Zschirnt, E. & Ruedin, D. (2016). Ethnic discrimination in hiring decisions: A meta-analysis of correspondence tests 1990–2015. *Journal of Ethnic and Migration Studies*, 42(7). DOI 10.1080/1369183X.2015.1133279
- **Replikationsdaten:** Harvard Dataverse, doi:10.7910/DVN/ZU8H79 → liegen in `01_data/raw_files/`.
  `meta-clean.csv`: 43 Studien (`global == "global"`) und 738 Subgruppen; davon haben 34 Studien und 215 Subgruppen die vier Callback-Zählungen für die OR.
- **Supplementary Material** (`meta-supplement.pdf`): S1 Studienliste, S2/S3 Codierung, S6–S10 Odds Ratios, S11 Wirtschaftslage, S12 Publication bias (Trim & Fill), S13 multivariate Meta-Regression.
- **Methode im Original:** `metafor::rma(measure = "OR", method = "REML")` auf Studienebene (siehe `meta-replication.Rmd`).
- **Figure 1 im Paper** zeigt nur 33 Zeilen (Weichselbaumer 2015 Österreich ist dort als «Hofer et al. 2013» beschriftet, Weichselbaumer 2015 Deutschland fehlt). Das Modell und die 0.60 beruhen aber auf **k = 34** – so auch Askarov et al. (30 + 4 Ausreisser = 34).
- Kleiner Fehler im Supplement S6: Die Tabelle «Odds Ratio 0.509 / 0.604» zeigt in Wahrheit $-\ln OR$; die OR sind 0.60 bzw. 0.55 (Text sagt 0.54).

### Zielwerte (aus `meta-replication.pdf`) – werden vom Code exakt getroffen

| Modell | Original | Prüfung in |
|---|---|---|
| RE (REML), Studien, k = 34 | $\ln OR = -0.5086$ (SE 0.0701), $\hat\tau^2 = 0.1406$, $I^2 = 92.73\%$, $Q = 327.68$ → OR 0.60 [0.52; 0.69] | `02_replication.py` |
| RE ohne Bendick, k = 33 | $-0.5404$ (0.0549), $\hat\tau^2 = 0.0764$ | `02_replication.py` |
| RE, Subgruppen, k = 215 | $-0.6041$ (0.0283), $\hat\tau^2 = 0.0934$ | `02_replication.py` |
| Meta-Regression RG1 (skills, REML + Knapp-Hartung), k = 30 | Konstante $-0.6080$ (0.1571), high 0.1578 (0.2241), low 0.0665 (0.1990), $\hat\tau^2 = 0.1696$ | `05_meta_regression.py` |
| Askarov et al. (2024), Table S2 | 30 Schätzungen (+4 Ausreisser), 87 % signifikant, Ø Power 0.909 | – |

### Weitere Resultate (Stand 3.11.2026, nur Originalstudien, k = 34)

| Grösse | Wert |
|---|---|
| FE = UWLS | OR 0.63; KI FE [0.61; 0.65], UWLS [0.56; 0.71] (SE-Verhältnis 3.15 = $\sqrt{Q/(k-1)}$) |
| RE (DL / PM) | 0.61 / 0.60 |
| 95%-Prediction-Interval (RE) | [0.28; 1.27] |
| Median-Power (bei UWLS) | 0.97; 24 von 34 Studien mit Power ≥ 80 % |
| WAAP | 0.64 [0.55; 0.73] |
| FAT-PET | $\hat\beta_1 = -1.05$ (SE 1.29); PET-OR 0.69 [0.53; 0.91] |
| ESS | 27 von 34 signifikant (0.79), erwartet 0.83 → ESS −0.03 |

---

## Effektgrösse und Vorzeichen

- Effekt pro Studie: $y_i = \ln(OR_i)$, OR = Callback-Odds **Minderheit / Mehrheit**. **Negativ = Diskriminierung.**
- Achtung: Die *relative Call-back-Ratio* im Paper ist umgekehrt definiert (Mehrheit/Minderheit, > 1 = Diskriminierung). Nicht mischen.
- Aus Rohzahlen ($a, b$ = Callback ja/nein Minderheit; $c, d$ = Mehrheit):
  $OR_i = \dfrac{a_i/b_i}{c_i/d_i}$, $\quad SE_i = \sqrt{1/a_i + 1/b_i + 1/c_i + 1/d_i}$. Bei Nullzellen: 0.5 zu allen Zellen addieren und dokumentieren.
- Aus 95%-KI: $SE_i = \dfrac{\ln UL_i - \ln LL_i}{2 \cdot 1.96}$.
- Analyse auf Log-Skala, Darstellung im Bericht als OR ($e^{y}$).
- Einschränkung für den Bericht: Bei log OR korrelieren Effekt und SE mechanisch etwas → Funnel-Asymmetrie nicht automatisch Publication bias.
- Analyseeinheit: **eine Schätzung pro Studie** (wie Figure 1). Neue Studien ebenfalls auf Studienebene (alle Minderheiten gepoolt vs. Mehrheit).

## Methoden (Vorgaben des Prof) und Umsetzung in Python

Pakete: nur `numpy`, `pandas`, `scipy`, `matplotlib` (kein statsmodels nötig). Alles ist in `02_code/utils_meta.py` selbst programmiert und gegen metafor (Original-Output) bzw. statsmodels geprüft.

- **FE** (`fixed_effect`): $\hat\mu = \sum w_i y_i / \sum w_i$, $w_i = 1/SE_i^2$, $SE(\hat\mu) = \sqrt{1/\sum w_i}$.
- **RE** (`random_effects`): $w_i^* = 1/(SE_i^2 + \hat\tau^2)$. Hauptspezifikation **REML** wie das Original; Robustheit DL, PM und Knapp-Hartung. $I^2$ wie metafor ($\hat\tau^2$ / ($\hat\tau^2$ + typische Varianz)). KI mit $z$, wie metafor.
- **UWLS** (`uwls`): OLS von $y_i/SE_i$ auf $1/SE_i$ ohne Konstante. Punkt = FE, SE = FE-SE × $\sqrt{Q/(k-1)}$; KI mit $t_{k-1}$.
- **Power:** $q_i = \Phi\!\left(|\hat\mu|/SE_i - 1.96\right)$ mit $\hat\mu$ = UWLS. Median berichten. Adequately powered: $SE_i \le |\hat\mu|/2.8$.
- **WAAP:** UWLS nur über adequately powered Schätzungen (Fallback UWLS, falls < 2 Studien).
- **FAT-PET:** WLS $y_i = \beta_0 + \beta_1 SE_i + \varepsilon_i$, Gewichte $1/SE_i^2$. $\beta_1$ = Bias (FAT), $\beta_0$ = korrigierter Effekt (PET).
- **ESS** (`ess`): beobachteter Anteil signifikanter Schätzungen vs. erwarteter Anteil (Power bei UWLS, beide Seiten). Zusätzlich eine Variante, in der die wahren Effekte mit $\hat\tau^2$ streuen.
- **PEESE** als Zusatz: wie FAT-PET mit $SE_i^2$.
- **Meta-Regression mit Moderatoren** (`05_meta_regression.py`): WLS (Hauptmodell, wie vom Prof verlangt) und RE-Meta-Regression REML + Knapp-Hartung (wie Original S13). Moderatoren: `europe`, `german_speaking`, `skill_high`/`skill_low` (Referenz mixed), `decade` = (Testjahr − 2000)/10, `new` (nur nach Update). Bei ca. 35 Studien sparsam bleiben.
- **Plots** (`forest_plot`, `funnel_plot`, `power_plot`): OR auf Log-Skala; Funnel mit SE (invertiert) und mit Präzision $1/SE$; neue Studien rot. Export als PDF + PNG.
- **Ausreisser:** Bendick et al. (1991), OR = 2.45 (Latino-CVs mit besseren Qualifikationen) → Hauptmodell wie Original mit, Robustheit ohne.

---

## Daten-Regeln

- `01_data/raw_files/` wird nie verändert. Alles Weitere entsteht per Skript.
- Jede Zahl muss rückverfolgbar sein (Spalte `source`: «Dataverse meta-clean.csv» oder «Autor Jahr, Tabelle X, S. Y»).
- **`update_studies.csv`** (eine Zeile pro neue Studie, alle Minderheiten gepoolt):
  `study_id, authors, year, title, journal, country, testing_year, minority, gender, skills, n_minority, cb_minority, n_majority, cb_majority, or, ci_low, ci_high, source, notes`
  Entweder die vier Zählungen (`n_*` = Bewerbungen, `cb_*` = Callbacks) **oder** `or, ci_low, ci_high`. `skills` ∈ {high, low, mixed}. Fehlende Werte leer lassen, nicht raten.
  Länder ausserhalb der Listen in `utils_meta.py` werden als «Other» codiert (Warnung im Output).

## Code-Regeln

- Skripte nummeriert, laufen vom Repo-Root aus (`python 02_code/02_replication.py`), nur relative Pfade.
- Gemeinsame Funktionen in `02_code/utils_meta.py`, nicht kopieren.
- Tabellen als `.tex` (eigener booktabs-Writer `to_latex_table`, kein jinja2 nötig) + `.csv`; Zahlen für den Fliesstext als LaTeX-Makros (`write_macros`, Präfix `\ma…`, z. B. `\maORre`). Plots als PDF + PNG. Alles nach `04_report/`; Zwischenstände nach `03_tmp/`.
- Neue Pakete in `requirements.txt` eintragen. Python-Umgebung in `venv/`.
- Nach Änderungen an der Analyse: `python 02_code/run_all.py` – die Checks in 01, 02 und 05 müssen «OK» zeigen.

## Bericht und Präsentation

- Bericht in **Overleaf (LaTeX)**, Englisch. Ordner `04_report/figures/` und `04_report/tables/` nach Overleaf hochladen (als `figures/` und `tables/`). Finales PDF zusätzlich als `04_report/group4.pdf` ins Repo.
- Overleaf-Präambel: `\usepackage{booktabs,longtable,array,graphicx}` und z. B. `\usepackage[margin=2.5cm]{geometry}`; Makros mit `\input{tables/macros_replication.tex}` (analog `macros_update`, `macros_power_bias`). Tabellen mit `\input{tables/replication.tex}` usw.
- Gliederung und Folienplan: siehe `PLAN.md`, Schritte 8 und 9.
- Pflichtinhalte: Tabelle der Evidenz, Forest + Funnel Plot, Replikation, ≥ 2 neue Studien (im KI? Änderung der Schätzung?), Aussage zur visuellen Evidenz für Publication bias, WLS-Meta-Regression, Fazit zur Verlässlichkeit der Evidenz.

## Arbeitsweise

- Nicht ohne Rückfrage committen oder pushen. Remote: `git@github.com:KEDES1998/MetaAnalysis.git`, Branch `main`.
- Kleine Commits mit klarer Nachricht.
- Erledigte Punkte in `PLAN.md` abhaken, neue offene Fragen dort unter «Offene Fragen» eintragen.

## Seminarunterlagen (im claude.ai-Projekt, nicht im Repo)

- `MetaIntro.pdf` – Rahmen, Zeitplan, die 6 Aufgaben
- `instruction.pdf` – formale und inhaltliche Anforderungen an den Bericht
- `notes.pdf` – Folien des Prof (FE, RE, UWLS, Funnel, Publication bias, Power)
- `Askarov.studies.pdf` – Askarov et al. (2024), Online Supplement, Table S2 (Liste der Meta-Studien)

## Offene Punkte

- Auswahl und Erfassung der Update-Studien in `01_data/update_studies.csv` (Kandidaten in `PLAN.md`, Schritt 3); danach `run_all.py` neu laufen lassen.
- Bendick et al. (1991): Hauptmodell mit (wie Original), ohne als Robustheit – beides wird gerechnet; Entscheid für den Text offen.
