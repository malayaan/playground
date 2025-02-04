import fitz  # PyMuPDF
import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode

def extract_first_page_as_image(pdf_path, output_image="page1.png"):
    """
    Extrait la première page du PDF et la sauvegarde comme image.
    """
    print("🔹 Extraction de la première page du PDF avec PyMuPDF...")
    try:
        # Ouvrir le PDF
        pdf_document = fitz.open(pdf_path)
        # Récupérer la première page
        page = pdf_document[0]
        # Convertir la page en image (300 DPI)
        pix = page.get_pixmap(dpi=300)
        # Sauvegarder l'image
        pix.save(output_image)
        print(f"✅ Première page extraite et sauvegardée sous {output_image}.")
        return output_image
    except Exception as e:
        print(f"❌ ERREUR : {e}")
        return None

def crop_qr_code_zone(image_path, crop_x=50, crop_y=50, crop_width=300, crop_height=300):
    """
    Recadre uniquement la zone du 2D-Doc (QR Code) en haut à gauche.
    Ajustez les coordonnées selon la position exacte.
    """
    print("🔹 Recadrage de la zone contenant le 2D-Doc...")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("❌ Impossible de charger l'image.")
        return None

    # Définir la région où se trouve le 2D-Doc (ajustez les valeurs si nécessaire)
    qr_code_region = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

    # Sauvegarder pour vérifier visuellement
    cropped_image_path = "cropped_qrcode.png"
    cv2.imwrite(cropped_image_path, qr_code_region)
    print(f"✅ Zone du 2D-Doc extraite et sauvegardée sous {cropped_image_path}.")

    return cropped_image_path

def read_2ddoc_from_image(image_path):
    """
    Détecte et lit un 2D-Doc dans une image recadrée.
    """
    print("🔹 Lecture du 2D-Doc à partir de l'image...")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("❌ Impossible de charger l'image.")
        return None

    # Appliquer un prétraitement pour améliorer la lisibilité
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scanner le DataMatrix (2D-Doc)
    print("🔹 Détection du 2D-Doc en cours...")
    decoded_data = decode(image_bin)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté dans l'image.")
        return None

    # Extraire les données
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Exécuter avec votre PDF
pdf_path = "chemin/vers/mon_fichier.pdf"  # Remplacez par le chemin de votre PDF
full_image_path = extract_first_page_as_image(pdf_path)

if full_image_path:
    cropped_image_path = crop_qr_code_zone(full_image_path, crop_x=50, crop_y=50, crop_width=300, crop_height=300)
    if cropped_image_path:
        read_2ddoc_from_image(cropped_image_path)