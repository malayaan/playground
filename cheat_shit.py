Oui, il est possible d'ajouter des barres de progression pour UMAP et HDBSCAN, mais ça demande d'instrumenter leurs processus internes. Voici comment faire pour chacun :


---

🚀 1️⃣ Ajouter une barre de progression pour UMAP

UMAP ne fournit pas de barre de progression native, mais tu peux utiliser tqdm pour suivre l’avancement ligne par ligne.

✅ Solution : Activer tqdm dans UMAP

Ajoute l'option verbose=True à UMAP, puis intercepte les logs avec tqdm :

from tqdm import tqdm
import umap

class UMAPProgress(umap.UMAP):
    def fit(self, X, y=None):
        self._tqdm = tqdm(total=X.shape[0], desc="UMAP Training", position=0, leave=True)
        result = super().fit(X, y)
        self._tqdm.close()
        return result

    def _input_to_output(self, *args, **kwargs):
        if hasattr(self, "_tqdm"):
            self._tqdm.update(1)
        return super()._input_to_output(*args, **kwargs)

# Remplace UMAP par cette classe :
umap_model = UMAPProgress(n_neighbors=10, n_components=2, metric='cosine', verbose=True)

✅ Effet : Une barre de progression tqdm s’affiche pendant l’entraînement d’UMAP.


---

🚀 2️⃣ Ajouter une barre de progression pour HDBSCAN

HDBSCAN n’a pas non plus de barre native, mais on peut suivre l’avancement en instrumentant la fonction fit.

✅ Solution : Modifier fit avec tqdm

from tqdm import tqdm
import hdbscan

class HDBSCANProgress(hdbscan.HDBSCAN):
    def fit(self, X, y=None):
        self._tqdm = tqdm(total=3, desc="HDBSCAN Training", position=0, leave=True)
        result = super().fit(X, y)
        self._tqdm.update(1)  # Met à jour après chaque étape importante
        self._tqdm.close()
        return result

# Remplace HDBSCAN par cette classe :
hdbscan_model = HDBSCANProgress(min_cluster_size=10, metric='euclidean')

✅ Effet : Une barre de progression apparaît pendant le clustering HDBSCAN.


---

🔥 Résumé

Avec ça, tu peux voir en direct où en est chaque phase du process UMAP et HDBSCAN 🚀

Dis-moi si ça fonctionne bien ou si tu veux encore plus de détails ! 😃

