import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

def read_2ddoc_zxing(image_path):
    """
    Détecte un DataMatrix 2D-Doc en utilisant ZXing (pyzbar).
    """
    print("\n🔹 Début du scan avec ZXing...")

    # Charger l'image en niveaux de gris
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("❌ ERREUR : Impossible de charger l'image.")
        return None

    # Appliquer une binarisation stricte (Noir et Blanc)
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convertir en format PIL pour pyzbar
    processed_image_pil = Image.fromarray(image_bin)

    # Scanner avec pyzbar (ZXing)
    print("🔹 Détection du 2D-Doc en cours avec ZXing...")
    decoded_data = decode(processed_image_pil)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté après prétraitement avec ZXing.")
        return None

    # Extraction des données
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Exécuter avec votre image
image_path = "data/Capture.JPG"  # Remplacez par le bon chemin
read_2ddoc_zxing(image_path)