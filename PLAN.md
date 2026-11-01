# PLAN – Meta-Analyse «Ethnic Discrimination in Hiring»

Dieser Plan zeigt Schritt für Schritt, was wir bis zur Abgabe machen.
Wenn etwas erledigt ist: Haken setzen (`[ ]` → `[x]`) und committen.

---

## 1. Auf einen Blick

| | |
|---|---|
| **Team** | Kevin und Vanessa – Gruppe 4 |
| **Original-Studie** | Zschirnt & Ruedin (2016): *Ethnic discrimination in hiring decisions: A meta-analysis of correspondence tests 1990–2015*. Journal of Ethnic and Migration Studies 42(7) |
| **Unsere Aufgabe** | Die Meta-Analyse **nachrechnen** (Replikation) und mit neueren Studien **ergänzen** (Update) |
| **Abgabe Bericht** | **Freitag, 13.11.2026, bis Mitternacht** – als `group4.pdf` per E-Mail an rainer.winkelmann@econ.uzh.ch |
| **Präsentation** | Di 17.11.2026 (Gruppen 1–3) oder Di 24.11.2026 (Gruppen 4–6), Raum KOL-H-309. **Wir (Gruppe 4) präsentieren am Di 24.11.** |
| **Umfang** | Bericht ca. 10 Seiten, höchstens 15 (ohne Anhang). Präsentation 20 Min. + 10 Min. Diskussion. Beide müssen reden. |
| **Werkzeuge** | Python (Rechnen), Overleaf/LaTeX (Bericht), GitHub (Code und Daten) |
| **Sprache** | Bericht und Folien auf Englisch |
| **Note** | Bericht 50 %, Präsentation 40 %, Mitarbeit 10 % |

---

## 2. Worum geht es? (kurz erklärt)

**Die Frage:**
Werden Bewerbende mit einem ausländisch klingenden Namen seltener zum Vorstellungsgespräch eingeladen als gleich gute Bewerbende aus der Mehrheitsbevölkerung?

**Wie misst man das?**
Mit sogenannten *Correspondence Tests*. Forschende schicken erfundene, gleich gute Bewerbungen an echte Stellenausschreibungen. Der einzige Unterschied ist der Name (zum Beispiel ein «schweizerischer» und ein «türkischer» Name). Dann zählen sie, wer eine positive Antwort bekommt. Diese Antwort heisst *Callback*.

- **X (Treatment):** Die Bewerbung trägt einen Minderheiten-Namen statt eines Mehrheits-Namens.
- **Y (Outcome):** Callback ja oder nein (Einladung zum Gespräch oder positive Antwort).

**Die Effektgrösse:**
Wir nehmen – wie das Paper – die **Odds Ratio (OR)**. Sie vergleicht die Chance auf einen Callback der Minderheit mit der Chance der Mehrheit.

- OR = 1 → keine Diskriminierung
- OR < 1 → die Minderheit wird seltener eingeladen (Diskriminierung)

Gerechnet wird immer mit dem Logarithmus: $y_i = \ln(OR_i)$.
Dann gilt: **negativer Wert = Diskriminierung**. Am Schluss rechnen wir mit $e^{y}$ wieder in eine OR zurück.

**Das Ergebnis im Original:**
Random-Effects-Modell mit 33 Studien: **OR = 0.60 [0.52; 0.69]** (Figure 1 im Paper).
Das heisst: Minderheiten haben rund 40 % tiefere Odds auf einen Callback. Anders gesagt: Sie müssen etwa 50 % mehr Bewerbungen schreiben, um gleich oft eingeladen zu werden.

**Gute Nachricht:**
Ein erster Test (29.10.) zeigt: Mit den Zahlen aus Figure 1 kommt man genau auf 0.60 [0.52; 0.69]. Die Replikation ist also machbar.

---

## 3. Was der Prof verlangt (Checkliste)

Aus `MetaIntro.pdf` (Folien 10–11) und `instruction.pdf`:

