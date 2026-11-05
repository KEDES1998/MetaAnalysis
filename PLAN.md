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
Random-Effects-Modell mit 34 Studien: **OR = 0.60 [0.52; 0.69]** (Figure 1 im Paper).
Das heisst: Minderheiten haben rund 40 % tiefere Odds auf einen Callback. Anders gesagt: Sie müssen etwa 50 % mehr Bewerbungen schreiben, um gleich oft eingeladen zu werden.

(Figure 1 im Paper zeigt nur 33 Zeilen. Das Modell der Autoren rechnet aber mit 34 Studien – das sieht man im R-Output der Autoren, `01_data/raw_files/meta-replication.pdf`.)

**Stand 3.11.: Replikation geschafft.**
Der Python-Code trifft die Zahlen der Autoren exakt (OR 0.60 [0.52; 0.69], $\hat\tau^2 = 0.141$, $I^2 = 92.7\%$). Wie man den Code startet, steht in Abschnitt 9.

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
- [x] `requirements.txt` füllen: `numpy`, `pandas`, `scipy`, `matplotlib` (statsmodels brauchen wir nicht).
- [ ] Python-Umgebung anlegen und Pakete installieren (jede Person einmal auf ihrem Computer):
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- [x] `.gitignore` füllen (`venv/`, `.DS_Store`, `__pycache__/`, `03_tmp/`, PDFs – ausser den Plots in `04_report/figures/`).
- [ ] Overleaf-Projekt anlegen und die andere Person einladen.
- [x] Gruppennummer klären: Gruppe 4 → `group4.pdf`, Präsentation Di 24.11.

**Fertig, wenn:** Beide können Python im Repo starten, und beide haben Zugriff auf Overleaf.

---

### Schritt 1 – Daten der Original-Studie aufbereiten

**Ziel:** Eine saubere CSV-Datei mit allen 34 Studien. Für jede Studie: Effekt ($\ln OR$) und Standardfehler (SE).

Es gibt zwei Quellen:

- **Quelle A (besser): Die Replikationsdaten der Autoren** auf Harvard Dataverse: <https://doi.org/10.7910/DVN/ZU8H79>.
  Liegen **unverändert** in `01_data/raw_files/` (erledigt).
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

- [x] Dataverse-Dateien anschauen: `meta-clean.csv` hat 43 Studien und 738 Subgruppen. Nur 34 Studien (und 215 Subgruppen) haben die vier Callback-Zahlen, die man für die OR braucht.
- [x] Skript `02_code/01_prepare_data.py` schreiben. Es liest die Rohdaten, rechnet `log_or` und `se` und speichert `01_data/zr2016_studies.csv`.
- [x] Kontrolle: Alle 34 OR-Werte stimmen mit dem Forest Plot der Autoren überein (auf 2 Nachkommastellen).
- [x] Moderatoren mitnehmen: Land, Kontinent, EU, deutschsprachig, Testjahr, Geschlecht, Generation, Skill-Level, EU-Richtlinie vorher/nachher.

**Ergebnis:** `01_data/zr2016_studies.csv` (34 Studien), `zr2016_subgroups.csv` (215 Subgruppen), `zr2016_studies_no_counts.csv` (die 9 Studien ohne Zahlen – sie gehören trotzdem ins Literaturverzeichnis).

**Fertig, wenn:** 34 Zeilen, jede mit `log_or` und `se`, und die Werte passen zu Figure 1. ✔

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

- [x] Skript `02_code/02_replication.py` schreiben.
- [x] FE, RE und UWLS rechnen. Für RE die Methode **REML** nehmen (so hat es das Original gemacht, mit dem R-Paket metafor). Zum Vergleich auch DerSimonian-Laird, Paule-Mandel und Knapp-Hartung.
- [x] Ergebnisse in OR zurückrechnen: $OR = e^{y}$.
- [x] Tabelle machen: Methode | OR | 95%-KI | $\tau^2$ | $I^2$.
- [x] Forest Plot zeichnen und als PDF speichern.
- [x] Bendick et al. (1991) ist ein Ausreisser (OR = 2.45; dort hatten die Latino-Bewerbungen bessere Qualifikationen). Wir rechnen einmal **mit** und einmal **ohne** diese Studie.

