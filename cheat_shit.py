import pandas as pd
import plotly.graph_objects as go

# Données (Confirmed et Intermediate extraits manuellement)
data = [
    ["CFM", "Confirmed", 15.0, 22.64],
    ["CFM", "Intermediate", 15.0, 20.75],
    ["GBI", "Confirmed", 20.10, 6.10],
    ["GBI", "Intermediate", 20.33, 20.73],
    ["GIS", "Confirmed", 20.0, 7.69],
    ["GIS", "Intermediate", 50.0, 30.77],
    ["IRB", "Confirmed", 4.55, 3.88],
    ["IRB", "Intermediate", 21.22, 14.56],
    ["RPI", "Confirmed", 4.23, 0.0],
    ["RPI", "Intermediate", 26.47, 29.79],
]
df = pd.DataFrame(data, columns=["team", "data_skill_cat", "target_ratio", "real_ratio"])

# Ajouter "Beginner" par complément à 100%
def complete_beginner_ratios(group):
    t_sum = group["target_ratio"].sum()
    r_sum = group["real_ratio"].sum()
    group = group.copy()
    group.loc[len(group.index)] = [
        group["team"].iloc[0], "Beginner",
        max(0, 100 - t_sum),
        max(0, 100 - r_sum)
    ]
    return group

df = df.groupby("team", group_keys=False).apply(complete_beginner_ratios)

# Totaux par équipe
team_totals = {
    "CFM": 30,
    "GBI": 120,
    "GIS": 24,
    "IRB": 84,
    "RPI": 33
}

# Calcul des effectifs
df["total_nb"] = df["team"].map(team_totals)
df["target_nb"] = (df["target_ratio"] * df["total_nb"] / 100).round(1)
df["real_nb"] = (df["real_ratio"] * df["total_nb"] / 100).round(1)

# Création du graphique
fig = go.Figure()
color_map = {"Beginner": "red", "Intermediate": "pink", "Confirmed": "black"}
levels = ["Beginner", "Intermediate", "Confirmed"]

# Barres Target
for level in levels:
    sub = df[df["data_skill_cat"] == level]
    fig.add_bar(
        name=f"Target - {level}",
        x=sub["team"],
        y=sub["target_ratio"],
        marker_color=color_map[level],
        offsetgroup=0,
        legendgroup="Target",
        opacity=0.5,
        text=sub["target_nb"],
        textposition="inside"
    )

# Barres Real
for level in levels:
    sub = df[df["data_skill_cat"] == level]
    fig.add_bar(
        name=f"Real - {level}",
        x=sub["team"],
        y=sub["real_ratio"],
        marker_color=color_map[level],
        offsetgroup=1,
        legendgroup="Real",
        text=sub["real_nb"],
        textposition="inside"
    )

# Ajout des totaux
for team, total in team_totals.items():
    fig.add_annotation(
        x=team, y=105,
        text=f"Total: {total}",
        showarrow=False,
        font=dict(size=12),
        xanchor="center"
    )

# Mise en forme finale
fig.update_layout(
    barmode="stack",
    title="Répartition des niveaux de compétence par équipe : Réel vs Cible",
    xaxis_title="Équipe",
    yaxis_title="Pourcentage (%)",
    yaxis=dict(range=[0, 110]),
    height=600
)

# Affichage
fig.show()