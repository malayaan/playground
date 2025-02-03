import fitz  # PyMuPDF pour lire le PDF
import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image
import io
import pytesseract

def extract_first_page_image(pdf_path):
    """
    Extrait l'image de la première page du PDF.
    """
    doc = fitz.open(pdf_path)  # Ouvrir le PDF
    page = doc[0]  # Première page

    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        img_pil = Image.open(io.BytesIO(image_bytes))
        return img_pil  # Retourne la première image trouvée

    return None

def detect_qr_codes(image):
    """
    Détecte les QR Codes / DataMatrix dans une image et retourne leurs positions et contenus.
    """
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Appliquer un prétraitement pour améliorer la détection
    _, image_bin = cv2.threshold(image_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Détecter les QR Codes / DataMatrix
    qr_codes = pyzbar_decode(image_bin)
    datamatrix_codes = decode(image_bin)

    qr_list = []
    
    # Ajouter les QR Codes détectés
    for qr in qr_codes:
        qr_list.append({
            "type": "QR",
            "data": qr.data.decode("utf-8"),
            "position": qr.rect
        })
    
    # Ajouter les DataMatrix détectés
    for dm in datamatrix_codes:
        qr_list.append({
            "type": "DataMatrix",
            "data": dm.data.decode("utf-8"),
            "position": None  # Pas toujours dispo avec pylibdmtx
        })

    return qr_list

def detect_text_below_qr(image, qr_position):
    """
    Vérifie si le texte "2D-Doc" est écrit sous un QR Code donné.
    """
    x, y, w, h = qr_position.left, qr_position.top, qr_position.width, qr_position.height
    roi = np.array(image)[y + h : y + h + 40, x : x + w]  # Zone sous le QR Code
    
    # Extraire le texte avec OCR
    text = pytesseract.image_to_string(roi, config="--psm 6").strip()
    
    return "2D-Doc" in text

def process_pdf(pdf_path):
    """
    Extrait le premier QR Code valide d'un PDF (avec "2D-Doc" en dessous).
    """
    image = extract_first_page_image(pdf_path)

    if image is None:
        print("⚠️ Aucun QR Code détecté sur la première page.")
        return

    qr_codes = detect_qr_codes(image)

    for qr in qr_codes:
        if qr["position"]:  # Vérifie que la position est disponible (QR Codes)
            if detect_text_below_qr(image, qr["position"]):
                print(f"✅ QR Code 2D-Doc détecté : {qr['data']}")
                return qr["data"]

    print("⚠️ Aucun QR Code 2D-Doc trouvé.")

# 📌 Exécution avec un fichier PDF contenant un QR Code 2D-Doc
pdf_file = "chemin/vers/votre_fichier.pdf"
process_pdf(pdf_file)