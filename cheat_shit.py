import plotly.graph_objects as go

def plot_gauge(current_value, target_value, label):
    """
    Plots a simplified gauge chart with 4 segments (red, orange, yellow, green),
    adds a text annotation below the gauge and an annotation above the gauge.
    """

    plot_bgcolor = "white"
    text_color = "#000000"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=current_value,
            title={"text": label, "font": {"color": text_color}},
            gauge={
                "axis": {"range": [0, target_value], "tickcolor": text_color, "showticklabels": False},
                "bar": {"color": "black"},  # Needle color
                "steps": [
                    {"range": [0, target_value * 0.25], "color": "#f25829"},  # Red
                    {"range": [target_value * 0.25, target_value * 0.5], "color": "#f2a529"},  # Orange
                    {"range": [target_value * 0.5, target_value * 0.75], "color": "#f2e541"},  # Yellow
                    {"range": [target_value * 0.75, target_value], "color": "#33cc33"},  # Green
                ],
            },
            number={"font": {"color": text_color}},
        )
    )

    # Ajouter un rectangle blanc arrondi en fond
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                fillcolor="white",
                line=dict(color="white"),
                layer="below",
                # Pour arrondir les bords, utiliser 'path' serait plus précis, mais Plotly ne supporte pas directement.
                # Une astuce simple : définir un rectangle blanc derrière (sinon on peut jouer avec CSS dans l'app).
            )
        ],
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=plot_bgcolor,
        font={"color": text_color},
    )

    # Ajouter annotation sous la jauge
    annotation_text = (
        f"<b>{current_value}</b> personnes avec le niveau <b>{label}</b> "
        f"pour une target à <b>{target_value}</b>"
    )
    fig.update_layout(
        annotations=[
            dict(
                x=0.5,
                y=-0.2,
                text=annotation_text,
                showarrow=False,
                font=dict(size=14, color=text_color),
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
            ),
            # Annotation au-dessus de la jauge avec texte en anglais demandé
            dict(
                x=0.5,
                y=1.15,
                text=f"{current_value} at the Skill {label} over a target of {target_value}",
                showarrow=False,
                font=dict(size=14, color=text_color),
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
            ),
        ]
    )

    # Afficher la figure avec Streamlit
    import streamlit as st
    st.plotly_chart(fig, use_container_width=True)