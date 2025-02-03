import cv2
from pyzbar.pyzbar import decode
from PIL import Image

def scan_qr_code(image_path):
    # Charger l'image avec OpenCV
    image = cv2.imread(image_path)

    # Convertir en niveaux de gris pour améliorer la détection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Scanner le QR Code
    decoded_objects = decode(gray)

    if not decoded_objects:
        print("Aucun QR Code détecté.")
        return None

    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        print("Contenu du QR Code 2D-Doc :", qr_data)
        return qr_data

    return None

# Exemple d'utilisation
image_file = "qrcode.png"  # Remplacez par votre fichier
qr_content = scan_qr_code(image_file)

if qr_content:
    print("QR Code 2D-Doc extrait avec succès :", qr_content)
else:
    print("Aucun QR Code trouvé.")