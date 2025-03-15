🔥 Bonne nouvelle ! Tu as CUDA 12.6 installé et deux GPU Tesla V100 avec 16 Go de VRAM chacun.

🚨 Le problème vient donc de cuDNN. Il manque libcudnn ou il n'est pas bien configuré.


---

📌 1️⃣ Vérifier si cuDNN est installé

Lance cette commande pour voir si libcudnn est bien installé :

ls /usr/local/cuda/lib64 | grep cudnn

Si aucun résultat, alors cuDNN n'est pas installé.

Si tu vois des fichiers comme libcudnn.so, alors il faut juste ajouter son chemin :

export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

Puis teste si Faster Whisper fonctionne à nouveau.


---

📌 2️⃣ Installer cuDNN pour CUDA 12.6 (si absent)

Si ls /usr/local/cuda/lib64 | grep cudnn ne trouve rien, installe cuDNN avec conda :

conda install -c nvidia cudnn

Puis configure-le :

export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH


---

📌 3️⃣ Vérifier que cuDNN est bien activé

