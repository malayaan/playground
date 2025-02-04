import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from PIL import Image

def preprocess_image(image_path):
    """
    Applique des améliorations sur l'image pour optimiser la détection du 2D-Doc.
    """
    print("🔹 Chargement de l'image...")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print("❌ ERREUR : Impossible de charger l'image. Vérifiez le chemin.")
        return None

    print("✅ Image chargée avec succès.")

    # Augmenter le contraste (améliorer les bords du DataMatrix)
    print("🔹 Augmentation du contraste...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    image = clahe.apply(image)
    print("✅ Contraste amélioré.")

    # Appliquer une binarisation stricte (Noir et Blanc)
    print("🔹 Conversion en noir et blanc...")
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("✅ Image binarisée.")

    # Redimensionner l’image pour améliorer la lisibilité (x2)
    print("🔹 Redimensionnement de l’image...")
    image_resized = cv2.resize(image_bin, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    print("✅ Image redimensionnée.")

    return image_resized

def read_2ddoc(image_path):
    """
    Détecte et extrait les données d'un QR Code 2D-Doc (DataMatrix).
    """
    print("\n🔹 Début du processus de lecture du 2D-Doc...")

    # Appliquer le prétraitement
    processed_image = preprocess_image(image_path)

    if processed_image is None:
        print("❌ ERREUR : Le prétraitement a échoué.")
        return None

    print("✅ Prétraitement terminé.")

    # Scanner le DataMatrix (2D-Doc)
    print("🔹 Détection du 2D-Doc en cours...")
    decoded_data = decode(processed_image)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté après le prétraitement.")
        return None

    # Extraction des données sous forme de texte
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Test du script avec votre image
image_path = "chemin/vers/image_du_2d_doc.png"  # Remplacez par votre chemin de fichier
read_2ddoc(image_path)
