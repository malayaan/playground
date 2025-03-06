Below is a very minimal preprocessing approach: no thresholding, no histogram equalization, no blurring—just a straightforward grayscale conversion. This should avoid turning your document into black blocks while still improving OCR performance compared to color images.


---

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

PDF_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\part_ged"
IMG_FOLDER = r"V:\SGCIB\FR\IGAD-AUD-RPI-BDT-MISS-2025\001 SGRF Credits consommations\6 - Travaux\DATA\GED_Images"
os.makedirs(IMG_FOLDER, exist_ok=True)

def detect_pdf_type(pdf_path):
    text = extract_text(pdf_path).strip()
    return "native_pdf" if len(text) > 30 else "scanned_pdf"

def enhance_image(image):
    # Convert to grayscale ONLY (no thresholding, no equalization, no blur)
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    return gray

def extract_text_from_pdfs(pdf_folder, img_folder):
    results = []
    
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_type = detect_pdf_type(pdf_path)
            
            if pdf_type == "native_pdf":
                text = extract_text(pdf_path).strip()
            else:
                pdf = pdfium.PdfDocument(pdf_path)
                text_list = []
                for i in range(len(pdf)):
                    # Render at higher resolution for better OCR
                    img = pdf[i].render(scale=2).to_pil()
                    img_path = os.path.join(img_folder, f"{os.path.splitext(pdf_file)[0]}_{i}.jpg")
                    img.save(img_path, "JPEG")

                    processed_img = enhance_image(img)
                    page_text = pytesseract.image_to_string(
                        processed_img, lang="fra", config="--oem 3 --psm 6"
                    ).strip()
                    text_list.append(page_text)
                
                text = "\n".join(text_list)
            
            results.append({"file": pdf_file, "text": text, "quality_flag": pdf_type})
    
    return pd.DataFrame(results)

df_text = extract_text_from_pdfs(PDF_FOLDER, IMG_FOLDER)
df_text.to_csv("extracted_text.csv", index=False)
print(df_text.head())

Key Points:

Grayscale Only: Prevents over-processing that can lead to black blocks.

scale=2: Renders pages at double resolution to improve OCR accuracy.

Tesseract Config: Uses --oem 3 (LSTM engine) and --psm 6 (block of text).


If you need slightly more contrast, you can add light histogram equalization or minimal blur, but start with this plain grayscale approach first. Let me know how it works!

