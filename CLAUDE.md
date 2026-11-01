# CLAUDE.md – Projektkontext

Seminararbeit im MA-Seminar «Meta-Analysis» (Prof. Rainer Winkelmann, UZH, HS 2026).
Wir **replizieren und erweitern** die Meta-Analyse von Zschirnt & Ruedin (2016) zu ethnischer Diskriminierung bei Bewerbungen.
Der Arbeitsplan mit allen Schritten und Fristen steht in **`PLAN.md`** – vor grösseren Arbeiten dort nachschauen und erledigte Punkte abhaken.

---

## Team, Fristen, Abgabe

- Team: Kevin de Silva und Vanessa Allenspach, Group 4
- **Bericht:** Fr 13.11.2026, bis Mitternacht, per E-Mail an rainer.winkelmann@econ.uzh.ch. Dateiname `group4.pdf`. Ca. 10, max. 15 Seiten ohne Anhang. Titelseite mit Titel und beiden Namen. Vollständige Liste aller untersuchten Studien im Literaturverzeichnis.
- **Präsentation:** Di 17.11.2026 (Gruppen 1–3) oder Di 24.11.2026 (Gruppen 4–6), 20 Min. + 10 Min. Diskussion, beide präsentieren. Folien (PDF/PPT) spätestens am Präsentationstag an den Prof mailen.
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
  Zschirnt_Ruedin_2016.pdf   Original-Paper (Preprint, EconStor)
  raw/                       Rohdaten (Dataverse-Download), NIE verändern
  update_papers/             PDFs der neuen Studien fürs Update
  zr2016_studies.csv         aufbereitete Original-Studien (Output von 01_prepare_data.py)
  update_studies.csv         neue Studien (von Hand erfasst, mit Quellen)
02_code/
  utils_meta.py              gemeinsame Funktionen (FE, RE, UWLS, Power, WAAP, ESS, Plots)
  01_prepare_data.py
  02_replication.py
  03_update.py
  04_power_bias.py
  05_meta_regression.py
03_tmp/                      Zwischenstände, Experimente – nicht für die Abgabe (gitignored)
04_report/
  figures/                   Plots als PDF (für Overleaf)
  tables/                    Tabellen als .tex (für Overleaf)
  slides/                    Präsentation
  groupX.pdf                 finaler Bericht
