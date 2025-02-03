import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode

def read_qr_code(image_path):
    """
    Lit et extrait les données d'un QR Code 2D-Doc à partir d'une image.
    """
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Appliquer un traitement pour améliorer la lecture
    _, image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scanner le QR Code / DataMatrix
    decoded_data = decode(image_bin)
    
    if not decoded_data:
        print("⚠️ Aucun QR Code détecté.")
        return None
    
    # Extraire les données sous forme de texte
    qr_text = decoded_data[0].data.decode("utf-8")
    print(f"📄 Données brutes du 2D-Doc : {qr_text}")

    return qr_text

def parse_2ddoc_data(qr_text):
    """
    Analyse manuellement les données extraites du QR Code 2D-Doc.
    """
    data_dict = {}
    
    # Détection du format (JSON, XML, ou format simple `|`)
    if "|" in qr_text:  # Cas classique d'un 2D-Doc fiscal
        elements = qr_text.split("|")
        
        # Exemple hypothétique de format : "FRTAX|123456789|DUPONT|45000€"
        if len(elements) >= 3:
            data_dict["Type"] = elements[0]
            data_dict["Numéro fiscal"] = elements[1]
            data_dict["Nom"] = elements[2]
            if len(elements) > 3:
                data_dict["Revenu"] = elements[3]

    elif "{" in qr_text and "}" in qr_text:  # Format JSON encodé
        import json
        try:
            data_dict = json.loads(qr_text)
        except json.JSONDecodeError:
            print("⚠️ Impossible de décoder le JSON.")

    elif "<" in qr_text and ">" in qr_text:  # Format XML encodé
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(qr_text)
            for child in root:
                data_dict[child.tag] = child.text
        except ET.ParseError:
            print("⚠️ Impossible de décoder l’XML.")

    return data_dict

# 📌 Exécution avec une image de QR Code 2D-Doc
image_path = "chemin/vers/l_image_qr_code.png"
qr_text = read_qr_code(image_path)

if qr_text:
    parsed_data = parse_2ddoc_data(qr_text)
    print("\n✅ Informations extraites du 2D-Doc :")
    for key, value in parsed_data.items():
        print(f"🔹 {key}: {value}")