
---

# 🔍 PARTIE 1 — **Python logique générale**

---

## ✅ **Exercice 1 : Séparer pairs et impairs**

### ✏️ Code :

```python
def pair_ou_impair(nombres):
    pairs = [n for n in nombres if n % 2 == 0]
    impairs = [n for n in nombres if n % 2 != 0]
    return pairs, impairs
```

### 🧠 Explication :

* `def pair_ou_impair(nombres):` → On définit une fonction qui prend en entrée une **liste de nombres**.
* `n % 2 == 0` → Cela signifie que le nombre est **pair** (divisible par 2).
* `[n for n in nombres if ...]` → On utilise une **compréhension de liste** pour parcourir les nombres et en créer deux nouvelles listes :

  * `pairs` contient tous les nombres pairs
  * `impairs` contient tous les autres
* On retourne les deux listes en **tuple**.

### 📝 À retenir :

* Utiliser `%` pour déterminer la parité
* La compréhension de liste = rapide + lisible

---

## ✅ **Exercice 2 : Vérifier un palindrome**

### ✏️ Code :

```python
def est_palindrome(mot):
    return mot == mot[::-1]
```

### 🧠 Explication :

* `mot[::-1]` → C’est un **slice inversé** de la chaîne : `"bonjour"` devient `"ruojnob"`.
* `mot == mot[::-1]` → Vérifie si le mot est égal à son inverse.
* `return` retourne un booléen `True` ou `False`.

### 📝 À retenir :

* Une string peut être **slicée** comme une liste
* Vérification directe : pas besoin de boucle ici

---

## ✅ **Exercice 3 : Trouver le mot le plus long**

### ✏️ Code :

```python
def mot_plus_long(phrase):
    mots = phrase.split()
    return max(mots, key=len)
```

### 🧠 Explication :

* `phrase.split()` → Transforme une phrase `"Je suis CK"` en liste : `["Je", "suis", "CK"]`
* `max(mots, key=len)` → Cherche le mot ayant la plus grande **longueur** dans la liste.
* Le paramètre `key=len` dit à `max()` de comparer les **longueurs** plutôt que les mots eux-mêmes.

### 📝 À retenir :

* `split()` divise une chaîne en mots
* `max(..., key=...)` est une fonction puissante pour trouver des éléments personnalisés

---

# 🧠 PARTIE 2 — **POO Python**

---

## ✅ **Classe Animal + héritage avec Chien**

### ✏️ Code :

```python
class Animal:
    def __init__(self, nom):
        self.nom = nom

    def crier(self):
        return "..."
```

* `class Animal:` → On définit une classe de base.
* `__init__` est le **constructeur**, appelé automatiquement à la création de l’objet.
* `self.nom = nom` → Attribut de l’objet accessible via `self`.
* `crier()` → Méthode qui pourra être redéfinie (polymorphisme).

---

### 🐶 Classe Chien :

```python
class Chien(Animal):
    def crier(self):
        return "Wouf !"
```

* `class Chien(Animal)` → Hérite de la classe `Animal`.
* Elle **redéfinit** (override) la méthode `crier()` → C’est du **polymorphisme**.
* Quand on appelle `crier()` sur un `Chien`, c’est la version "Wouf !" qui est utilisée.

---

### 🔁 Fonction pour tester :

```python
def faire_crier_animaux(animaux):
    for animal in animaux:
        print(animal.nom, ":", animal.crier())
```

* On passe une **liste d’objets** `Animal` ou `Chien`.
* `animal.nom` et `animal.crier()` sont dynamiques : Python choisit la bonne méthode selon le type d’objet.

### 📝 À retenir :

* L’héritage simplifie la gestion de plusieurs types d’objets
* Le polymorphisme permet de remplacer une méthode sans toucher au reste du code

---

# 🛠️ PARTIE 3 — **Odoo : Mini Cas**

---

## ✅ Code Complet :

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Cheval(models.Model):
    _name = 'stable.cheval'
    _description = 'Cheval'

    name = fields.Char(string="Nom", required=True)
    age = fields.Integer(string="Âge")
    est_vieux = fields.Boolean(string="Retraité", compute='_compute_est_vieux', store=True)

    @api.depends('age')
    def _compute_est_vieux(self):
        for cheval in self:
            cheval.est_vieux = cheval.age > 15

    @api.constrains('age')
    def _check_age(self):
        for cheval in self:
            if cheval.age < 0:
                raise ValidationError("L'âge ne peut pas être négatif.")

    def action_marquer_comme_retraité(self):
        for cheval in self:
            cheval.est_vieux = True
```

---

### 📌 Explication par bloc :

#### 📌 Importation :

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError
```

* `models` : base pour créer des modèles.
* `fields` : pour déclarer les champs (comme `Char`, `Boolean`, etc.)
* `api` : contient les décorateurs comme `@api.depends`, `@api.constrains`.
* `ValidationError` : permet de bloquer l’enregistrement si une condition n’est pas remplie.

---

#### 📌 Déclaration du modèle :

```python
class Cheval(models.Model):
    _name = 'stable.cheval'
    _description = 'Cheval'
```

* `models.Model` : tous les modèles Odoo doivent hériter de cette classe.
* `_name` : identifiant technique du modèle dans la base.
* `_description` : description affichée dans l’interface Odoo.

---

#### 📌 Champs :

```python
    name = fields.Char(string="Nom", required=True)
    age = fields.Integer(string="Âge")
    est_vieux = fields.Boolean(string="Retraité", compute='_compute_est_vieux', store=True)
```

* `Char` : texte court.
* `Integer` : nombre entier.
* `Boolean` : case à cocher, ici calculée automatiquement.
* `compute=...` : ce champ est **calculé** via une fonction.
* `store=True` : le champ est **enregistré** en base (sinon juste affiché à l’écran).

---

#### 📌 Champ calculé :

```python
    @api.depends('age')
    def _compute_est_vieux(self):
        for cheval in self:
            cheval.est_vieux = cheval.age > 15
```

* `@api.depends('age')` → Odoo recalcule le champ si `age` change.
* Pour chaque cheval : si `age > 15`, on coche `est_vieux`.

---

#### 📌 Contrainte de validation :

```python
    @api.constrains('age')
    def _check_age(self):
        for cheval in self:
            if cheval.age < 0:
                raise ValidationError("L'âge ne peut pas être négatif.")
```

* `@api.constrains(...)` : exécution automatique avant `create()` et `write()`.
* Si l’âge est négatif, une **erreur bloquante** est levée.

---

#### 📌 Méthode bouton :

```python
    def action_marquer_comme_retraité(self):
        for cheval in self:
            cheval.est_vieux = True
```

* Fonction appelée depuis un **bouton dans la vue**.
* Elle met `est_vieux = True` pour chaque enregistrement sélectionné.

---

