🔥 OK, on va tout corriger avec le bon chemin !

Tu m’as dit que cuDNN est dans :

/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/cudnn-linux-x86_64-9.8.0.87_cuda12-archive

Donc on va mettre à jour les variables d’environnement avec ce chemin.


---

📌 1️⃣ Mettre à jour les variables d’environnement

Exécute ces commandes :

export CUDNN_PATH="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/cudnn-linux-x86_64-9.8.0.87_cuda12-archive"
export LD_LIBRARY_PATH="$CUDNN_PATH/lib:$LD_LIBRARY_PATH"
export CPATH="$CUDNN_PATH/include:$CPATH"
export LIBRARY_PATH="$CUDNN_PATH/lib:$LIBRARY_PATH"


---

📌 2️⃣ Ajouter ces variables au .bashrc

Pour que ça reste en mémoire même après un redémarrage :

echo 'export CUDNN_PATH="/home/a730878/25-AUD-RPI-001_Credits-consommations/cons-frf/audio-analysis/data/SAVED_MODELS/cudnn-linux-x86_64-9.8.0.87_cuda12-archive"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="$CUDNN_PATH/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
echo 'export CPATH="$CUDNN_PATH/include:$CPATH"' >> ~/.bashrc
echo 'export LIBRARY_PATH="$CUDNN_PATH/lib:$LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc

