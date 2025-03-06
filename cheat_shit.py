To create a Kedro project that handles the requirements you mentioned, you will need the following basic structure:

1. Input: PDFs (with or without text).


2. Processing: Classifying PDFs into two categories:

PDFs with text go into one folder.

PDFs without text go into another folder.



3. Processing Images: OCR all images in a separate node.



We’ll set up the project with the following steps:

Step 1: Check if the PDF contains text or is an image.

Step 2: Save PDFs with text to one folder.

Step 3: Save PDFs without text to another folder.

Step 4: OCR the images in the PDF (in a separate node).



---

Step 1: Setting Up the Kedro Project

First, create a new Kedro project by running the following command in your terminal:

kedro new --starter=pandas-iris

This will create a Kedro project with the default template. Let’s then modify it to fit your needs.

Step 2: Add Dependencies

Ensure you have the following dependencies installed:

pip install kedro pdfminer.six pytesseract pdfium paddlepaddle-gpu

Step 3: Project Directory Structure

Here’s the directory structure for your Kedro project:

kedro_project/
├── conf/
│   ├── base/
│   │   └── catalog.yml
│   └── local/
│       └── catalog.yml
├── data/
│   ├── raw/
│   ├── output/
│   │   ├── with_text/
│   │   └── without_text/
├── notebooks/
├── src/
│   ├── <your_project_name>/
│   │   ├── pipeline/
│   │   │   ├── nodes.py
│   │   │   ├── pipeline.py
│   │   ├── pipelines.py
│   │   └── settings.py
└── kedro.yml

Step 4: Kedro Nodes

1. Node 1: Classifying PDFs with Text or Without Text

Create a node to check if the PDF contains text using pdfminer.six and classify it.

In src/<your_project_name>/pipeline/nodes.py:

import os
from pdfminer.high_level import extract_text
from pathlib import Path

def classify_pdfs(pdf_folder: str, with_text_folder: str, without_text_folder: str):
    """Classify PDFs with or without text and move them into separate folders."""
    # Create folders if they don't exist
    Path(with_text_folder).mkdir(parents=True, exist_ok=True)
    Path(without_text_folder).mkdir(parents=True, exist_ok=True)

    # Get list of PDF files
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        raw_text = extract_text(pdf_path).strip()

        # Classify PDF and move it to the corresponding folder
        if len(raw_text) > 30:
            # PDF contains text
            os.rename(pdf_path, os.path.join(with_text_folder, pdf_file))
        else:
            # PDF doesn't contain text
            os.rename(pdf_path, os.path.join(without_text_folder, pdf_file))

    return {"with_text": with_text_folder, "without_text": without_text_folder}

2. Node 2: OCR for Images in Scanned PDFs

For scanned PDFs (images), we need a separate node that processes the images. We'll OCR these pages using PaddleOCR or Tesseract.

In src/<your_project_name>/pipeline/nodes.py:

from paddleocr import PaddleOCR
from pathlib import Path
import pdfium
import os
import cv2
import pytesseract
import numpy as np

ocr_model = PaddleOCR(use_angle_cls=True, lang='fra', use_gpu=True)

def ocr_scanned_pdfs(pdf_folder: str, output_folder: str):
    """Perform OCR on images in scanned PDFs and save the results."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Get list of PDF files (only those in the 'without_text' folder)
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        pdf = pdfium.PdfDocument(pdf_path)

        text_list = []
        for i in range(len(pdf)):
            page = pdf[i]
            img = page.render(scale=3, grayscale=False).to_pil()
            np_img = np.array(img)
            gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

            # OCR using PaddleOCR or Tesseract
            ocr_result = ocr_model.ocr(gray, cls=True)
            page_text = "\n".join([line[1][0] for line in ocr_result])
            text_list.append(page_text)

        # Save OCR output to file
        output_file = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}.txt")
        with open(output_file, 'w') as f:
            f.write("\n".join(text_list))

    return {"ocr_output": output_folder}


---

Step 5: Pipeline Configuration

In src/<your_project_name>/pipeline/pipeline.py, define your pipeline:

from kedro.pipeline import Pipeline, node
from .nodes import classify_pdfs, ocr_scanned_pdfs

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=classify_pdfs,
                inputs=["params:pdf_folder", "params:with_text_folder", "params:without_text_folder"],
                outputs=["with_text", "without_text"],
                name="classify_pdfs_node",
            ),
            node(
                func=ocr_scanned_pdfs,
                inputs=["with_text", "params:ocr_output_folder"],
                outputs="ocr_output",
                name="ocr_scanned_pdfs_node",
            ),
        ]
    )

Step 6: Configuration (catalog.yml)

Now, configure the Kedro catalog.yml to specify where to read and write the data:

In conf/base/catalog.yml:

pdf_folder:
  type: str
  value: "/path/to/your/pdfs"

with_text_folder:
  type: str
  value: "data/output/with_text/"

without_text_folder:
  type: str
  value: "data/output/without_text/"

ocr_output_folder:
  type: str
  value: "data/output/ocr_text/"

Step 7: Running the Pipeline

Now you can run the Kedro pipeline with:

kedro run

This will:

Classify PDFs into two folders: with_text and without_text.

Run OCR on the images in the without_text folder and output the results into the ocr_text folder.


Summary

Node 1: Classifies PDFs with or without text and moves them into separate folders.

Node 2: Performs OCR on scanned PDFs and outputs the text to a file.

Input: PDF folder with PDFs (some may have text, some may be images).

Output: Two folders for PDFs (with text and without text), and OCR text files for images.


This Kedro pipeline ensures a clean separation of concerns and can be easily extended for future processing.

