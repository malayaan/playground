import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from PIL import Image

def read_2ddoc(image_path):
    """
    Lit et extrait les données d'un QR Code 2D-Doc à partir d'une image.
    """
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Améliorer la qualité du scan
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scanner le DataMatrix (2D-Doc)
    decoded_data = decode(image_bin)

    if not decoded_data:
        print("⚠️ Aucun 2D-Doc détecté dans l'image.")
        return None

    # Extraction des données sous forme de texte
    qr_text = decoded_data[0].data.decode("utf-8")
    print(f"📄 Données brutes du 2D-Doc : {qr_text}")

    return qr_text

# 📌 Test du script avec une image contenant un code 2D-Doc
image_path = "chemin/vers/image_du_2d_doc.png"
read_2ddoc(image_path)