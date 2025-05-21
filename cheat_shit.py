import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Exemple de données
df = pd.DataFrame({
    "team": ["Équipe A", "Équipe B", "Équipe C", "Équipe D"],
    "real_staff": [12, 18, 15, 20],
    "target_staff": [15, 16, 15, 22]
})

# Ajouter la ligne Total
df.loc[len(df)] = ["Total", df["real_staff"].sum(), df["target_staff"].sum()]

# Bar chart avec plotly express
fig = px.bar(
    df,
    x="team",
    y="real_staff",
    title="Effectif réel vs cible par équipe",
    labels={"real_staff": "Effectif réel"},
    color_discrete_sequence=["grey"] * (len(df) - 1) + ["red"]
)

# Ajout des lignes horizontales de target (on "écarte" les x pour que ce soit visible)
for i, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["team"], row["team"] + " "],  # Espace pour forcer une ligne visible
        y=[row["target_staff"], row["target_staff"]],
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False
    ))

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

# Améliorations esthétiques
fig.update_layout(
    yaxis_title="Nombre de personnes",
    xaxis_title="Équipe",
    template="simple_white",
    bargap=0.4
)

fig.show()