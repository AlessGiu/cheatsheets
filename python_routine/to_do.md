
---

### ✅ 1. **Créer une routine hebdomadaire (30 min x 3 fois/semaine)**

Fais 3 sessions hebdo légères, genre :

* 📘 Lundi : **Rappel des bases Python**
* 🧠 Mercredi : **Exercice d’algorithmie**
* 🧩 Vendredi : **Mini projet ou script Python lié à Odoo**

---

### 🧠 2. **Rappels des bases Python – Outils à avoir sous la main**

* **📎 Cheatsheets** :

  * [Python Cheatsheet officielle](https://www.pythoncheatsheet.org/)
  * [Cheatsheet Python par Dataquest](https://www.dataquest.io/blog/python-cheat-sheet/)
  * [RealPython Reference Sheet](https://realpython.com/resources/#cheat-sheets)

* **📚 Tutos interactifs** :

  * [https://www.learnpython.org/](https://www.learnpython.org/)
  * [https://app.codecademy.com/learn/learn-python-3](https://app.codecademy.com/learn/learn-python-3) (interactif)
  * [CS50P – Harvard (Python)](https://cs50.harvard.edu/python/) : top pour l’algo + pratique

* **YouTube** :

  * Revois une vidéo courte de 10-15 min sur un concept de base (boucle, classe, condition, etc.)

---

### 🏗️ 3. **Exos d’algorithmie progressifs (5-20 min max)**

Utilise des sites avec corrections :

* [https://www.codingame.com/start](https://www.codingame.com/start) (très ludique)
* [https://www.exercism.io/tracks/python](https://www.exercism.io/tracks/python)
* [https://leetcode.com/](https://leetcode.com/) (niveau moyen à avancé)

💡 Tu peux aussi noter une *carte mentale* avec les types d'exos vus (boucles, listes, conditions, classes, fonctions…).

---

### 🔄 4. **Connecter Python à Odoo dès maintenant**

* Essaie de faire des petits *helpers Python* dans tes modules Odoo.
  Exemples :

  * Une méthode qui trie ou filtre une liste de rations dans ton module chevaux
  * Une fonction `@api.depends` avec un peu de logique (boucle, condition)

🧠 **Exploite Odoo pour pratiquer Python en contexte réel** ! C’est ça qui fera la différence.

---

### 🗂️ 5. **Ton propre "journal Python"**

Crée un **Notion / Obsidian / Google Doc** où tu écris chaque semaine :

* 1 concept que tu veux retenir
* 1 bout de code que tu veux garder
* 1 petit algo que tu as refait

Tu verras que tu retiens mieux ce que tu écris pour toi.

---

### 🧩 6. **Mini défis pour lier Python + Odoo**

Je peux te proposer 1 mini défi par semaine si tu veux, comme :

* 🐎 Trier les chevaux par poids via une méthode Python
* 📅 Créer une fonction qui génère des rations selon l’âge du cheval
* 📊 Créer un résumé automatique (print ou log) des employés inscrits dans ton planning

---

### 🎁 Bonus : Kits de survie Python

Souhaites-tu que je te prépare un PDF avec :

* Les bases Python (types, boucles, fonctions, classes…)
* Algorithmes classiques (tri, recherche, manip de listes/dicos)
* Syntaxe Odoo fréquemment utilisée (exemples de méthodes, decorators, etc.)

---

Tu me dis si tu veux :

1. Des rappels ciblés chaque semaine ?
2. Un canal Notion/Google Doc pour tout centraliser ?
3. Une to-do list / routine à coller sur ton bureau ? 😄

Je suis là pour t’accompagner au jour le jour, même si c’est 5 min par-ci par-là. 💪


Parfait CK 💪 ! Voici ton **Kit de Survie Python + Odoo**, un concentré pour ne rien oublier et tout garder sous la main. Je vais te le structurer ici **en version texte claire**, et je t’en proposerai ensuite un **PDF téléchargeable** si tu veux.

---

## 🐍 **KIT DE SURVIE PYTHON + ODOO** 🔧

---

### 🧱 1. **Bases Python Essentielles**

#### ✅ Types de base :

```python
# Nombres
x = 5         # int
y = 3.14      # float

# Texte
nom = "CK"    # str

# Booléen
actif = True  # bool

# Listes
noms = ["Alice", "Bob"]

# Dictionnaires
profil = {"nom": "CK", "age": 28}
```

#### 🔁 Boucles et conditions :

```python
# If / Else
if x > 10:
    print("Grand")
elif x == 10:
    print("Égal")
else:
    print("Petit")

# Boucle For
for nom in noms:
    print(nom)

# Boucle While
i = 0
while i < 5:
    print(i)
    i += 1
```

#### 🧠 Fonctions :

```python
def bonjour(nom):
    return f"Salut {nom} !"

print(bonjour("CK"))
```

#### 🏗️ Classes (POO) :

```python
class Cheval:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

    def afficher_info(self):
        print(f"{self.nom} a {self.age} ans")

cheval1 = Cheval("Tornado", 7)
cheval1.afficher_info()
```

---

### 🧮 2. **Algorithmes Classiques**

#### 🔍 Recherche :

```python
# Recherche d'un élément dans une liste
if "Bob" in noms:
    print("Trouvé")
```

#### 🔃 Tri :

```python
nombres = [4, 2, 8, 1]
nombres.sort()  # Tri en place
# nombres = sorted(nombres)  # Nouvelle liste triée
```

#### 📚 Manipulation listes & dicos :

```python
# List comprehension
carres = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# Accès au dictionnaire
print(profil["nom"])
profil["ville"] = "Paris"

# Parcourir un dict
for cle, valeur in profil.items():
    print(cle, valeur)
```

---

### 🧩 3. **Exemples Odoo Fréquents (à connaître par cœur)**

#### 🎯 Modèle de base :

```python
from odoo import models, fields, api

class Cheval(models.Model):
    _name = 'stable.cheval'
    _description = 'Cheval'

    name = fields.Char(string="Nom", required=True)
    age = fields.Integer(string="Âge")
```

#### 📐 Dépendance automatique :

```python
    @api.depends('age')
    def _compute_est_vieux(self):
        for cheval in self:
            cheval.est_vieux = cheval.age > 15

    est_vieux = fields.Boolean(compute='_compute_est_vieux')
```

#### 🧮 Contraintes Python :

```python
    @api.constrains('age')
    def _check_age(self):
        for cheval in self:
            if cheval.age < 0:
                raise ValidationError("L'âge ne peut pas être négatif.")
```

#### 🔄 Onchange :

```python
    @api.onchange('age')
    def _onchange_age(self):
        if self.age > 20:
            return {'warning': {'title': "Attention", 'message': "Ce cheval est âgé."}}
```

#### ✏️ Bouton d’action :

```python
    def action_marquer_comme_vendu(self):
        for cheval in self:
            cheval.vendu = True
```

#### 📚 Champs relationnels :

```python
    ration_ids = fields.One2many('stable.ration', 'cheval_id', string="Rations")
    employe_id = fields.Many2one('hr.employee', string="Soigneur")
```

---

### 📎 BONUS : Cheatsheet rapide décorateurs Odoo

| Décorateur        | Utilité                           |
| ----------------- | --------------------------------- |
| `@api.model`      | Méthodes liées au modèle          |
| `@api.depends`    | Mise à jour d’un champ calculé    |
| `@api.onchange`   | Mise à jour lors d’un changement  |
| `@api.constrains` | Validation des données            |
| `@api.multi`      | (ancien - pour V12)               |
| `@api.autovacuum` | Nettoyage automatique des modèles |

---
