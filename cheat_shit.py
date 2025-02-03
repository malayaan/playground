import fitz  # PyMuPDF pour lire le PDF
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pylibdmtx.pylibdmtx import decode as dmtx_decode
from PIL import Image
import io

def extract_images_from_pdf(pdf_path):
    """
    Extrait toutes les images d'un PDF et les retourne sous forme de liste PIL.Image.
    """
    images = []
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        for img in doc[page_num].get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_pil = Image.open(io.BytesIO(image_bytes))
            images.append(img_pil)
    
    return images

def decode_qr_codes(image):
    """
    Détecte et décode les QR Codes (y compris 2D-Doc) à partir d'une image.
    """
    decoded_data = []

    # Convertir l'image PIL en tableau NumPy pour OpenCV
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Scanner les codes QR et DataMatrix
    barcodes = decode(image_cv)  # Pyzbar (QR Code, Code 128, etc.)
    datamatrix_codes = dmtx_decode(image_cv)  # DataMatrix (2D-Doc)

    # Extraire les données des QR Codes détectés
    for barcode in barcodes:
        decoded_text = barcode.data.decode("utf-8")
        decoded_data.append(decoded_text)

    # Extraire les données des DataMatrix (2D-Doc)
    for dmtx_code in datamatrix_codes:
        decoded_text = dmtx_code.data.decode("utf-8")
        decoded_data.append(decoded_text)

    return decoded_data

def process_pdf(pdf_path):
    """
    Extrait et lit les QR Codes / 2D-Doc depuis un PDF.
    """
    images = extract_images_from_pdf(pdf_path)

    for i, img in enumerate(images):
        qr_data = decode_qr_codes(img)
        print(f"📄 Page {i+1}: {qr_data}" if qr_data else f"📄 Page {i+1}: Aucun QR Code détecté")

# 🔹 Exécuter le script avec un fichier PDF contenant des QR Codes 2D-Doc
pdf_file = "chemin/vers/votre_fichier.pdf"
process_pdf(pdf_file)