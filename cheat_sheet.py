import matplotlib.pyplot as plt
import networkx as nx
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# Liste des groupes et de leurs marques
brands_by_group = {
    'Toyota': ['Toyota', 'Lexus', 'Daihatsu'],
    'Ford': ['Ford', 'Lincoln'],
    'Daimler': ['Mercedes-Benz', 'Smart'],
    'FCA': ['Maserati', 'Fiat', 'Lancia', 'Alfa Romeo', 'Dodge', 'Ram', 'Jeep', 'Chrysler'],
    'Nissan': ['Nissan', 'Infiniti', 'Datsun'],
    'Honda': ['Honda', 'Acura'],
    'PSA': ['Peugeot', 'Citroën', 'DS Automobiles', 'Opel', 'Vauxhall'],
    'BMW Group': ['BMW', 'Mini', 'Rolls-Royce'],
    'Tata': ['Tata Motors', 'Jaguar', 'Land Rover'],
    'Renault': ['Renault', 'Dacia', 'Samsung'],
    'GM': ['Chevrolet', 'Cadillac', 'GMC', 'Buick', 'Wuling Motors', 'Baojun', 'Holden'],
    'Hyundai': ['Hyundai', 'Kia'],
    'Volkswagen': ['Volkswagen', 'Audi', 'Porsche', 'Lamborghini', 'Bugatti', 'Bentley', 'Skoda', 'Seat'],
    'Geely': ['Volvo', 'The London Taxi Company']
}

# Création du graphe
G = nx.Graph()

for group, brands in brands_by_group.items():
    for brand in brands:
        G.add_edge(group, brand)

# Position des nœuds
pos = nx.spring_layout(G, k=1.8, seed=42)

# Tracé des arêtes
plt.figure(figsize=(18, 18))
nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.5)

# Fonction pour charger l'image si elle existe
def get_image(path, zoom=0.08):
    if os.path.exists(path):
        img = mpimg.imread(path)
        return OffsetImage(img, zoom=zoom)
    else:
        return None

# Placer logos ou texte
ax = plt.gca()

for node, (x, y) in pos.items():
    # préparer le nom du fichier
    filename = node.lower().replace(" ", "").replace("-", "") + ".png"
    filepath = os.path.join("images", filename)

    imagebox = get_image(filepath)
    if imagebox:
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)
    else:
        # Afficher nom si logo non trouvé
        plt.text(x, y, node, fontsize=8, ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.3', fc='lightgrey', ec='black', lw=0.5))

plt.title("14 Car Companies Control a Combined 54 Brands", fontsize=16, weight='bold')
plt.axis('off')
plt.show()