**Ergebnis:** `04_report/tables/replication.tex` und `04_report/figures/forest_original.pdf`

**Resultat:**

| Methode | OR | 95%-KI |
|---|---|---|
| FE | 0.63 | [0.61; 0.65] |
| UWLS | 0.63 | [0.56; 0.71] |
| RE (REML) | 0.60 | [0.52; 0.69] |
| RE ohne Bendick (k = 33) | 0.58 | [0.52; 0.65] |
| RE auf Subgruppen-Ebene (k = 215) | 0.55 | [0.52; 0.58] |

**Fertig, wenn:**
- [x] RE ergibt 0.60 [0.52; 0.69]. ✔ (exakt wie im Original)
- [x] FE und UWLS haben denselben Schätzwert. ✔ (beide 0.63)
- [ ] Wir können erklären, welches Konfidenzintervall breiter ist und warum.
  Tipp: Das UWLS-Intervall ist rund 3-mal breiter. Der Faktor ist $\sqrt{Q/(k-1)} = \sqrt{327.7/33} \approx 3.15$. Er ist grösser als 1, weil die Studien viel stärker streuen, als es der Zufall allein erklären würde (Heterogenität).

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
- [ ] Zahlen in `01_data/update_studies.csv` eintragen. Die Datei ist schon vorbereitet (nur die Kopfzeile). Am einfachsten in Excel oder Numbers öffnen und als CSV speichern.
- [ ] Bei jeder Zahl die Quelle notieren (Spalte `source`, z. B. «Table 2, p. 240»).
- [ ] Pro Studie **eine Zeile**: alle Minderheiten zusammen gegen die Mehrheit. So ist es wie im Original auf Studienebene.
- [ ] PDFs der neuen Studien in `01_data/update_papers/` ablegen.

Die wichtigsten Spalten in `update_studies.csv`:

| Spalte | Was eintragen | Beispiel |
|---|---|---|
| `authors`, `year` | Autoren, Erscheinungsjahr | Koopmans et al., 2019 |
| `country` | Land auf Englisch | Germany |
| `testing_year` | Jahr, in dem die Bewerbungen verschickt wurden | 2014 |
| `minority` | getestete Gruppe(n) | Turkish, Arab |
| `gender`, `skills` | male / female / both; high / low / mixed | both, mixed |
| `n_minority`, `cb_minority` | Anzahl Bewerbungen und Anzahl Callbacks der **Minderheit** | 3000, 600 |
| `n_majority`, `cb_majority` | dasselbe für die **Mehrheit** | 3000, 800 |
| `or`, `ci_low`, `ci_high` | **nur** wenn es keine Zahlen gibt: berichtete OR mit 95%-KI | |
| `source`, `notes` | Seite/Tabelle; Bemerkungen | Table 2, p. 240 |

Wenn eine Studie nur Callback-**Quoten** nennt: Anzahl Callbacks = Quote × Anzahl Bewerbungen (runden) und in `notes` vermerken.

**Fertig, wenn:** Mindestens 2 Studien mit `log_or` und `se`, und jede Zahl hat eine Quellenangabe. Danach einfach `python 02_code/run_all.py` laufen lassen – Schritte 4 bis 7 rechnen dann automatisch mit den neuen Studien.

---

### Schritt 4 – Update rechnen

**Ziel:** Prüfen, ob die neuen Studien zum alten Ergebnis passen.

So geht's:

- [x] Skript `02_code/03_update.py` schreiben. (Fertig und getestet – wartet nur auf die neuen Studien.)
- [ ] **Frage A:** Liegen die neuen Effekte im Konfidenzintervall des Originals, also zwischen 0.52 und 0.69?
- [ ] **Frage B:** Neue Meta-Schätzung mit allen Studien zusammen (alt + neu). Ändert sie sich stark?
- [ ] Für die Diskussion: Auch das *Prediction Interval* anschauen: [0.28; 1.27]. Es zeigt, wo eine **einzelne neue** Studie liegen sollte. Das ist bei starker Heterogenität fairer als das Konfidenzintervall des Durchschnitts.

