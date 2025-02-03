import fitz  # PyMuPDF
from pdf2image import convert_from_path
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

def extract_qr_code_from_pdf(pdf_path, output_image_path="qrcode.png"):
    # Convertir la première page du PDF en image
    images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=300)

    if not images:
        print("Erreur : Impossible de convertir le PDF en image.")
        return None

    # Sauvegarder l'image pour analyse
    image = images[0]
    image.save(output_image_path, "PNG")

    # Charger l'image avec OpenCV
    img_cv = cv2.imread(output_image_path)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Détection du QR Code
    decoded_objects = decode(gray)

    if not decoded_objects:
        print("Aucun QR Code détecté.")
        return None

    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        print("Contenu du QR Code :", qr_data)
        return qr_data

    return None

# Exemple d'utilisation
pdf_file = "avis_impot.pdf"  # Remplacez par votre fichier PDF
qr_content = extract_qr_code_from_pdf(pdf_file)

if qr_content:
    print("QR Code extrait avec succès :", qr_content)
else:
    print("Aucun QR Code trouvé.")