- [ ] **Aufgabe 1:** Frage und Umfang der Meta-Analyse erklären. Was ist X, was ist das Outcome? Typische Methode, typische Schätzgleichung, typischer Datensatz.
- [ ] **Aufgabe 2:** Die Original-Schätzung replizieren. Durchschnitt mit FE, RE und UWLS rechnen. Zeigen: FE und UWLS geben denselben Schätzwert, aber unterschiedliche Konfidenzintervalle. Welches ist breiter?
- [ ] **Aufgabe 3:** Update. Mindestens 2 neuere Studien finden, Effekt und Standardfehler herausschreiben. Liegen die neuen Werte im Konfidenzintervall? Ändert sich die Meta-Schätzung stark?
- [ ] **Aufgabe 4:** Median-Power berechnen. Warum ist tiefe Power ein Problem? Warum haben Studien mit tiefer Power eher Publication bias? Warum ist unser Wert eher eine Obergrenze?
- [ ] **Aufgabe 5:** Publication bias prüfen mit: Funnel Plot, WAAP, ESS, Meta-Regression von Effekt auf SE. (Testen ist nicht nötig.)
- [ ] **Aufgabe 6:** Fazit. Gibt es verlässliche Evidenz zur wahren Effektgrösse? Warum oder warum nicht?

Das muss ausserdem im Bericht sein:

- [ ] Tabelle der Evidenz: Titel, Autoren, Jahr, Effektgrösse, Standardfehler, Moderatoren
- [ ] Forest Plot und Funnel Plot
- [ ] WLS-Meta-Regression (Publication bias und, wenn möglich, Moderatoren)
- [ ] Titelseite mit Titel und beiden Namen
- [ ] Vollständige Liste aller untersuchten Studien im Literaturverzeichnis
- [ ] Optional: Schätzung nur mit Studien mit genügend Power (= WAAP)

---

## 4. Zeitplan

Heute ist Do, 29.10. Wir haben gut zwei Wochen.

| Wann | Schritt | Wer |
|---|---|---|
| Do 29.10. – Fr 30.10. | 0 – Setup und Paper lesen | beide |
| Sa 31.10. – Mo 2.11. | 1 – Daten der Original-Studie aufbereiten | Kev |
| Sa 31.10. – Do 5.11. | 3 – Neue Studien suchen und erfassen | Vanessa |
| Di 3.11. – Mi 4.11. | 2 – Replikation (FE, RE, UWLS, Plots) | Kev |
| Do 5.11. | 4 – Update rechnen | Kev |
| Fr 6.11. – Sa 7.11. | 5 – Power, 6 – Publication bias, 7 – Meta-Regression | beide |
| ab Mo 2.11. | 8 – Bericht: Einleitung und Theorie schreiben | Vanessa |
| So 8.11. – Mi 11.11. | 8 – Bericht: Resultate und Fazit schreiben | beide |
| Do 12.11. | Puffer: gegenseitig lesen und korrigieren | beide |
| **Fr 13.11.** | **Abgabe per E-Mail** | Kev schickt, Vanessa in CC |
| Sa 14.11. – Mo 23.11. | 9 – Präsentation machen und üben | beide |
| **Di 24.11.** | **Präsentation** | beide |

Die Aufteilung ist ein Vorschlag (siehe Abschnitt 6).

---

## 5. Die Schritte im Detail

### Schritt 0 – Setup und Paper lesen

**Ziel:** Wir verstehen das Paper, und das Repo funktioniert bei beiden.

So geht's:

- [ ] Beide lesen das Paper `01_data/Zschirnt_Ruedin_2016.pdf`. Am wichtigsten sind die Seiten 6–10 (Methode, Daten, Figure 1 und 2).
- [ ] Beide klonen das Repo von GitHub.
- [ ] `requirements.txt` füllen mit: `numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`.
- [ ] Python-Umgebung anlegen:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- [ ] `.gitignore` füllen mit: `.DS_Store`, `.venv/`, `__pycache__/`, `03_tmp/*` (aber `!03_tmp/.gitkeep`).
- [ ] Overleaf-Projekt anlegen und die andere Person einladen.
- [x] Gruppennummer klären: Gruppe 4 → `group4.pdf`, Präsentation Di 24.11.

**Fertig, wenn:** Beide können Python im Repo starten, und beide haben Zugriff auf Overleaf.

---

### Schritt 1 – Daten der Original-Studie aufbereiten

**Ziel:** Eine saubere CSV-Datei mit allen 33 Studien. Für jede Studie: Effekt ($\ln OR$) und Standardfehler (SE).

Es gibt zwei Quellen:

- **Quelle A (besser): Die Replikationsdaten der Autoren** auf Harvard Dataverse: <https://doi.org/10.7910/DVN/ZU8H79>.
  Im Browser herunterladen und **unverändert** in `01_data/raw/` ablegen.
- **Quelle B (Notlösung): Figure 1 im Paper abtippen.** Dort stehen für jede Studie die OR und das 95%-Konfidenzintervall.

