import pandas as pd
import plotly.graph_objects as go

# === Données ===
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

# === Ajout de la ligne "Beginner" par différence ===
def add_beginner(group):
    team = group["team"].iloc[0]
    t_sum = group["target_ratio"].sum()
    r_sum = group["real_ratio"].sum()
    return pd.concat([group, pd.DataFrame([{
        "team": team,
        "data_skill_cat": "Beginner",
        "target_ratio": max(0, 100 - t_sum),
        "real_ratio": max(0, 100 - r_sum)
    }])])

df = df.groupby("team", group_keys=False).apply(add_beginner)

# === Totaux par équipe ===
team_totals = {"CFM": 30, "GBI": 120, "GIS": 24, "IRB": 84, "RPI": 33}
df["total_nb"] = df["team"].map(team_totals)
df["target_nb"] = (df["target_ratio"] * df["total_nb"] / 100).round(1)
df["real_nb"] = (df["real_ratio"] * df["total_nb"] / 100).round(1)

# === Création du graphique ===
fig = go.Figure()
levels = ["Beginner", "Intermediate", "Confirmed"]
colors = {"Beginner": "red", "Intermediate": "pink", "Confirmed": "black"}

# Pour chaque niveau, on trace les barres target et real côte à côte
for level in levels:
    sub = df[df["data_skill_cat"] == level]
    
    fig.add_bar(
        name=f"Target - {level}",
        x=sub["team"],
        y=sub["target_ratio"],
        text=sub["target_nb"],
        textposition="inside",
        marker_color=colors[level],
        offsetgroup="target",
        base=0,
        legendgroup="Target",
        showlegend=(level == "Beginner")
    )
    
    fig.add_bar(
        name=f"Real - {level}",
        x=sub["team"],
        y=sub["real_ratio"],
        text=sub["real_nb"],
        textposition="inside",
        marker_color=colors[level],
        offsetgroup="real",
        base=0,
        legendgroup="Real",
        showlegend=(level == "Beginner")
    )

# === Totaux affichés au-dessus ===
for team in df["team"].unique():
    total = team_totals[team]
    fig.add_annotation(
        x=team, y=105, text=f"Total: {total}", showarrow=False,
        xanchor="center", yanchor="bottom", font=dict(size=12)
    )

# === Mise en page ===
fig.update_layout(
    barmode="stack",
    title="Répartition des niveaux par équipe : Réel vs Cible",
    xaxis_title="Équipe",
    yaxis_title="Pourcentage (%)",
    yaxis=dict(range=[0, 110]),
    height=600
)

fig.show()