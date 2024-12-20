import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# Charger les données nécessaires
# Exemple fictif, remplacez par vos données réelles
loan_tape = pd.read_csv("loan_tape.csv")  # Chargez votre DataFrame
top_anomalies = loan_tape.sort_values(by="anomaly_score", ascending=False).head(10)  # Extrait le top 10 des anomalies
rules_metier = pd.read_csv("rules_metier.csv")  # Chargez vos règles métier si nécessaire

# Interface Streamlit
st.title("Exploration des anomalies dans la Loan Tape")

# Afficher le tableau des anomalies
st.subheader("Top anomalies détectées")
selected_row = st.dataframe(top_anomalies)

# Sélectionner une ligne du tableau
st.write("Sélectionnez une ligne dans le tableau ci-dessus pour afficher les détails.")

selected_index = st.selectbox(
    "Sélectionnez l'index de l'anomalie à visualiser",
    options=top_anomalies.index.tolist(),
    format_func=lambda x: f"Index {x}"
)

# Lorsque l'utilisateur sélectionne une ligne
if selected_index is not None:
    st.subheader(f"Détails pour l'anomalie sélectionnée (Index : {selected_index})")

    # Extraire les informations de la ligne sélectionnée
    selected_anomaly = loan_tape.loc[selected_index]

    # Afficher les données de la ligne sous forme de tableau
    st.write("**Données de la ligne sélectionnée :**")
    st.write(selected_anomaly.to_frame().transpose())

    # Tracer les histogrammes
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Histogramme des métriques métier
    axs[0].hist(rules_metier.values.flatten(), bins=8, color="blue", edgecolor="black")
    axs[0].set_xlabel("Valeurs")
    axs[0].set_ylabel("Fréquence")
    axs[0].set_title("Histogramme des métriques métier")

    # Histogramme du score d'anomalie
    axs[1].hist(loan_tape["anomaly_score"], bins=8, color="green", edgecolor="black")
    axs[1].set_xlabel("Valeurs")
    axs[1].set_ylabel("Fréquence")
    axs[1].set_title("Histogramme des scores d'anomalie")
    axs[1].invert_xaxis()

    # Afficher les graphiques
    st.pyplot(fig)

    # Ajouter une analyse des risques ou des détails spécifiques si nécessaire
    st.subheader("Analyse des métriques de risque pour la ligne sélectionnée")
    metrics = rules_metier.loc[selected_index]
    st.bar_chart(metrics.sort_values())  # Trier les métriques par ordre croissant