PLAN.md                      Arbeitsplan (Deutsch, für das Team)
CLAUDE.md                    diese Datei
```

---

## Die Original-Studie

- **Zitat:** Zschirnt, E. & Ruedin, D. (2016). Ethnic discrimination in hiring decisions: A meta-analysis of correspondence tests 1990–2015. *Journal of Ethnic and Migration Studies*, 42(7). DOI 10.1080/1369183X.2015.1133279
- **Replikationsdaten:** Harvard Dataverse, doi:10.7910/DVN/ZU8H79 (Download im Browser; aus der Sandbox nicht erreichbar).
- **Supplementary Material** (S1 Studienliste, S2/S3 Gruppen-Codierung, S6–S10 Odds Ratios, S11 Wirtschaftslage, S12 Publication bias, S13 multivariate Meta-Regression) – beim Journal, noch nicht im Repo.
- **Umfang:** Correspondence Tests in OECD-Ländern 1990–2015. Preprint: 42 Studien, 18 Länder, 730 Subgruppen. Die publizierte Version nennt 43 Studien / 738 Tests → kleine Abweichungen zum Preprint möglich, mit Dataverse abgleichen.
- **Methode im Original:** Random-Effects-Modell (R/metafor, «RE Model» → vermutlich REML) auf Studienebene.

### Zielwerte für die Replikation

| Grösse | Wert | Quelle |
|---|---|---|
| RE, Studienebene (N = 33) | OR = 0.60 [0.52; 0.69] | Figure 1 |
| RE, Subgruppenebene | OR = 0.54 | Text S. 8 / Suppl. S6 |
| Relative Call-back-Ratio (Mehrheit/Minderheit), Studien | Mittel 1.55, Median 1.44 | S. 9, Figure 2 |
| Relative Call-back-Ratio, Subgruppen | Mittel 1.75, Median 1.49 | S. 9 |
| Askarov et al. (2024), Table S2 | 30 Schätzungen (+4 Ausreisser entfernt), 87 % signifikant, Ø Power 0.909, $\hat\tau^2 = 0.0215$ | `Askarov.studies.pdf` |

### Kontrollwerte (Vorab-Check 29.10.2026, gerechnet aus den gerundeten Werten in Figure 1)

| Methode | OR | 95%-KI | Bemerkung |
|---|---|---|---|
| RE, REML | 0.600 | [0.521; 0.691] | $\hat\tau^2 = 0.145$ – trifft Original exakt |
| RE, Paule-Mandel | 0.599 | [0.519; 0.692] | $\hat\tau^2 = 0.152$ |
| RE, DerSimonian-Laird | 0.604 | [0.536; 0.681] | $\hat\tau^2 = 0.100$ |
| FE | 0.628 | [0.607; 0.651] | |
| UWLS | 0.628 | [0.562; 0.703] | gleicher Punkt wie FE, breiteres KI |

Weitere Vorab-Werte: 26 von 33 Studien signifikant (79 %); Median-Power bei $\hat\mu_{UWLS}$ ≈ 0.99.
Neuer Code muss diese Werte (bis auf Rundung) reproduzieren.

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

Pakete: `numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`.

- **FE:** $\hat\mu = \sum w_i y_i / \sum w_i$, $w_i = 1/SE_i^2$, $SE(\hat\mu) = \sqrt{1/\sum w_i}$.
- **RE:** $w_i^* = 1/(SE_i^2 + \hat\tau^2)$. Hauptspezifikation **REML** (eigene kleine Funktion mit `scipy.optimize`, da `statsmodels` kein REML hat). Robustheit: DL und PM über `statsmodels.stats.meta_analysis.combine_effects(eff, var, method_re="chi2" | "iterated")`. Heterogenität: $Q$, $I^2$. Optional Hartung-Knapp.
- **UWLS:** OLS von $y_i/SE_i$ auf $1/SE_i$ ohne Konstante. Punkt = FE, SE skaliert mit Residual-Standardfehler. (`combine_effects(...).summary_frame()` Zeile «fixed effect wls» entspricht UWLS – mit eigener Regression gegenprüfen.)
- **Power:** $q_i = \Phi\!\left(|\hat\mu|/SE_i - 1.96\right)$ mit $\hat\mu$ = UWLS. Median berichten. Adequately powered: $SE_i \le |\hat\mu|/2.8$.
- **WAAP:** UWLS nur über adequately powered Schätzungen (Fallback UWLS, falls < 2 Studien).
- **FAT-PET:** WLS $y_i = \beta_0 + \beta_1 SE_i + \varepsilon_i$, Gewichte $1/SE_i^2$. $\beta_1$ = Bias (FAT), $\beta_0$ = korrigierter Effekt (PET).
- **ESS:** beobachteter Anteil signifikanter Schätzungen vs. erwarteter Anteil $\frac{1}{n}\sum_i q_i$ (Power bei UWLS bzw. WAAP).
- **Meta-Regression mit Moderatoren:** FAT-PET + wenige Moderatoren (Region, Post-2000, deutschsprachig, Jahr). Bei ca. 35 Studien sparsam bleiben.
- **Plots:** Forest Plot (OR, Log-Skala, Linie bei 1) und Funnel Plot ($\ln OR$ vs. $1/SE$, Trichter um FE/UWLS) mit `matplotlib`, Export als PDF nach `04_report/figures/`.
- **Ausreisser:** Bendick et al. (1991), OR = 2.45 (Latino-CVs mit besseren Qualifikationen) → Hauptmodell wie Original mit, Robustheit ohne.

---

## Daten-Regeln

- `01_data/raw/` wird nie verändert. Alles Weitere entsteht per Skript.
- Jede Zahl muss rückverfolgbar sein (Spalte `source`: «dataverse», «figure1» oder «Autor Jahr, Tabelle X, S. Y»).
- CSV-Schema (für Original und Update gleich):
  `study_id, authors, year, title, country, region, n_minority, cb_minority, n_majority, cb_majority, or, ci_low, ci_high, log_or, se, german_speaking, post2000, in_original, source, notes`
  Fehlende Werte leer lassen, nicht raten.

## Code-Regeln

- Skripte nummeriert, laufen vom Repo-Root aus (`python 02_code/02_replication.py`), nur relative Pfade.
- Gemeinsame Funktionen in `02_code/utils_meta.py`, nicht kopieren.
- Ergebnisse (Tabellen als `.tex` via `pandas.to_latex`, Plots als PDF) nach `04_report/`; Zwischenstände nach `03_tmp/`.
- Neue Pakete in `requirements.txt` eintragen. Python-Umgebung in `.venv/`.
- Nach Änderungen an der Analyse: Kontrollwerte oben prüfen.

## Bericht und Präsentation

- Bericht in **Overleaf (LaTeX)**, Englisch. Figures/Tabellen werden aus `04_report/` in Overleaf hochgeladen. Finales PDF zusätzlich als `04_report/groupX.pdf` ins Repo.
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

- Gruppennummer und Name der Mitstudentin eintragen; Präsentationstermin (17.11. oder 24.11.).
- Format und Inhalt der Dataverse-Daten (Moderatoren vorhanden?).
- Auswahl der Update-Studien (Kandidaten in `PLAN.md`, Schritt 3).
- Abweichung Askarov (34 Schätzungen) vs. Figure 1 (33 Studien) klären.
