Parfait ! Voici 5 questions de réactivation pour le début de la 2ᵉ journée, avec des extraits de code autour de :

merge

apply

regex

data analysis simple (stats / groupby)

Et un peu de logique conditionnelle


Format : “Que retourne ce code ?” ou “Explique ce que fait ce code”. Tous les exemples sont courts et directement interprétables par des gens qui ont vu la journée 1.


---

1. Merge (jointure)

df1 = pd.DataFrame({"id": [1, 2], "nom": ["Alice", "Bob"]})
df2 = pd.DataFrame({"id": [2, 3], "score": [88, 75]})
print(pd.merge(df1, df2, on="id", how="inner"))

Question : Que va afficher ce code ?

> Réponse : Une ligne avec id = 2, nom = "Bob", score = 88 (car inner garde uniquement les id communs)




---

2. apply() avec une fonction simple

df = pd.DataFrame({"age": [20, 30, 40]})
df["age_cat"] = df["age"].apply(lambda x: "jeune" if x < 35 else "vieux")
print(df["age_cat"])

Question : Que contient la colonne age_cat ?

> Réponse : ["jeune", "jeune", "vieux"]




---

3. Regex avec str.contains()

df = pd.DataFrame({"email": ["alice@mail.com", "bob@sg.fr", "contact@banque.fr"]})
print(df[df["email"].str.contains(".*@.*\.fr")])

Question : Quelles lignes seront gardées ?

> Réponse : Les emails se terminant par .fr : bob@sg.fr et contact@banque.fr




---

4. Groupby + mean

df = pd.DataFrame({"job": ["admin", "admin", "student"], "age": [30, 40, 22]})
print(df.groupby("job")["age"].mean())

Question : Que retourne ce code ?

> Réponse :



job
admin     35.0
student   22.0
Name: age, dtype: float64


---

5. apply() avec row (axis=1)

df = pd.DataFrame({"nom": ["Alice", "Bob"], "score": [80, 90]})
def bonus(row):
    return row["score"] + 5 if row["nom"] == "Alice" else row["score"]

df["score_bonus"] = df.apply(bonus, axis=1)
print(df["score_bonus"])

Question : Quelles sont les valeurs de score_bonus ?

> Réponse : [85, 90] (Alice reçoit +5)




---

Souhaites-tu un format PDF imprimable, slides, ou une version type quiz collectif avec réponse à l’oral ? Je peux te le préparer tout de suite.

