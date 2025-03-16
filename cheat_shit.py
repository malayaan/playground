🚀 Pas de souci ! On va configurer cuDNN sans sudo, directement dans ton dossier SAVED_MODELS !

Tu as décompressé cuDNN dans /home/a730878/25-AUD-RPI-001_Credits-consommations/data/SAVED_MODELS/, donc on va utiliser ce chemin au lieu de /usr/local/cuda/.


---

📌 1️⃣ Définir les variables d’environnement pour cuDNN

Comme tu n’as pas sudo, on va dire à ton système d’utiliser le cuDNN dans ton dossier personnel :

export CUDNN_PATH="/home/a730878/25-AUD-RPI-001_Credits-consommations/data/SAVED_MODELS/cudnn-linux-x86_64-9.8.0.87_cuda12-archive"
export LD_LIBRARY_PATH="$CUDNN_PATH/lib:$LD_LIBRARY_PATH"
export CPATH="$CUDNN_PATH/include:$CPATH"
export LIBRARY_PATH="$CUDNN_PATH/lib:$LIBRARY_PATH"

Ajoute ces lignes à ton .bashrc pour qu’elles soient chargées à chaque session :

echo 'export CUDNN_PATH="/home/a730878/25-AUD-RPI-001_Credits-consommations/data/SAVED_MODELS/cudnn-linux-x86_64-9.8.0.87_cuda12-archive"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="$CUDNN_PATH/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
echo 'export CPATH="$CUDNN_PATH/include:$CPATH"' >> ~/.bashrc
echo 'export LIBRARY_PATH="$CUDNN_PATH/lib:$LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc


---

📌 2️⃣ Vérifier que cuDNN est bien pris en compte

Lance ces commandes :

ls $CUDNN_PATH/lib | grep cudnn
python -c "import torch; print(torch.backends.cudnn.version())"

