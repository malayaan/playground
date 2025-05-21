import plotly.graph_objects as go
import pandas as pd

# Exemple de données
df = pd.DataFrame({
    "team": ["Équipe A", "Équipe B", "Équipe C", "Équipe D"],
    "real_staff": [12, 18, 15, 20],
    "target_staff": [15, 16, 15, 22]
})

# Ajouter la ligne Total
df.loc[len(df)] = ["Total", df["real_staff"].sum(), df["target_staff"].sum()]

# Créer la figure
fig = go.Figure()

# Barres d'effectif réel
fig.add_trace(go.Bar(
    x=df["team"],
    y=df["real_staff"],
    name="Réel",
    marker_color=["grey"] * (len(df) - 1) + ["red"]
))

# Ajout des lignes de target (traits fins pleins)
for i, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["team"], row["team"]],
        y=[row["target_staff"], row["target_staff"]],
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False
    ))

# Ajout des flèches (bonne direction)
for i, row in df.iterrows():
    fig.add_annotation(
        x=row["team"],
        y=row["target_staff"],
        ax=row["team"],
        ay=row["real_staff"],
        xref='x',
        yref='y',
        axref='x',
        ayref='y',
        text="",  # Pas de texte
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="black"
    )

# Mise en forme
fig.update_layout(
    title="Effectif réel vs cible par équipe",
    yaxis_title="Nombre de personnes",
    xaxis_title="Équipe",
    template="simple_white",
    bargap=0.4
)

fig.show()