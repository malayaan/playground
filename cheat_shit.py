import os
import cv2
import pytesseract
import pdf2image
import pandas as pd
from PIL import Image

# Set Tesseract path (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define paths
PDF_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\part_ged"
IMG_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\GED_Images"

# Ensure image folder exists
os.makedirs(IMG_FOLDER, exist_ok=True)

# Convert PDF to images and perform OCR
def extract_text_from_pdfs(pdf_folder, img_folder):
    results = []
    
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            images = pdf2image.convert_from_path(pdf_path, dpi=300)

            for i, image in enumerate(images):
                img_path = os.path.join(img_folder, f"{os.path.splitext(pdf_file)[0]}_{i}.jpg")
                image.save(img_path, "JPEG")
                
                # Convert to grayscale for better OCR
                gray = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, lang="fra")
                
                results.append({"file": pdf_file, "text": text})
    
    return pd.DataFrame(results)

# Run OCR extraction
df_text = extract_text_from_pdfs(PDF_FOLDER, IMG_FOLDER)

# Save results
df_text.to_csv("extracted_text.csv", index=False)

# Display first few results
print(df_text.head())