Wie man den Standardfehler bekommt:

Wenn wir die Rohzahlen haben ($a$ = Callbacks Minderheit, $b$ = keine Callbacks Minderheit, $c$ und $d$ gleich für die Mehrheit):

$$
OR_i = \frac{a_i / b_i}{c_i / d_i}, \qquad SE_i = \sqrt{\frac{1}{a_i} + \frac{1}{b_i} + \frac{1}{c_i} + \frac{1}{d_i}}
$$

Wenn wir nur das Konfidenzintervall haben (untere Grenze $LL$, obere Grenze $UL$):

$$
SE_i = \frac{\ln(UL_i) - \ln(LL_i)}{2 \cdot 1.96}
$$

So geht's:

- [ ] Dataverse-Dateien anschauen: Welches Format? Welche Spalten? Was bedeuten sie?
- [ ] Skript `02_code/01_prepare_data.py` schreiben. Es liest die Rohdaten, rechnet `log_or` und `se` und speichert `01_data/zr2016_studies.csv`.
- [ ] Kontrolle: Stimmen unsere OR-Werte mit Figure 1 überein (auf 2 Nachkommastellen)?
- [ ] Moderatoren mitnehmen, falls vorhanden: Land, Region, Jahr, Geschlecht, Generation, Skill-Level, deutschsprachig ja/nein.

**Ergebnis:** `01_data/zr2016_studies.csv`

**Fertig, wenn:** 33 Zeilen, jede mit `log_or` und `se`, und die Werte passen zu Figure 1.

---

### Schritt 2 – Replikation

**Ziel:** Die 0.60 [0.52; 0.69] selber herausbekommen und die drei Methoden vergleichen.

Die drei Methoden in einfachen Worten:

- **FE (Fixed Effect):** Ein gewichteter Durchschnitt. Grosse, genaue Studien zählen mehr. Gewicht $w_i = 1/SE_i^2$.
  Annahme: Alle Studien messen denselben wahren Effekt. Unterschiede sind nur Zufall.
- **RE (Random Effects):** Erlaubt, dass der wahre Effekt von Studie zu Studie schwankt. Diese Schwankung heisst $\tau^2$.
  Gewicht $w_i^* = 1/(SE_i^2 + \tau^2)$. Dadurch bekommen kleine Studien relativ mehr Gewicht als bei FE.
- **UWLS (Unrestricted Weighted Least Squares):** Eine Regression von $y_i/SE_i$ auf $1/SE_i$, ohne Konstante.
  Ergibt **denselben Schätzwert wie FE**, aber ein anderes Konfidenzintervall.

So geht's:

- [ ] Skript `02_code/02_replication.py` schreiben.
- [ ] FE, RE und UWLS rechnen. Für RE die Methode **REML** nehmen (so hat es das Original gemacht, mit dem R-Paket metafor). Zum Vergleich auch DerSimonian-Laird.
- [ ] Ergebnisse in OR zurückrechnen: $OR = e^{y}$.
- [ ] Tabelle machen: Methode | OR | 95%-KI | $\tau^2$ | $I^2$.
- [ ] Forest Plot zeichnen und als PDF speichern.
- [ ] Diskussionspunkt notieren: Bendick et al. (1991) ist ein Ausreisser (OR = 2.45; dort hatten die Latino-Bewerbungen bessere Qualifikationen). Wir rechnen einmal **mit** und einmal **ohne** diese Studie.

**Ergebnis:** `04_report/tables/replication.tex` und `04_report/figures/forest.pdf`

**Fertig, wenn:**
- RE ergibt ca. 0.60 [0.52; 0.69].
- FE und UWLS haben denselben Schätzwert.
- Wir können erklären, welches Konfidenzintervall breiter ist und warum. (Tipp: Es hat mit der Heterogenität zwischen den Studien zu tun.)

---

### Schritt 3 – Neue Studien suchen und erfassen (Update)

**Ziel:** Mindestens 2 neuere Studien, die **nicht** im Original sind. Besser 3 bis 5.

Die Studien müssen ähnlich sein wie im Original, sonst kann man sie nicht vergleichen:

- Correspondence Test (schriftliche Bewerbungen, kein persönliches Vorsprechen)
- Ethnische Minderheit gegen Mehrheit
- In einem OECD-Land
- Nach 2015 veröffentlicht
- **Wichtigste Bedingung:** Die Studie nennt pro Gruppe die **Anzahl Bewerbungen und die Anzahl Callbacks** (oder Callback-Quote und Anzahl). Sonst können wir keine OR und keinen SE rechnen.

