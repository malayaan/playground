import os
import cv2
import pytesseract
import pdfium
import pandas as pd
from PIL import Image

# Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Paths
PDF_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\part_ged"
IMG_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\GED_Images"

os.makedirs(IMG_FOLDER, exist_ok=True)

def extract_text_from_pdfs(pdf_folder, img_folder):
    results = []
    
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf = pdfium.PdfDocument(pdf_path)
            
            for i in range(len(pdf)):
                img = pdf[i].render().to_pil()
                img_path = os.path.join(img_folder, f"{os.path.splitext(pdf_file)[0]}_{i}.jpg")
                img.save(img_path, "JPEG")

                gray = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, lang="fra")

                results.append({"file": pdf_file, "text": text})
    
    return pd.DataFrame(results)

df_text = extract_text_from_pdfs(PDF_FOLDER, IMG_FOLDER)
df_text.to_csv("extracted_text.csv", index=False)

print(df_text.head())