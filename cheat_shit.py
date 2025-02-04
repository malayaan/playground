import cv2
import numpy as np
from pdf2image import convert_from_path
from pylibdmtx.pylibdmtx import decode
from PIL import Image

def extract_first_page_as_image(pdf_path, dpi=300):
    """
    Convertit UNIQUEMENT la première page du PDF en image haute résolution.
    """
    print("🔹 Extraction de la première page du PDF...")
    images = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=1)
    
    if not images:
        print("❌ ERREUR : Impossible d'extraire une image du PDF.")
        return None

    print("✅ Première page extraite avec succès.")
    return images[0]  # Retourne l’image de la première page

def read_2ddoc_from_pdf(pdf_path):
    """
    Extrait un 2D-Doc depuis la première page d'un PDF et le lit.
    """
    print("\n🔹 Début du scan du 2D-Doc à partir du PDF...")

    # Extraire la première page sous forme d’image
    image_pil = extract_first_page_as_image(pdf_path)

    if image_pil is None:
        print("❌ Impossible d'extraire l’image depuis le PDF.")
        return None

    # Convertir en niveaux de gris pour traitement
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2GRAY)

    # Appliquer une binarisation stricte (Noir et Blanc)
    print("🔹 Conversion en noir et blanc...")
    _, image_bin = cv2.threshold(image_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scanner le DataMatrix (2D-Doc)
    print("🔹 Détection du 2D-Doc en cours...")
    decoded_data = decode(image_bin)

    if not decoded_data:
        print("❌ AUCUN 2D-Doc détecté après extraction depuis le PDF.")
        return None

    # Extraction des données
    qr_text = decoded_data[0].data.decode("utf-8")
    print("\n📄 **Données extraites du 2D-Doc :**\n")
    print(qr_text)

    return qr_text

# 📌 Exécuter avec votre fichier PDF
pdf_path = "chemin/vers/mon_fichier.pdf"  # Remplacez par le chemin du PDF
read_2ddoc_from_pdf(pdf_path)