Wo wir suchen:

- **Lippens, Vermeiren & Baert (2023):** grosse Meta-Analyse über fast alle Correspondence-Experimente von 2005 bis 2020, mit einer Liste aller Studien (Table R1). Arbeitspapier-Version: <https://docs.iza.org/dp14966.pdf>
- **Google Scholar:** «correspondence test» ethnic discrimination hiring, ab 2016
- **Kandidaten** (noch prüfen, ob die nötigen Zahlen drinstehen):
  - Koopmans, Veit & Yemane (2019), *Ethnic and Racial Studies* 42(16) – Deutschland, fast 6'000 Stellen
  - Lancee (2021), *Journal of Ethnic and Migration Studies* – GEMM-Experiment in fünf Ländern
  - Niederlande-Studie im *Journal of International Migration and Integration* (2021), 4'211 Bewerbungen: <https://doi.org/10.1007/s12134-020-00795-w>
  - Zschirnt & Fibbi (2019) – Schweiz, Working Paper

So geht's:

- [ ] Für jede Kandidaten-Studie das PDF holen und die Tabelle mit den Callbacks suchen.
- [ ] Zahlen in `01_data/update_studies.csv` eintragen (gleiche Spalten wie in Schritt 1).
- [ ] Bei jeder Zahl die Quelle notieren (Seite, Tabelle).
- [ ] Pro Studie **eine Zeile**: alle Minderheiten zusammen gegen die Mehrheit. So ist es wie im Original auf Studienebene.
- [ ] PDFs der neuen Studien in `01_data/update_papers/` ablegen.

**Fertig, wenn:** Mindestens 2 Studien mit `log_or` und `se`, und jede Zahl hat eine Quellenangabe.

---

### Schritt 4 – Update rechnen

**Ziel:** Prüfen, ob die neuen Studien zum alten Ergebnis passen.

So geht's:

- [ ] Skript `02_code/03_update.py` schreiben.
- [ ] **Frage A:** Liegen die neuen Effekte im Konfidenzintervall des Originals, also zwischen 0.52 und 0.69?
- [ ] **Frage B:** Neue Meta-Schätzung mit allen Studien zusammen (alt + neu). Ändert sie sich stark?
- [ ] Für die Diskussion: Auch das *Prediction Interval* anschauen. Es zeigt, wo eine **einzelne neue** Studie liegen sollte. Das ist bei starker Heterogenität fairer als das Konfidenzintervall des Durchschnitts.

**Ergebnis:** `04_report/tables/update.tex` und ein Forest Plot, in dem die neuen Studien markiert sind.

---

### Schritt 5 – Power

**Die Idee:**
Power ist die Wahrscheinlichkeit, dass eine Studie einen echten Effekt auch als signifikant erkennt.
Wir tun so, als wäre die Meta-Schätzung $\hat\mu$ (aus UWLS) der wahre Effekt. Dann ist die Power von Studie $i$:

$$
q_i = \Phi\left(\frac{|\hat\mu|}{SE_i} - 1.96\right)
$$

Eine Studie hat «genügend Power» (mindestens 80 %), wenn gilt: $SE_i \le |\hat\mu| / 2.8$.

So geht's:

- [ ] Skript `02_code/04_power_bias.py` anfangen.
- [ ] Power pro Studie rechnen, dann den **Median**.
- [ ] Vergleich mit Askarov et al. (2024): Dort hat dieses Gebiet eine durchschnittliche Power von 0.91. In der Ökonomie insgesamt liegt der Median nur bei ca. 7 %.
- [ ] Diskutieren: Warum ist tiefe Power ein Problem? Warum ist unser Wert eher eine Obergrenze?
  (Tipp: Wenn Publication bias den Meta-Effekt grösser macht, wird auch die berechnete Power zu gross.)

**Erwartung:** Die Power ist hier eher hoch, weil Correspondence Tests oft Tausende Bewerbungen verschicken.

---

### Schritt 6 – Publication bias

**Die Idee:** Wurden vor allem «schöne», signifikante Ergebnisse veröffentlicht? Wir schauen mit vier Methoden hin. Testen ist laut Prof nicht nötig.

1. **Funnel Plot:** x-Achse = $\ln(OR)$, y-Achse = Präzision $1/SE$.
   Ohne Bias sieht er aus wie ein symmetrischer Trichter. Ist er schief?
