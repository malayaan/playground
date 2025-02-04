import fitz  # PyMuPDF
import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode

def extract_first_page_as_image(pdf_path, output_image="page1.png"):
    """
    Extrait la première page d'un PDF et la sauvegarde comme image.
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

def read_2ddoc_from_image(image_path):
    """
    Détecte et lit un 2D-Doc dans une image.
    """
    print("🔹 Lecture du 2D-Doc à partir de l'image...")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("❌ Impossible de charger l'image.")
        return None

    # Prétraitement pour améliorer la lisibilité
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scanner le DataMatrix (2D-Doc)
    decoded_data = decode(image_bin)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté dans l'image.")
        return None

    # Extraire les données
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Test du script avec un PDF
pdf_path = "chemin/vers/mon_fichier.pdf"  # Remplacez par le chemin de votre PDF
image_path = extract_first_page_as_image(pdf_path)

if image_path:
    read_2ddoc_from_image(image_path)