**Ergebnis:** `04_report/tables/update_new_studies.tex` (Frage A), `update_pooled.tex` (Frage B), `04_report/figures/forest_combined.pdf` (neue Studien rot) und die Tabelle der Evidenz `evidence_table.tex` für den Anhang.

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

- [x] Skript `02_code/04_power_bias.py` schreiben.
- [x] Power pro Studie rechnen, dann den **Median**.
- [ ] Vergleich mit Askarov et al. (2024): Dort hat dieses Gebiet eine durchschnittliche Power von 0.91. In der Ökonomie insgesamt liegt der Median nur bei ca. 7 %.
- [ ] Diskutieren: Warum ist tiefe Power ein Problem? Warum ist unser Wert eher eine Obergrenze?
  (Tipp: Wenn Publication bias den Meta-Effekt grösser macht, wird auch die berechnete Power zu gross.)

**Resultat (Originalstudien):** Median-Power **0.97**, Durchschnitt 0.83. 24 von 34 Studien haben genügend Power (≥ 80 %). Die Erwartung stimmt also: Die Power ist hoch, weil Correspondence Tests oft Tausende Bewerbungen verschicken.

**Ergebnis:** `04_report/tables/power_bias_stats.tex`, `power_by_study.csv`, `04_report/figures/power_original.pdf`

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

- [x] Alle vier Methoden in `02_code/04_power_bias.py` rechnen (dazu PEESE als Extra).
- [x] Funnel Plot als PDF speichern (einmal mit SE, einmal mit Präzision $1/SE$ auf der y-Achse).
- [x] Eine Tabelle mit allen Schätzungen: FE, RE, UWLS, WAAP, PET, PEESE – für Original, Original ohne Bendick und (nach dem Update) Original + neue Studien.

**Resultat (Originalstudien):**

| | Wert |
|---|---|
| WAAP | OR 0.64 [0.55; 0.73] – fast gleich wie UWLS (0.63) |
| FAT: $\hat\beta_1$ | −1.05 (SE 1.29), also kein klarer Zusammenhang zwischen Effekt und SE |
| PET | OR 0.69 [0.53; 0.91] – etwas weniger Diskriminierung als UWLS, aber immer noch deutlich unter 1 |
| ESS | 27 von 34 Studien signifikant (79 %), erwartet wären 83 % → kein Überschuss an Signifikanz |

Zum Vergleich: Die Autoren selbst haben im Supplement (S12) mit «Trim & Fill» 8 bis 9 «fehlende» Studien auf der rechten Seite gefunden (also Studien mit weniger Diskriminierung). Das passt zur leicht negativen FAT – lohnt sich für die Diskussion.

**Achtung für den Bericht:** Bei der log OR hängt der SE rechnerisch ein bisschen mit der Grösse des Effekts zusammen. Etwas Schiefe im Funnel Plot kann deshalb auch ohne Publication bias entstehen. Das schreiben wir als Einschränkung dazu.

**Ergebnis:** `04_report/tables/pubbias_estimates.tex`, `power_bias_stats.tex` und `04_report/figures/funnel_original.pdf`, `funnel_precision_original.pdf`

---

### Schritt 7 – Meta-Regression mit Moderatoren (wenn Daten vorhanden)

**Ziel:** Erklären, *warum* die Studien unterschiedliche Effekte finden (Heterogenität).

Wir erweitern die Regression aus Schritt 6 um Moderatoren, zum Beispiel:

$$
y_i = \beta_0 + \beta_1 \, SE_i + \beta_2 \, \text{Europe}_i + \beta_3 \, \text{Post2000}_i + \beta_4 \, \text{GermanSpeaking}_i + \varepsilon_i
$$

