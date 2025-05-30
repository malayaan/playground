import pandas as pd

def process_excel_file(filepath):
    # Lire le fichier sans inférer les noms de colonnes
    df_raw = pd.read_excel(filepath, header=None)

    # Lire le texte des filtres dans la cellule A1
    filter_text = str(df_raw.iloc[0, 0])

    # Extraire la date de situation
    situationdate = None
    if "situationdate est" in filter_text:
        situationdate = filter_text.split("situationdate est")[1].split()[0]

    # Extraire Ligne_Metier_Strategique jusqu'au retour à la ligne
    ligne_metier_strat = None
    if "Ligne_Metier_Strategique est" in filter_text:
        after = filter_text.split("Ligne_Metier_Strategique est")[1]
        ligne_metier_strat = after.split('\n')[0].strip()

    # Lire les données à partir de la ligne 3 (index 2)
    df = pd.read_excel(filepath, header=2)

    # Ajouter les colonnes
    df["risktype"] = "Debtor Risk"
    df["situationdate"] = situationdate
    df["Ligne_Metier_Strategique"] = ligne_metier_strat

    return df