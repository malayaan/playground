D’après ton image, which conda ne retourne toujours pas le bon chemin après avoir ajouté le bon PATH. Cela signifie que la fonction conda n’est pas correctement initialisée.


---

✅ Solution : Forcer l’activation correcte de Conda

Essaye ces étapes dans cet ordre :

1️⃣ Désactiver les anciennes configurations

Nettoie les éventuelles anciennes activations de Conda :

unset CONDA_SHLVL
unset CONDA_PROMPT_MODIFIER
unset CONDA_EXE
unset _CE_CONDA
unset _CE_M
unset CONDA_ROOT
unset CONDA_PYTHON_EXE

Puis recharge ton shell :

exec bash


---

2️⃣ Activer Conda proprement

Charge correctement le script de Conda :

source /home/a730878/bin/mf-24.9.2-0/etc/profile.d/conda.sh

Ensuite, vérifie que conda fonctionne bien :

which conda

Si ça retourne /home/a730878/bin/mf-24.9.2-0/bin/conda, alors c’est bon ! ✅


---

3️⃣ Activer ton environnement et vérifier

Si Conda est bien détecté, active ton environnement avec :

conda activate env_audit_credit_3.9

Puis, vérifie que Python est bien dans le bon environnement :

which python

Tu dois voir :

/home/a730878/.conda/envs/env_audit_credit_3.9/bin/python

✅ Si c’est bon, ton environnement est bien activé.


---

4️⃣ Rendre la configuration permanente

Si tout fonctionne bien, ajoute cette ligne à ton fichier ~/.bashrc pour ne pas avoir à refaire ces étapes :

echo 'source /home/a730878/bin/mf-24.9.2-0/etc/profile.d/conda.sh' >> ~/.bashrc

Puis recharge le terminal avec :

source ~/.bashrc


---

📌 Résumé des étapes

1️⃣ Nettoie l’ancienne configuration (unset ...).
2️⃣ Recharge le shell (exec bash).
3️⃣ Active Conda proprement (source /home/a730878/bin/mf-24.9.2-0/etc/profile.d/conda.sh).
4️⃣ Vérifie que which conda affiche bien le bon chemin.
5️⃣ Active ton environnement (conda activate env_audit_credit_3.9).
6️⃣

