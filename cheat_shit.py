import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# Étape 1 : Initialiser les DataFrames avec les index de LoanTape
LongTapeAnomaliesCore = pd.DataFrame(index=loan_tape.index, columns=feature_names)
LongTapeRiskValues = pd.DataFrame(index=loan_tape.index, columns=control_names)

# Fonction pour traiter une seule ligne
def process_row(index_row_tuple):
    index, row = index_row_tuple
    single_row_df = loan_tape.loc[[index]]

    # Calcul des valeurs d'anomalies
    feature_names, anomaly_values = od.plot_feature_summarizer(
        relevant_features=cols_reduced,
        df_lt=loan_tape,
        i=0,
        top_anomalies=single_row_df,
        iso_forest=iso_forest,
        display=False
    )

    # Calcul des valeurs de risque
    control_names, risk_values = od.plot_risk_metrics_for_control(
        loan_tape.loc[[index]],
        [col for col in controle_list if col not in to_drop],
        rules_metier.loc[[index]],
        t=0,
        display=False
    )

    return index, anomaly_values, risk_values

# Étape 2 : Utiliser le parallélisme pour traiter chaque ligne
with ProcessPoolExecutor() as executor:
    # Préparer les tâches
    tasks = {executor.submit(process_row, (idx, row)): idx for idx, row in loan_tape.iterrows()}
    
    # Barre de progression avec tqdm
    for future in tqdm(as_completed(tasks), total=len(tasks)):
        try:
            # Récupérer les résultats pour chaque ligne
            index, anomaly_values, risk_values = future.result()
            
            # Mettre à jour les DataFrames
            LongTapeAnomaliesCore.loc[index] = anomaly_values
            LongTapeRiskValues.loc[index] = risk_values
        except Exception as e:
            print(f"Erreur pour l'index {tasks[future]} : {e}")

# Étape 3 : Afficher les résultats pour vérification
print("LongTapeAnomaliesCore:")
print(LongTapeAnomaliesCore.head())

print("\nLongTapeRiskValues:")
print(LongTapeRiskValues.head())