2. **Meta-Regression von Effekt auf SE (FAT-PET):**

   $$
   y_i = \beta_0 + \beta_1 \, SE_i + \varepsilon_i \qquad \text{(WLS mit Gewicht } 1/SE_i^2\text{)}
   $$

   $\beta_1$ misst den Bias. $\beta_0$ ist der «korrigierte» Effekt für eine unendlich grosse Studie ($SE \to 0$).
3. **WAAP:** UWLS nur mit den Studien, die genügend Power haben (aus Schritt 5).
4. **ESS (Excess Statistical Significance):** Wie viele Studien sind signifikant? Und wie viele würden wir aufgrund der Power *erwarten* ($\sum_i q_i$)? Sind es viel mehr als erwartet, ist das ein Hinweis auf Selektion.

So geht's:

- [ ] Alle vier Methoden in `02_code/04_power_bias.py` rechnen.
- [ ] Funnel Plot als PDF speichern.
- [ ] Eine Tabelle mit allen Schätzungen: FE, RE, UWLS, PET, WAAP.

**Achtung für den Bericht:** Bei der log OR hängt der SE rechnerisch ein bisschen mit der Grösse des Effekts zusammen. Etwas Schiefe im Funnel Plot kann deshalb auch ohne Publication bias entstehen. Das schreiben wir als Einschränkung dazu.

**Ergebnis:** `04_report/tables/pubbias.tex` und `04_report/figures/funnel.pdf`

---

### Schritt 7 – Meta-Regression mit Moderatoren (wenn Daten vorhanden)

**Ziel:** Erklären, *warum* die Studien unterschiedliche Effekte finden (Heterogenität).

Wir erweitern die Regression aus Schritt 6 um Moderatoren, zum Beispiel:

$$
y_i = \beta_0 + \beta_1 \, SE_i + \beta_2 \, \text{Europe}_i + \beta_3 \, \text{Post2000}_i + \beta_4 \, \text{GermanSpeaking}_i + \varepsilon_i
$$

Ideen aus dem Paper: Region (Europa vs. Nordamerika), vor/nach den EU-Richtlinien (2000), deutschsprachige Länder, Jahr.

- [ ] Skript `02_code/05_meta_regression.py` schreiben.
- [ ] Nur wenige Moderatoren nehmen. Wir haben nur ca. 35 Studien, also vorsichtig interpretieren.

---

### Schritt 8 – Bericht schreiben (Overleaf, Englisch)

Gliederung mit ungefährer Seitenzahl:

| Kapitel | Inhalt | Seiten |
|---|---|---|
| Title page | Titel, beide Namen, Gruppe | – |
| 1 Introduction | Worum geht es, warum ist es wichtig | 1 |
| 2 Research question and literature | X, Outcome, Correspondence-Test-Design, typische Schätzgleichung, typischer Datensatz (Aufgabe 1) | 1.5 |
| 3 The original meta-analysis and data | Zschirnt & Ruedin (2016), Daten, Effektgrösse | 1.5 |
| 4 Replication | FE, RE, UWLS, Forest Plot (Aufgabe 2) | 2 |
| 5 Update | Neue Studien, im KI? Neue Schätzung (Aufgabe 3) | 1.5 |
| 6 Statistical power | Median-Power (Aufgabe 4) | 1 |
| 7 Publication bias | Funnel, FAT-PET, WAAP, ESS (Aufgabe 5) | 2 |
| 8 Heterogeneity | Meta-Regression mit Moderatoren | 1 |
| 9 Conclusion | Gibt es verlässliche Evidenz? (Aufgabe 6) | 1 |
| References | **Alle** untersuchten Studien | – |
| Appendix | Tabelle der Evidenz | – |

Für Kapitel 2 – typische Schätzgleichung in Correspondence Tests (lineares Wahrscheinlichkeitsmodell):

$$
\text{Callback}_{ij} = \alpha + \beta \, \text{Minority}_{i} + \gamma' X_{ij} + \varepsilon_{ij}
$$

Typischer Datensatz: zum Beispiel Bertrand & Mullainathan (2004), rund 5'000 erfundene Lebensläufe auf Stelleninserate in Boston und Chicago.

So geht's:

