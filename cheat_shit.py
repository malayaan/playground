import dask.dataframe as dd
from dask import delayed
import pandas as pd

# Charger le DataFrame initial (remplacez par votre code de chargement)
loan_tape = pd.read_csv('your_large_dataset.csv')  # Exemple de chargement
loan_tape_dd = dd.from_pandas(loan_tape, npartitions=44)  # Divisez en partitions selon le nombre de processeurs

# Fonction à appliquer sur chaque partition
def process_partition(partition):
    LoanTapeAnomaliesScore = pd.DataFrame(
        index=partition.index,
        columns=[x for x in partition.columns if x not in to_drop]
    )
    
    LoanTapeRiskValues = pd.DataFrame(
        index=partition.index,
        columns=[x for x in controle_list if x not in to_drop]
    )
    
    results = []
    for index, row in partition.iterrows():
        single_row_df = partition.loc[[index]]
        
        # Calcul des anomalies
        anomaly_values = od.plot_feature_summarizer(
            relevant_features=cols_reduced,
            df=single_row_df,
            top_anomalies=single_row_df.shape[1],
            display=False,
            top_number=LoanTapeAnomaliesScore.shape[1],
        )
        df_anomaly = pd.DataFrame({
            'feature_name': [value for value in anomaly_values]
        })
        
        # Calcul des contrôles
        risk_values = od.plot_risk_metrics_for_control(
            loan_tape=single_row_df,
            control_list=[col for col in controle_list if col not in to_drop],
            rules=rules_metier_loc[index],
            display=False,
            top_number=LoanTapeRiskValues.shape[1],
        )
        df_control = pd.DataFrame({
            'control_names': risk_values
        })

        results.append((df_anomaly, df_control))
    
    return results

# Appliquer la fonction sur chaque partition
processed = loan_tape_dd.map_partitions(process_partition, meta=object)

# Récupérer les résultats finaux
results = processed.compute()