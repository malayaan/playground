from joblib import Parallel, delayed
import pandas as pd
import time

def process_excel_file(filepath):
    # Lire le fichier brut sans header
    df_raw = pd.read_excel(filepath, header=None)

    # Extraire les informations de la cellule A1
    filter_text = str(df_raw.iloc[0, 0])
    
    # Extraction des informations
    risktype = "Debtor Risk"

    situationdate = None
    if "situationdate est" in filter_text:
        situationdate = filter_text.split("situationdate est")[1].split()[0]

    ligne_metier_strat = None
    if "Ligne_Metier_Strategique est" in filter_text:
        after = filter_text.split("Ligne_Metier_Strategique est")[1]
        ligne_metier_strat = after.split('\n')[0].strip()

    # Lire les données à partir de la ligne 3
    df = pd.read_excel(filepath, header=2)

    # Ajouter les colonnes
    df["risktype"] = risktype
    df["situationdate"] = situationdate
    df["Ligne_Metier_Strategique"] = ligne_metier_strat

    return df

# Fonction appelée en parallèle
def excel_concat(i):
    print(f"processing data ({i})")
    file_path = f"C:/Users/A738878/OneDrive - GROUP DIGITAL WORKPLACE/Documents/info/25-ins-016-exposure-to-automotive-sector/data/base_RCT_30_05_2025_data ({i}).xlsx"
    df = process_excel_file(file_path)
    print(f"data ({i}) processed")
    return df

# Liste des fichiers à traiter (1 à 70 inclus)
inputs = range(1, 71)

# Exécution parallèle
dfs = Parallel(n_jobs=-1)(delayed(excel_concat)(i) for i in inputs)

# Fusionner les DataFrames
df_final = pd.concat(dfs, ignore_index=True)

# Enregistrer le résultat
df_final.to_excel("output_concatenated.xlsx", index=False)

print("✅ Traitement terminé.")