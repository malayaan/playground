import pandas as pd
from rapidfuzz import fuzz

def check_declarante_match(row, threshold=80):
    """
    Vérifie si le contenu de la colonne 'Déclarant1' est présent dans 'Data'
    et retourne un tuple (match, confidence) selon la source.
    - Pour les PDF, le test est un simple "in" (exact match).
    - Pour l'OCR, on calcule un score de similarité (fuzzy matching).
    """
    declarant = row["Déclarant1"]
    data_text = row["Data"]
    source = row["Source"]
    
    # Si l'une des valeurs est manquante, on retourne False
    if pd.isnull(declarant) or pd.isnull(data_text):
        return False, 0

    if source.upper() == "PDF":
        match = declarant in data_text
        confidence = 100 if match else 0
    else:
        # Pour OCR, on utilise token_set_ratio de RapidFuzz
        confidence = fuzz.token_set_ratio(declarant, data_text)
        match = confidence >= threshold
        
    return match, confidence

# Appliquer la fonction à chaque ligne et ajouter deux nouvelles colonnes
df[['match_declarante', 'confidence']] = df.apply(
    lambda row: pd.Series(check_declarante_match(row, threshold=80)), axis=1
)

# Afficher quelques résultats
print(df[['Déclarant1', 'Data', 'Source', 'match_declarante', 'confidence']].head())