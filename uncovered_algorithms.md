
# Yet uncovered algorithms / approaches

## DPLL-artig



## Local search based

### Moser-Scheder algorithm

Eine Erweiterung von Dantsins Ansatz: auch hier werden Überdeckungscodes genutzt, 
jedoch nochmal mit Kniffen klüger aufgespannt. Die Kernidee bleibt jedoch die gleiche.
Erreicht jedoch O(1.33^n) für 3-SAT (statt 1.5).

### Novelty / Novelty+

Eine weitere Ausprägung der GSAT / WSAT Familie.
Hier wurde weiter an der Variablenauswahl geklügelt.
Zum GSAT-"score" kommt jetzt noch das "Alter" hinzu.
So werden zu gewissem Grad auch die vergangenen bereits getesteten Belegung in Betracht gezogen,
nicht nur die aktuelle.
Folge: gerade eben geflippte Variablen können nicht direkt wieder zurückgeflippt werden.

## Sonstiges

### Stalmarck

### OBDSS?


