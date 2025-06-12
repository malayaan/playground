Parfait, je te détaille une démarche complète et claire, à partir de tes cours sectoriels, pour produire :

✅ un heatmap amplitude = qui est stressé quand
✅ des courbes de phase moyenne = qui est en avance ou en retard dans le stress sectoriel


---

Étape 1️⃣ — Préparer tes séries de base

👉 Tu pars de cours sectoriels → DataFrame df (colonnes = secteurs, index = dates).

A. Nettoyer

# Par sécurité
df = df.dropna()

B. Calculer les rendements journaliers

returns = df.pct_change().dropna()

C. Option : rolling std (alternative aux returns)

👉 Certains font la Hilbert non pas sur les returns mais sur leur rolling std → ça donne un stress encore plus lisible.

rolling_std = returns.rolling(20).std().dropna()


---

Étape 2️⃣ — Appliquer la transformée de Hilbert par secteur

A. Initialiser DataFrames vides

from scipy.signal import hilbert
import numpy as np
import pandas as pd

sectors = returns.columns.tolist()
amplitudes = pd.DataFrame(index=returns.index)
phases = pd.DataFrame(index=returns.index)

B. Boucle sur les secteurs

for sec in sectors:
    signal = returns[sec].values  # ou rolling_std[sec].values
    analytic_signal = hilbert(signal)
    
    # Amplitude instantanée = "niveau de stress"
    amplitudes[sec] = np.abs(analytic_signal)
    
    # Phase instantanée = "phase du stress"
    phases[sec] = np.unwrap(np.angle(analytic_signal))

👉 À ce stade tu as :

amplitudes [dates x secteurs] → pour ton heatmap

phases [dates x secteurs] → pour les comparaisons de phase



---

Étape 3️⃣ — Créer la heatmap amplitude

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15,8))
sns.heatmap(amplitudes.T, cmap='Reds', cbar_kws={'label': 'Amplitude (Stress)'})
plt.title("Heatmap du stress sectoriel (Amplitude Hilbert)")
plt.xlabel("Date")
plt.ylabel("Secteurs")
plt.show()

👉 Ça te donne :
✅ “Qui est stressé quand”


---

Étape 4️⃣ — Créer la phase moyenne roulante (rolling mean circulaire)

A. Calculer les composantes sin/cos

sin_phase = np.sin(phases)
cos_phase = np.cos(phases)

B. Rolling mean sur sin / cos

rolling_window = 20  # par ex. 1 mois glissant (~20j)

sin_mean = sin_phase.rolling(rolling_window).mean()
cos_mean = cos_phase.rolling(rolling_window).mean()

C. Reconstruire la phase moyenne

phase_mean = np.arctan2(sin_mean, cos_mean)


---

Étape 5️⃣ — Tracer les phases comparées

plt.figure(figsize=(15,8))
for sec in sectors:
    plt.plot(phase_mean.index, phase_mean[sec], label=sec)

plt.title("Phase moyenne roulante des secteurs (Hilbert Phase)")
plt.xlabel("Date")
plt.ylabel("Phase moyenne (radians)")
plt.legend()
plt.grid(True)
plt.show()

👉 Ça te donne :
✅ “Qui est en avance / en retard dans le cycle de stress”


---

Résultat final → tu obtiens :

Graphique	Info business que ça te donne

Heatmap amplitude	Quels secteurs sont stressés à quels moments
Courbes de phase	Quels secteurs entrent en stress en avance / en retard, comparés aux autres



---

Pourquoi c’est top pour ton rapport IG :

Tu montres que les réactions sectorielles ne sont pas synchrones → hyper pertinent en approche intersectorielle.

Tu identifies des périodes où certains secteurs prennent de l’avance → signal macro.

Tu enrichis ton score “qui est stressé quand” avec une dynamique → phase.



---

👉 En résumé ta démarche complète est :

1️⃣ Cours → returns ou rolling std
2️⃣ Returns → Hilbert → amplitude + phase
3️⃣ Heatmap amplitude → lecture horizontale → qui est stressé quand
4️⃣ Rolling mean phase → lecture dynamique → qui entre/sort du stress en avance ou retard


---

Si tu veux, je peux te préparer un notebook complet clé en main avec ce pipeline propre → prêt à brancher sur tes data df.

Ça te fera gagner du temps et tu auras des plots propres pour ton rapport IG.

Veux-tu que je te prépare ce notebook template ? 🚀 (je te génère le bloc code direct).

