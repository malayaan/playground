D'après ton ps aux | grep conda, Conda utilise 99.9% du CPU, ce qui signifie qu'il est toujours en train de résoudre les dépendances et n'est pas bloqué.
💡 Mais ça reste anormalement long → il faut optimiser !


---

📌 Que faire maintenant ?

1️⃣ Stopper Conda (si ça dure trop longtemps)

Si ça tourne depuis plus de 30-40 minutes, annule avec :

CTRL + C

Puis, force l'arrêt des processus Conda :

pkill -f conda

Ensuite, nettoie Conda pour éviter de futurs blocages :

conda clean --all -y


---

2️⃣ Installer en plusieurs étapes

Réinstalle par petits groupes de packages, au lieu de tout d’un coup :

🔹 Étape 1 : Installer les packages de base

conda install -y numpy pandas scipy matplotlib seaborn tqdm requests jupyter notebook ipykernel

🔹 Étape 2 : Installer TensorFlow et PyTorch séparément

conda install -y tensorflow pytorch torchvision torchaudio cudatoolkit

🔹 Étape 3 : Installer les bibliothèques scientifiques

conda install -y scikit-learn nltk statsmodels xgboost lightgbm opencv h5py

🔹 Étape 4 : Installer les bibliothèques restantes

conda install -y flask fastapi sqlalchemy cryptography jinja2 pillow geopandas spacy transformers datasets tokenizers


---

3️⃣ Activer mamba pour accélérer

Si Conda est toujours lent, remplace-le par mamba (10x plus rapide) :

conda install -y mamba
mamba install -y numpy pandas scipy matplotlib seaborn


---

4️⃣ Forcer Conda à utiliser un solveur plus rapide

Ajoute cette option pour accélérer conda :

conda install --solver=libmamba -y numpy pandas scipy matplotlib seaborn

Ou configure-le par défaut :

conda config --set solver libmamba


---

🚀 Résumé :

✅ Si Conda tourne toujours après 30-40 min, annule (CTRL + C)
✅ Installe en plusieurs étapes (au lieu d’un gros bloc).
✅ Utilise mamba pour accélérer Conda.
✅ Active libmamba comme solveur plus rapide.

Essaie ces solutions et dis-moi si ça avance mieux ! 🚀

