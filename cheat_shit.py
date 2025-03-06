import os
import pdfium
import cv2
import pytesseract
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # Adjust if needed

PDF_FOLDER = "/path/to/pdfs"
OUTPUT_CSV = "extracted_text.csv"

def render_pdf_to_images(pdf_path, scale=2):
    """Convert each page of a PDF to a high-resolution PIL image."""
    images = []
    pdf = pdfium.PdfDocument(pdf_path)
    for i in range(len(pdf)):
        page = pdf[i]
        # scale=2 or higher for better DPI
        pil_img = page.render(scale=scale, grayscale=False).to_pil()
        images.append(pil_img)
    return images

def ocr_with_tesseract(image):
    """OCR a PIL image with Tesseract in grayscale."""
    np_img = np.array(image)
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(gray, lang="fra", config="--oem 3 --psm 6")
    return text.strip()

def process_one_pdf(pdf_path):
    """Detect if PDF is scanned or native, then extract text accordingly."""
    from pdfminer.high_level import extract_text
    raw_text = extract_text(pdf_path).strip()

    # If there's enough text from pdfminer, it's likely a native PDF
    if len(raw_text) > 30:
        return os.path.basename(pdf_path), raw_text, "native_pdf"
    else:
        # It's probably scanned; do OCR page by page
        images = render_pdf_to_images(pdf_path, scale=3)  # scale=3 for higher quality
        page_texts = [ocr_with_tesseract(img) for img in images]
        return os.path.basename(pdf_path), "\n".join(page_texts), "scanned_pdf"

def main():
    pdf_files = [os.path.join(PDF_FOLDER, f) for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    results = []
    with ProcessPoolExecutor() as executor:
        for pdf_file, text, flag in executor.map(process_one_pdf, pdf_files):
            results.append({"file": pdf_file, "text": text, "quality_flag": flag})

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print(df.head())

if __name__ == "__main__":
    main()