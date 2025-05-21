import plotly.graph_objects as go
import pandas as pd

# Données d’exemple (à adapter selon ton cas réel)
df = pd.DataFrame({
    "team": ["Équipe A", "Équipe B", "Équipe C", "Équipe D"],
    "real_staff": [12, 18, 15, 20],
    "target_staff": [15, 16, 15, 22]
})

# Ajout de la ligne Total
df.loc[len(df)] = ["Total", df["real_staff"].sum(), df["target_staff"].sum()]

# Création de la figure avec go.Bar pour garder le contrôle
fig = go.Figure()

# Barres d'effectif réel
fig.add_trace(go.Bar(
    x=df["team"],
    y=df["real_staff"],
    marker_color=["grey"] * (len(df) - 1) + ["red"],
    name="Effectif réel"
))

# Ajout des lignes horizontales cibles
for i, row in df.iterrows():
    fig.add_shape(
        type="line",
        x0=i - 0.3,
        x1=i + 0.3,
        y0=row["target_staff"],
        y1=row["target_staff"],
        line=dict(color="black", width=2),
        xref="x",
        yref="y"
    )

# Ajout des flèches
for i, row in df.iterrows():
    fig.add_annotation(
        x=row["team"],
        y=row["target_staff"],
        ax=row["team"],
        ay=row["real_staff"],
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="black"
    )

# Layout
fig.update_layout(
    title="Effectif réel vs cible par équipe",
    yaxis_title="Nombre de personnes",
    xaxis_title="Équipe",
    template="simple_white",
    bargap=0.4
)

fig.show()