- [ ] Gliederung in Overleaf anlegen.
- [ ] Grafiken aus `04_report/figures/` und Tabellen aus `04_report/tables/` in Overleaf hochladen.
- [ ] Jede Zahl im Text muss aus unserem Code kommen (nicht von Hand abschreiben, wenn es sich vermeiden lässt).
- [ ] Länge prüfen: 10–15 Seiten ohne Anhang.
- [ ] Gegenseitig korrigieren (Do 12.11.).
- [ ] PDF als `group4.pdf` speichern, auch in `04_report/` ablegen.
- [ ] **Fr 13.11. vor Mitternacht** an rainer.winkelmann@econ.uzh.ch schicken.

---

### Schritt 9 – Präsentation

- 20 Minuten sind ungefähr 10–12 Folien. Beide reden, zum Beispiel je die Hälfte.
- Folien auf Englisch.

Vorschlag für die Folien:

1. Title
2. Research question and correspondence tests
3. The original meta-analysis (Zschirnt & Ruedin 2016)
4. Data and effect size
5. Replication: FE, RE, UWLS
6. Forest plot
7. Update: new studies
8. Statistical power
9. Publication bias: funnel plot and FAT-PET
10. WAAP and ESS
11. Conclusion: reliable evidence?
12. Backup: meta-regression

So geht's:

- [ ] Folien machen (ab Sa 14.11., fertig bis ca. Do 19.11.).
- [ ] Einmal laut proben, mit Stoppuhr (spätestens Mo 23.11.).
- [ ] Mögliche Fragen für die 10 Minuten Diskussion überlegen.
- [ ] Folien als PDF **spätestens am Präsentationstag** an den Prof mailen (oder USB-Stick mitnehmen).

---

## 6. Aufgabenteilung (Vorschlag – bitte anpassen)

| Kev | Vanessa | Beide zusammen |
|---|---|---|
| Setup (Repo, Python) | Overleaf-Projekt anlegen | Paper lesen |
| Schritt 1: Daten aufbereiten | Schritt 3: neue Studien suchen und erfassen | Schritte 5–7 interpretieren |
| Schritt 2: Replikation | Bericht Kapitel 1–3 | Bericht Kapitel 4–9 |
| Schritt 4: Update rechnen | Tabelle der Evidenz und Literaturverzeichnis | Fazit (Aufgabe 6) |
| Code für Power und Bias | | Präsentation und Probe |

---

## 7. Offene Fragen

- [x] Welche Gruppennummer haben wir? → Gruppe 4, Präsentation am Di 24.11.2026.
- [ ] In welchem Format sind die Dataverse-Daten? Sind dort auch die Moderatoren drin?
- [ ] Bendick et al. (1991): im Hauptmodell lassen oder als Ausreisser behandeln?
- [ ] Welche neuen Studien nehmen wir? (Entscheid bis Do 5.11.)

---

## 8. Mini-Glossar

| Begriff | Bedeutung |
|---|---|
| **Correspondence Test** | Feldexperiment mit erfundenen schriftlichen Bewerbungen an echte Stellen |
| **Callback** | positive Antwort auf eine Bewerbung, meist eine Einladung zum Gespräch |
| **Odds Ratio (OR)** | Verhältnis der Callback-Chancen Minderheit/Mehrheit; < 1 heisst Diskriminierung |
| **SE** | Standardfehler: wie ungenau eine Schätzung ist |
| **FE** | Fixed Effect: gewichteter Durchschnitt, alle Studien messen denselben Effekt |
| **RE** | Random Effects: der wahre Effekt darf zwischen Studien schwanken |
| **$\tau^2$** | Varianz der wahren Effekte zwischen den Studien |
| **$I^2$** | Anteil der Streuung, der durch echte Unterschiede (nicht Zufall) kommt |
| **UWLS** | Regression, die denselben Wert wie FE gibt, deren KI aber die Heterogenität berücksichtigt |
| **Forest Plot** | Grafik: jede Studie mit Effekt und KI, unten der Durchschnitt |
| **Funnel Plot** | Grafik: Effekt gegen Präzision; schief = Hinweis auf Publication bias |
| **Publication bias** | Nur «schöne» oder signifikante Resultate werden veröffentlicht |
| **FAT-PET** | Regression von Effekt auf SE; prüft und korrigiert Publication bias |
| **Power** | Wahrscheinlichkeit, einen echten Effekt auch zu finden |
| **WAAP** | Durchschnitt nur aus Studien mit genügend Power (≥ 80 %) |
| **ESS** | Vergleich: beobachtete vs. erwartete Anzahl signifikanter Studien |
