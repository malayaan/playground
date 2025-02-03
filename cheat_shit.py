import fitz  # PyMuPDF pour lire directement le PDF
import pytesseract
import cv2
import numpy as np
from pyzbar.pyzbar import decode as pyzbar_decode
from pylibdmtx.pylibdmtx import decode as dmtx_decode
from PIL import Image
import io

def extract_qr_code_from_pdf(pdf_path):
    """
    Extrait les QR Codes directement du PDF sans conversion en image.
    """
    doc = fitz.open(pdf_path)  # Ouvrir le PDF
    page = doc[0]  # Prendre la première page

    # Extraire uniquement les objets images (codes-barres)
    qr_images = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        img_pil = Image.open(io.BytesIO(base_image["image"]))
        qr_images.append((img_pil, base_image["bbox"]))  # Ajouter image + position bbox

    return qr_images

def detect_text_below_qr(image, bbox):
    """
    Vérifie si le texte "2D-Doc" est écrit sous un QR Code donné.
    """
    x0, y0, x1, y1 = bbox  # Coordonnées du QR Code
    roi = image.crop((x0, y1, x1, y1 + 50))  # Zone sous le QR Code

    # OCR pour détecter "2D-Doc"
    text = pytesseract.image_to_string(roi, config="--psm 6").strip()

    return "2D-Doc" in text

def decode_qr(image):
    """
    Décode un QR Code ou DataMatrix dans une image.
    """
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, image_bin = cv2.threshold(image_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Essayer QR Code
    qr_codes = pyzbar_decode(image_bin)
    for qr in qr_codes:
        return qr.data.decode("utf-8")

    # Essayer DataMatrix (cas du 2D-Doc)
    dm_codes = dmtx_decode(image_bin)
    for dm in dm_codes:
        return dm.data.decode("utf-8")

    return None

def process_pdf(pdf_path):
    """
    Extrait le premier QR Code valide d'un PDF (avec "2D-Doc" en dessous).
    """
    qr_codes = extract_qr_code_from_pdf(pdf_path)

    if not qr_codes:
        print("⚠️ Aucun QR Code trouvé sur la première page.")
        return

    for img, bbox in qr_codes:
        qr_data = decode_qr(img)
        if qr_data:
            if detect_text_below_qr(img, bbox):
                print(f"✅ QR Code 2D-Doc détecté : {qr_data}")
                return qr_data

    print("⚠️ Aucun QR Code 2D-Doc trouvé.")

# 📌 Exécution avec un fichier PDF contenant un QR Code 2D-Doc
pdf_file = "chemin/vers/votre_fichier.pdf"
process_pdf(pdf_file)