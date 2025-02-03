import fitz  # PyMuPDF pour manipuler le PDF
import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from PIL import Image

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

def detect_and_crop_2ddoc(image):
    """
    Détecte un 2D-Doc (DataMatrix) dans l’image et l’extrait.
    """
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Appliquer un filtre pour améliorer la détection
    _, image_bin = cv2.threshold(image_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scanner les DataMatrix (2D-Doc)
    detected_dmtx = decode(image_bin)

    if not detected_dmtx:
        print("⚠️ Aucun 2D-Doc détecté.")
        return None

    # On prend le premier 2D-Doc détecté
    dmtx = detected_dmtx[0]
    x, y, w, h = dmtx.rect

    # Extraction de la région du 2D-Doc
    dmtx_crop = image.crop((x, y, x + w, y + h))

    return dmtx_crop

def process_pdf(pdf_path, output_image_path):
    """
    Convertit la première page du PDF en image, détecte et extrait le 2D-Doc, puis l'enregistre.
    """
    image = extract_first_page_as_image(pdf_path)

    if image is None:
        print("⚠️ Impossible de récupérer la première page du PDF.")
        return

    dmtx_image = detect_and_crop_2ddoc(image)

    if dmtx_image is not None:
        dmtx_image.save(output_image_path, "PNG")
        print(f"✅ 2D-Doc extrait et enregistré sous {output_image_path}")
    else:
        print("⚠️ Aucun 2D-Doc trouvé.")

# 📌 Exécution avec un fichier PDF contenant un 2D-Doc
pdf_file = "chemin/vers/votre_fichier.pdf"
output_png = "extracted_2ddoc.png"

process_pdf(pdf_file, output_png)