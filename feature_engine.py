import pandas as pd
import matplotlib.pyplot as plt

def plot_risk_metrics_for_control(control_id, df, risk_metric_columns, control_column='control_id'):
    """
    Affiche un plot bar des métriques de risque triées par ordre croissant pour une ligne de contrôle donnée.
    
    Paramètres :
    ----------
    control_id : str ou int
        Identifiant de la ligne de contrôle à visualiser.
    df : pd.DataFrame
        DataFrame contenant les informations sur les contrôles et leurs métriques de risque.
    risk_metric_columns : list
        Liste des colonnes correspondant aux métriques de risque.
    control_column : str
        Nom de la colonne identifiant les contrôles dans la DataFrame (par défaut 'control_id').
        
    Retour :
    ------
    Bar plot des métriques de risque pour le contrôle spécifié.
    """
    # Vérification que le contrôle existe dans la DataFrame
    if control_id not in df[control_column].values:
        raise ValueError(f"Le contrôle {control_id} n'existe pas dans la DataFrame.")
    
    # Sélectionner la ligne du contrôle
    control_data = df[df[control_column] == control_id]
    
    # Extraire les métriques de risque
    risk_metrics = control_data[risk_metric_columns].iloc[0]  # On prend la première ligne correspondant au contrôle
    risk_metrics_sorted = risk_metrics.sort_values()  # Trier par ordre croissant
    
    # Plot
    plt.figure(figsize=(10, 6))
    risk_metrics_sorted.plot(kind='bar', color='skyblue', alpha=0.8)
    plt.title(f"Métriques de risque pour le contrôle {control_id}")
    plt.ylabel("Valeur de la métrique de risque")
    plt.xlabel("Métriques de risque")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()