from pylibdmtx.pylibdmtx import decode
from PIL import Image

def decode_datamatrix(image_path):
    # Charger l'image avec Pillow
    image = Image.open(image_path)
    
    # Décoder le DataMatrix
    decoded_objects = decode(image)
    
    if decoded_objects:
        for obj in decoded_objects:
            print("Contenu du DataMatrix :", obj.data.decode('utf-8'))
            return obj.data.decode('utf-8')
    else:
        print("Aucun code DataMatrix détecté.")
        return None

# Exemple d'utilisation
image_file = "/mnt/data/file-Hi7zTX6szxGwGPT7iPJLKU"
data = decode_datamatrix(image_file)

if data:
    print("Code 2D-Doc extrait avec succès :", data)
else:
    print("Impossible de lire le DataMatrix.")