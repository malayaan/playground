import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from twoddoc import TwoDDoc

def read_2ddoc_from_image(image_path):
    """
    Lit et analyse un QR Code 2D-Doc depuis une image.
    """
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Améliorer l'image pour une meilleure détection
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Décoder le DataMatrix (QR Code 2D-Doc)
    decoded_data = decode(image_bin)
    
    if not decoded_data:
        print("⚠️ Aucun QR Code 2D-Doc détecté dans l'image.")
        return
    
    # Extraction des données
    qr_text = decoded_data[0].data.decode("utf-8")
    print(f"📄 Données brutes du 2D-Doc : {qr_text}")

    # Analyse du contenu avec la bibliothèque 2D-Doc
    try:
        twoddoc = TwoDDoc(qr_text)
        print("\n✅ Informations extraites du 2D-Doc :")
        for key, value in twoddoc.data.items():
            print(f"🔹 {key}: {value}")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'analyse du 2D-Doc : {e}")

# 📌 Exécuter le script avec votre image de QR Code 2D-Doc
image_path = "chemin/vers/l_image_qr_code.png"
read_2ddoc_from_image(image_path)