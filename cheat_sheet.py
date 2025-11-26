. Ne plus envoyer un CSV dense, mais une représentation sparse

Plutôt que :

ligne1: ,,,NOM,PRENOM,,,ADRESSE,,,,,,
ligne2: ,,,DURAND,Alexis,,,12 rue ...,,
...

Fais un truc du style :

ROW1: C4="NOM", C5="PRENOM"
ROW2: C4="DURAND", C5="Alexis", C7="12 rue ..."
ROW3: C2="Période", C3="01/10/2024 - 31/10/2024"
...

Idées pour limiter les tokens :

Row/Col en très court : R1C4="NOM" au lieu de longs mots.

Ne pas écrire les cellules vides (c’est là que tu gagnes vraiment).

Ne pas envoyer les coordonnées XY brutes au LLM : tu les utilises en amont pour reconstruire les indices de ligne/colonne, pas besoin de les inclure.