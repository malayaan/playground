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
# Créer une barre de progression personnalisée
def tqdm_joblib(tqdm_object):
    """Wrap `tqdm` instance for joblib.Parallel."""
    class TqdmBatchCompletionCallback:
        def __init__(self, tqdm_object):
            self.tqdm_object = tqdm_object
            self.tqdm_object.total = tqdm_object.total

        def __call__(self, *args, **kwargs):
            self.tqdm_object.update(n=1)

    return TqdmBatchCompletionCallback(tqdm_object)

# Étape 4 : Lancer les calculs parallèles avec tqdm
with tqdm(total=len(loan_tape), desc="Traitement des lignes", unit="ligne") as progress_bar:
    results = Parallel(n_jobs=-1, backend="loky", verbose=0)(
        delayed(process_row)(index, row)
        for index, row in loan_tape.iterrows()
    )

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