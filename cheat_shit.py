import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

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

    # Appliquer un filtre de contraste
    print("🔹 Augmentation du contraste...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    image = clahe.apply(image)

    # Convertir en noir et blanc strict
    print("🔹 Binarisation stricte...")
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Redimensionner (x2)
    print("🔹 Redimensionnement x2 pour améliorer la reconnaissance...")
    image_resized = cv2.resize(image_bin, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    return image_resized

def read_2ddoc_zxing(image_path):
    """
    Détecte un DataMatrix 2D-Doc en utilisant ZXing (pyzbar).
    """
    print("\n🔹 Début du scan avec ZXing...")

    # Prétraitement
    processed_image = preprocess_image(image_path)

    if processed_image is None:
        print("❌ Impossible de prétraiter l’image.")
        return None

    # Convertir en format compatible avec pyzbar
    processed_image_pil = Image.fromarray(processed_image)

    # Scanner avec pyzbar
    print("🔹 Détection du 2D-Doc en cours...")
    decoded_data = decode(processed_image_pil)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté après le prétraitement avec ZXing.")
        return None

    # Extraction des données
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Test avec votre image
image_path = "chemin/vers/image_du_2d_doc.png"  # Remplacez par votre fichier
read_2ddoc_zxing(image_path)