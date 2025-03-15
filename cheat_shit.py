Si tu as supprimé FFmpeg, mais que le chemin apparaît encore, il se peut que :

1. Le chemin soit toujours enregistré dans le $PATH, même si le fichier n'existe plus.


2. Un cache de which ou du shell garde une ancienne référence.




---

📌 Vérifier si le fichier FFmpeg existe vraiment

Pour t’assurer que le fichier n’est plus là, essaie :

ls -l /home/a730878/tools/python/bin/ffmpeg
ls -l /home/a730878/bin/ffmpeg
ls -l /usr/local/bin/ffmpeg
ls -l /usr/bin/ffmpeg

Si l’un des fichiers existe encore, supprime-le avec :

rm -f /chemin/vers/ffmpeg


---

📌 Nettoyer le $PATH et le cache

Si which ffmpeg affiche encore un chemin inexistant, il faut nettoyer :

1. Supprimer FFmpeg du PATH :

export PATH=$(echo $PATH | sed -e 's|:/home/a730878/tools/python/bin||g')


2. Vérifier si le PATH est bien mis à jour :

echo $PATH


3. Nettoyer le cache du shell :

hash -r




---

📌 Vérifier que FFmpeg n’existe plus

Après tout ça, reteste :

which ffmpeg
ffmpeg -version

Si aucun chemin n’est trouvé, alors FFmpeg est bien supprimé.


---

🚀 Maintenant, tu peux installer proprement la nouvelle version de FFmpeg !

