import plotly.graph_objects as go

# ------------------------------------------------------
# 1) Définir les montants et calculer le "reste cumulé"
# ------------------------------------------------------

# Entrées
salaire = 2756
copine = 465
ticket_restaurant = 110  # flux direct vers "Bouffe"

# Sorties depuis le compte courant (hors reste cumulé)
cc_to_av = 1300        # Assurance Vie
cc_to_livret = 340   # Livret A
cc_to_pea = 0          # PEA
cc_to_bouffe = 90     # Bouffe
cc_to_loisir = 500  # Loisir
cc_to_loyer = 910      # Loyer
cc_to_charges = 30+7+9 # Charges fixes (EDF, Internet, etc.)

# Calcul de la somme des entrées du compte courant
cc_input = salaire + copine  # Ticket Restaurant ne passe pas par le CC

# Calcul de la somme des sorties (sauf "reste cumulé")
cc_output_except_reste = (
    cc_to_av
    + cc_to_livret
    + cc_to_pea
    + cc_to_bouffe
    + cc_to_loisir
    + cc_to_loyer
    + cc_to_charges
)

# Reste cumulé = Entrées CC - Sorties CC
reste_cumule = cc_input - cc_output_except_reste

# ------------------------------------------------------
# 2) Créer les labels du Sankey
# ------------------------------------------------------
labels = [
    "Salaire",               # 0
    "Participation Copine",  # 1
    "Ticket Restaurant",     # 2
    "Compte Courant",        # 3
    "Assurance Vie",         # 4
    "Livret A",              # 5
    "PEA",                   # 6
    "Bouffe",       # 7
    "Loisir",             # 8
    "Loyer",                 # 9
    "Charges fixes",         # 10
    "Reste cumulé"           # 11
]

# ------------------------------------------------------
# 3) Définir les flux (source -> target) et leur valeur
# ------------------------------------------------------
sources = [
    0,  # Salaire           -> Compte Courant
    1,  # Copine            -> Compte Courant
    2,  # Ticket Restaurant -> Bouffe (flux direct hors CC)

    3,  # Compte Courant -> Assurance Vie
    3,  # Compte Courant -> Livret A
    3,  # Compte Courant -> PEA
    3,  # Compte Courant -> Bouffe
    3,  # Compte Courant -> Loisir
    3,  # Compte Courant -> Loyer
    3,  # Compte Courant -> Charges fixes
    3,  # Compte Courant -> Reste cumulé
]

targets = [
    3,  # Salaire           -> CC
    3,  # Copine            -> CC
    7,  # Ticket Restaurant -> Bouffe

    4,  # CC -> Assurance Vie
    5,  # CC -> Livret A
    6,  # CC -> PEA
    7,  # CC -> Bouffe
    8,  # CC -> Loisir
    9,  # CC -> Loyer
    10, # CC -> Charges fixes
    11  # CC -> Reste cumulé
]

values = [
    salaire,
    copine,
    ticket_restaurant,

    cc_to_av,
    cc_to_livret,
    cc_to_pea,
    cc_to_bouffe,
    cc_to_loisir,
    cc_to_loyer,
    cc_to_charges,
    reste_cumule
]

# ------------------------------------------------------
# 4) Construire et afficher le Sankey
# ------------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])

fig.update_layout(
    title_text="Flux des dépenses (avec reste cumulé dynamique)",
    font_size=14
)

fig.show()
