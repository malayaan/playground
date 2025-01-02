from joblib import Parallel, delayed
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

# Étape 1 : Initialiser les DataFrames
LongTapeAnomaliesCore = pd.DataFrame(index=loan_tape.index, columns=feature_names)
LongTapeRiskValues = pd.DataFrame(index=loan_tape.index, columns=control_names)

# Étape 2 : Fonction pour traiter une ligne individuelle
def process_row(index, row):
    # Simuler un délai pour tester la progression
    time.sleep(0.1)  # Facultatif : Retirer dans le code final

    # Initialiser les valeurs pour la ligne
    single_row_df = loan_tape.loc[[index]]

    # Calculer les anomalies
    feature_names, anomaly_values = od.plot_feature_summarizer(
        relevant_features=cols_reduced,
        df_lt=loan_tape,
        i=0,
        top_anomalies=single_row_df,
        iso_forest=iso_forest,
        display=False
    )

    # Calculer les risques
    control_names, risk_values = od.plot_risk_metrics_for_control(
        loan_tape.loc[[index]],
        [col for col in controle_list if col not in to_drop],
        rules_metier.loc[[index]],
        i=0,
        display=False
    )

    return anomaly_values, risk_values

# Étape 3 : Intégration de tqdm pour afficher la progression
def tqdm_parallel(iterable, func, n_jobs=-1, backend="loky"):
    """Wrapper pour intégrer tqdm à joblib.Parallel."""
    with tqdm(total=len(iterable)) as pbar:
        def tqdm_update(*args):
            pbar.update()
        results = Parallel(n_jobs=n_jobs, backend=backend)(
            delayed(func)(*item) for item in iterable
        )
    return results

# Étape 4 : Préparer les données pour joblib et tqdm
iterable = [(index, row) for index, row in loan_tape.iterrows()]

# Lancer le traitement avec tqdm et joblib
results = tqdm_parallel(iterable, process_row)

# Étape 5 : Stocker les résultats dans les DataFrames
for idx, (anomaly_values, risk_values) in enumerate(results):
    index = loan_tape.index[idx]
    LongTapeAnomaliesCore.loc[index] = anomaly_values
    LongTapeRiskValues.loc[index] = risk_values

# Étape 6 : Afficher les résultats pour vérification
print("LongTapeAnomaliesCore:")
print(LongTapeAnomaliesCore)

print("\nLongTapeRiskValues:")
print(LongTapeRiskValues)