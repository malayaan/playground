import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import matplotlib.pyplot as plt

def preprocess_image(image_path):
    """
    Améliore l'image pour maximiser la lisibilité du 2D-Doc.
    """
    print("🔹 Chargement de l'image...")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("❌ ERREUR : Impossible de charger l'image.")
        return None

    print("✅ Image chargée.")

    # Augmenter le contraste
    print("🔹 Augmentation du contraste...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    image = clahe.apply(image)

    # Binarisation stricte
    print("🔹 Conversion en noir et blanc...")
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Redimensionner (x2)
    print("🔹 Redimensionnement x2...")
    image_resized = cv2.resize(image_bin, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # Afficher l’image prétraitée
    plt.figure(figsize=(6, 6))
    plt.imshow(image_resized, cmap="gray")
    plt.title("Image prétraitée du 2D-Doc")
    plt.axis("off")
    plt.show()

    return image_resized

def read_2ddoc(image_path):
    """
    Détecte un DataMatrix 2D-Doc en utilisant pylibdmtx.
    """
    print("\n🔹 Début du scan du 2D-Doc...")

    # Prétraitement
    processed_image = preprocess_image(image_path)

    if processed_image is None:
        print("❌ Impossible de prétraiter l’image.")
        return None

    # Scanner avec pylibdmtx
    print("🔹 Détection du 2D-Doc en cours...")
    decoded_data = decode(processed_image)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté après prétraitement.")
        return None

    # Extraction des données
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Exécuter avec votre image
image_path = "chemin/vers/image_du_2d_doc.png"  # Remplacez par votre fichier
read_2ddoc(image_path)