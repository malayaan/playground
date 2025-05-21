import matplotlib.pyplot as plt
import pandas as pd

# Exemple de données (remplace-les par les tiennes)
df = pd.DataFrame({
    "team": ["Équipe A", "Équipe B", "Équipe C", "Équipe D"],
    "real_staff": [12, 18, 15, 20],
    "target_staff": [15, 16, 15, 22]
})

# Ajouter la ligne agrégée
total_row = pd.DataFrame({
    "team": ["Total"],
    "real_staff": [df["real_staff"].sum()],
    "target_staff": [df["target_staff"].sum()]
})

df = pd.concat([df, total_row], ignore_index=True)

# Couleurs : rouge pour la moyenne
colors = ['grey'] * (len(df) - 1) + ['red']

# Création du graphique
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df["team"], df["real_staff"], color=colors)

# Cibles et flèches
for i, row in df.iterrows():
    # Ligne pointillée horizontale à la hauteur de la cible
    ax.hlines(y=row["target_staff"], xmin=i - 0.3, xmax=i + 0.3, color="black", linestyle="--")
    # Flèche entre réel et cible
    ax.annotate("",
                xy=(i, row["target_staff"]),
                xytext=(i, row["real_staff"]),
                arrowprops=dict(arrowstyle="->", color="black"))

# Ajustements
ax.set_ylabel("Effectif")
ax.set_title("Effectif réel vs cible par équipe")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()