import fitz  # PyMuPDF pour extraire les pages du PDF
import cv2
import numpy as np
from pdf2image import convert_from_path
from pylibdmtx.pylibdmtx import decode
from PIL import Image

def extract_first_page_as_image(pdf_path, dpi=300):
    """
    Convertit la première page du PDF en image haute résolution.
    """
    print("🔹 Extraction de la première page du PDF...")
    images = convert_from_path(pdf_path, dpi=dpi)
    
    if not images:
        print("❌ ERREUR : Impossible d'extraire une image du PDF.")
        return None

    print("✅ Image extraite avec succès.")
    return images[0]

def read_2ddoc_from_pdf(pdf_path):
    """
    Extrait un 2D-Doc depuis un PDF et le lit.
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

# 📌 Test du script avec votre fichier PDF
pdf_path = "chemin/vers/mon_fichier.pdf"  # Remplacez par votre fichier
read_2ddoc_from_pdf(pdf_path)