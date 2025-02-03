import fitz  # PyMuPDF pour lire le PDF
import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import pytesseract

def extract_first_page_as_image(pdf_path, dpi=300):
    """
    Convertit la première page du PDF en image haute résolution.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]  # Première page

    # Rendu en image (pixmap haute résolution)
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    return img_pil

def find_2ddoc_location(image):
    """
    Localise le texte '2D-Doc' dans l'image avec OCR et retourne ses coordonnées.
    """
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # OCR pour trouver "2D-Doc"
    data = pytesseract.image_to_data(image_cv, config="--psm 6", output_type=pytesseract.Output.DICT)

    for i, text in enumerate(data["text"]):
        if "2D-Doc" in text:
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            print(f"✅ Localisation de '2D-Doc' détectée à : X={x}, Y={y}, W={w}, H={h}")
            return x, y, w, h

    print("⚠️ Texte '2D-Doc' non trouvé.")
    return None

def detect_and_crop_2ddoc(image, bbox):
    """
    Détecte un DataMatrix (2D-Doc) autour de la position trouvée par OCR.
    """
    if bbox is None:
        print("⚠️ Impossible de détecter la zone du 2D-Doc.")
        return None

    x, y, w, h = bbox

    # Définir une région légèrement au-dessus pour capturer le QR Code
    roi_x, roi_y, roi_w, roi_h = x - 50, y - 100, w + 100, h + 120
    roi_x, roi_y = max(0, roi_x), max(0, roi_y)  # Éviter les valeurs négatives

    # Extraire la zone autour du QR Code
    roi = np.array(image)[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    roi_pil = Image.fromarray(roi)

    # Scanner le QR Code uniquement dans cette région
    detected_dmtx = decode(roi)
    if not detected_dmtx:
        print("⚠️ Aucun QR Code 2D-Doc détecté dans la zone ciblée.")
        return None

    # Extraction du QR Code
    dmtx = detected_dmtx[0]
    qr_x, qr_y, qr_w, qr_h = dmtx.rect
    qr_crop = roi_pil.crop((qr_x, qr_y, qr_x + qr_w, qr_y + qr_h))

    return qr_crop

def process_pdf(pdf_path, output_image_path):
    """
    Convertit la première page en image, détecte la zone '2D-Doc' avec OCR,
    puis extrait le QR Code associé et l'enregistre.
    """
    image = extract_first_page_as_image(pdf_path)

    if image is None:
        print("⚠️ Impossible de récupérer la première page du PDF.")
        return

    # Trouver la position du texte '2D-Doc'
    bbox = find_2ddoc_location(image)

    # Extraire le QR Code autour de cette zone
    dmtx_image = detect_and_crop_2ddoc(image, bbox)

    if dmtx_image is not None:
        dmtx_image.save(output_image_path, "PNG")
        print(f"✅ 2D-Doc extrait et enregistré sous {output_image_path}")
    else:
        print("⚠️ Aucun 2D-Doc trouvé.")

# 📌 Exécution avec un fichier PDF contenant un 2D-Doc
pdf_file = "chemin/vers/votre_fichier.pdf"
output_png = "extracted_2ddoc.png"

process_pdf(pdf_file, output_png)