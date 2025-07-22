fig.update_layout(
    title="Skill Level Distribution",
    xaxis=dict(
        title="Team",
        tickvals=df["audit_team_l3"].unique(),
        ticktext=df["X_labels"],
        showline=True,
        linewidth=1,
        zeroline=False,
        font=dict(weight='bold')  # Ajoutez cette ligne pour mettre les labels X en gras
    ),
    yaxis=dict(
        title="Percentage (%)",
        range=[0, 110],
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
    ),
    height=600,
    barmode="group",  # Vous pouvez aussi ajouter la couleur de fond ici
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)