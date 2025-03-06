import os
import cv2
import pytesseract
import pdfium
import pandas as pd
from pdfminer.high_level import extract_text
from PIL import Image
import numpy as np

# Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Paths
PDF_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\part_ged"
IMG_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\GED_Images"

os.makedirs(IMG_FOLDER, exist_ok=True)

def detect_pdf_type(pdf_path):
    """ Detects if a PDF is native (text-based) or scanned (image-based). """
    text = extract_text(pdf_path).strip()
    return "native_pdf" if len(text) > 30 else "scanned_pdf"

def preprocess_image(image):
    """ Enhances scanned images for better OCR accuracy. """
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def extract_text_from_pdfs(pdf_folder, img_folder):
    results = []
    
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_type = detect_pdf_type(pdf_path)

            if pdf_type == "native_pdf":
                text = extract_text(pdf_path).strip()
                results.append({"file": pdf_file, "page": None, "text": text, "quality_flag": pdf_type})

            else:  # Process scanned PDFs
                pdf = pdfium.PdfDocument(pdf_path)
                
                for i in range(len(pdf)):
                    img = pdf[i].render().to_pil()
                    img_path = os.path.join(img_folder, f"{os.path.splitext(pdf_file)[0]}_{i}.jpg")
                    img.save(img_path, "JPEG")

                    processed_img = preprocess_image(img)
                    text = pytesseract.image_to_string(processed_img, lang="fra").strip()

                    results.append({"file": pdf_file, "page": i, "text": text, "quality_flag": pdf_type})
    
    return pd.DataFrame(results)

df_text = extract_text_from_pdfs(PDF_FOLDER, IMG_FOLDER)
df_text.to_csv("extracted_text.csv", index=False)

print(df_text.head())