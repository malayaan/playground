import plotly.graph_objects as go
import pandas as pd

# Exemple de données
df = pd.DataFrame({
    "team": ["Équipe A", "Équipe B", "Équipe C", "Équipe D"],
    "real_staff": [12, 18, 15, 20],
    "target_staff": [15, 16, 15, 22]
})

# Ajouter ligne agrégée
df.loc[len(df)] = ["Total", df["real_staff"].sum(), df["target_staff"].sum()]

fig = go.Figure()

# Barres d'effectif réel
fig.add_trace(go.Bar(
    x=df["team"],
    y=df["real_staff"],
    name="Réel",
    marker_color=["grey"] * (len(df) - 1) + ["red"]
))

# Lignes de cible + flèches
for i, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["team"], row["team"]],
        y=[row["real_staff"], row["target_staff"]],
        mode="lines+markers",
        marker=dict(size=1),
        line=dict(color="black", dash="dot"),
        showlegend=False
    ))
    fig.add_annotation(
        x=row["team"],
        y=(row["real_staff"] + row["target_staff"]) / 2,
        ax=0,
        ay=row["real_staff"] - row["target_staff"],
        xanchor='center',
        text="",
        arrowhead=3,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="black"
    )

# Mise en forme
fig.update_layout(
    title="Effectif réel vs cible par équipe",
    yaxis_title="Effectif",
    xaxis_title="Équipe",
    template="simple_white",
    bargap=0.4
)

fig.show()