Ideen aus dem Paper: Region (Europa vs. Nordamerika), vor/nach den EU-Richtlinien (2000), deutschsprachige Länder, Jahr.

- [x] Skript `02_code/05_meta_regression.py` schreiben. Kontrolle: Ein Modell der Autoren (Supplement, Modell mit Skill-Level) wird exakt repliziert.
- [x] Nur wenige Moderatoren nehmen. Wir haben nur ca. 35 Studien, also vorsichtig interpretieren.

Die Modelle (jeweils mit SE, also gleichzeitig Publication bias):

- M1: nur SE (= FAT-PET)
- M2: + Europa, deutschsprachiges Land
- M3: + Skill-Level der Stellen (hoch / tief, Referenz: gemischt)
- M4: + Testjahr (in Jahrzehnten)
- M5: + «neue Studie» (erst nach dem Update)

**Erster Befund (Originalstudien, WLS):** In Europa ist die Diskriminierung grösser als ausserhalb Europas (vor allem Nordamerika): Koeffizient ca. −0.29, das heisst eine rund 25 % tiefere OR. Für deutschsprachige Länder ist der Koeffizient positiv (weniger Diskriminierung als im übrigen Europa), aber unsicher.

**Ergebnis:** `04_report/tables/metareg_wls.tex` (Hauptmodell, WLS wie vom Prof verlangt), `metareg_re.tex` (Random-Effects-Version wie im Original)

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
- [x] In welchem Format sind die Dataverse-Daten? → CSV (`meta-clean.csv`) plus R-Code und Supplement. Moderatoren sind drin (Land, Jahr, Generation, Geschlecht, Skill-Level, EU-Richtlinie).
- [ ] Bendick et al. (1991): im Hauptmodell lassen oder als Ausreisser behandeln? (Der Code rechnet beides.)
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

---

## 9. Code – Kurzanleitung

**Einmal einrichten** (im Terminal, im Ordner des Repos):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Alles rechnen:**

```bash
source venv/bin/activate
python 02_code/run_all.py
```

Das dauert ein paar Sekunden. Im Output stehen die Kontrollen («OK») und die wichtigsten Zahlen.

**Was wo herauskommt:**

| Datei | Wofür |
|---|---|
| `04_report/figures/*.pdf` | Grafiken für Overleaf |
| `04_report/figures/*.png` | dieselben Grafiken für die Folien |
| `04_report/tables/*.tex` | fertige LaTeX-Tabellen für Overleaf |
| `04_report/tables/*.csv` | dieselben Zahlen zum Anschauen (Excel) |
| `04_report/tables/macros_*.tex` | Zahlen für den Fliesstext, z. B. `\maORre` → 0.60 |

**In Overleaf:**

1. Die Ordner `04_report/figures` und `04_report/tables` hochladen (als `figures/` und `tables/`).
2. In die Präambel: `\usepackage{booktabs,longtable,array,graphicx}`
3. Makros laden: `\input{tables/macros_replication.tex}` (ebenso `macros_power_bias.tex` und nach dem Update `macros_update.tex`).
4. Tabelle einfügen: `\input{tables/replication.tex}`. Grafik: `\includegraphics[width=\linewidth]{figures/forest_original.pdf}`.
5. Im Text: «The pooled odds ratio is \maORre{} \maCIre.» → «The pooled odds ratio is 0.60 [0.52; 0.69].»

Wenn neue Studien dazukommen: `update_studies.csv` ergänzen, `run_all.py` laufen lassen, die Ordner neu nach Overleaf hochladen. Alle Zahlen passen sich dann automatisch an.

| Skript | Schritt im Plan |
|---|---|
| `01_prepare_data.py` | 1 – Daten aufbereiten |
| `02_replication.py` | 2 – Replikation |
| `03_update.py` | 3 und 4 – neue Studien, Tabelle der Evidenz |
| `04_power_bias.py` | 5 und 6 – Power, Publication bias |
| `05_meta_regression.py` | 7 – Meta-Regression |
| `utils_meta.py` | alle Formeln (FE, RE, UWLS, WAAP, …) und Grafiken |
