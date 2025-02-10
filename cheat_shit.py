import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

# Constantes physiques
GRAVITY = 0.02  # Gravité simulée
RESTITUTION = 0.8  # Coefficient de rebond
ROTATION_SPEED = np.pi / 180  # Vitesse de rotation (radians par frame)

# Définition de l'octogone
def create_octagon(radius=1.0):
    angles = np.linspace(0, 2 * np.pi, 9)[:-1]  # 8 côtés
    return np.array([radius * np.array([np.cos(a), np.sin(a)]) for a in angles])

# Vérifier si un point est à l'intérieur de l'octogone
def is_inside_octagon(point, octagon):
    from scipy.spatial import ConvexHull
    hull = ConvexHull(octagon)
    new_hull = ConvexHull(np.vstack((octagon, point)))
    return np.array_equal(hull.vertices, new_hull.vertices)

# Rotation d'un point autour du centre
def rotate_points(points, angle):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    return np.dot(points, rotation_matrix.T)

# Initialisation
octagon = create_octagon()
ball_pos = np.array([0.0, 0.0])  # La balle commence au centre
ball_velocity = np.array([0.03, 0.0])  # Vitesse initiale

# Création de la figure
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

# Dessin de l'octogone et de la balle
octagon_patch = plt.Polygon(octagon, closed=True, edgecolor='black', fill=False, linewidth=2)
ball_patch = plt.Circle(ball_pos, 0.05, color='red')

ax.add_patch(octagon_patch)
ax.add_patch(ball_patch)

# Animation
def update(frame):
    global octagon, ball_pos, ball_velocity

    # Rotation de l'octogone
    octagon = rotate_points(octagon, ROTATION_SPEED)
    octagon_patch.set_xy(octagon)

    # Appliquer la gravité
    ball_velocity[1] -= GRAVITY

    # Déplacer la balle
    ball_pos += ball_velocity

    # Vérification des collisions
    for i in range(len(octagon)):
        p1, p2 = octagon[i], octagon[(i + 1) % len(octagon)]
        edge_vector = p2 - p1
        edge_normal = np.array([-edge_vector[1], edge_vector[0]])  # Normale perpendiculaire
        edge_normal /= np.linalg.norm(edge_normal)  # Normalisation
        
        # Projection sur la normale
        ball_to_edge = ball_pos - p1
        distance_to_edge = np.dot(ball_to_edge, edge_normal)
        
        if distance_to_edge < 0.05:  # Collision détectée
            ball_pos -= ball_velocity  # Revenir en arrière
            ball_velocity -= 2 * np.dot(ball_velocity, edge_normal) * edge_normal  # Réflexion
            ball_velocity *= RESTITUTION  # Perte d'énergie au rebond
            break  # Éviter plusieurs rebonds simultanés

    # Mise à jour de la balle
    ball_patch.set_center(ball_pos)

    return octagon_patch, ball_patch

ani = animation.FuncAnimation(fig, update, frames=500, interval=10, blit=False)
plt.show()