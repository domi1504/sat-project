
# Yet uncovered algorithms / approaches

## DPLL-artig

### Look-ahead based SAT solvers

Reference: Handbook Chapter 5.

Hier wird auf der DPLL-Backtracking Basis aufgebaut:
bei der Wahl der nächsten Variable wird nicht nur eine Heuristik verwendet,
sondern ein bisschen mehr Rechenaufwand in die Entscheidung gesteckt.
Idee: mehr Aufwand in die Entscheidung stecken, um bessere zu treffen (schneller ans Ziel kommen).

## Local search based

### Moser-Scheder algorithm

Eine Erweiterung von Dantsins Ansatz: auch hier werden Überdeckungscodes genutzt, 
jedoch nochmal mit Kniffen klüger aufgespannt. Die Kernidee bleibt jedoch die gleiche.
Erreicht jedoch O(1.33^n) für 3-SAT (statt 1.5).

Reference: Schöning p.106 f.

### Novelty / Novelty+

Eine weitere Ausprägung der GSAT / WSAT Familie.
Hier wurde weiter an der Variablenauswahl geklügelt.
Zum GSAT-"score" kommt jetzt noch das "Alter" hinzu.
So werden zu gewissem Grad auch die vergangenen bereits getesteten Belegung in Betracht gezogen,
nicht nur die aktuelle.
Folge: gerade eben geflippte Variablen können nicht direkt wieder zurückgeflippt werden.

Reference: Schöning p.111 f.

## Sonstiges

- DP-Algorithm
- Stalmarck
- OBDSS / Symbolic SAT
