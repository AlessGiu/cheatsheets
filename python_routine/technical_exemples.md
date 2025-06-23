
---

# 🔎 **TEST ENTRETIEN PYTHON + ODOO – NIVEAU DÉBUTANT/JUNIOR**

---

## 🧪 **PARTIE 1 — Python Logique Générale**

**⏱ Durée conseillée : 10–15 minutes**

### 🔸 Exercice 1 — Pair ou impair

Écris une fonction `pair_ou_impair(nombres)` qui prend une liste de nombres et retourne deux listes : l’une contenant les pairs, l’autre les impairs.

#### Exemple :

```python
pair_ou_impair([1, 2, 3, 4, 5])
# ➜ ([2, 4], [1, 3, 5])
```

---

### 🔸 Exercice 2 — Palindrome

Écris une fonction `est_palindrome(mot)` qui vérifie si un mot est un palindrome (se lit dans les deux sens).

#### Exemple :

```python
est_palindrome("radar")  # ➜ True
est_palindrome("cheval")  # ➜ False
```

---

### 🔸 Exercice 3 — Trouver le mot le plus long

Écris une fonction qui prend une phrase et retourne le mot le plus long.

---

## ✅ CORRIGÉ PARTIE 1 :

```python
def pair_ou_impair(nombres):
    pairs = [n for n in nombres if n % 2 == 0]
    impairs = [n for n in nombres if n % 2 != 0]
    return pairs, impairs

def est_palindrome(mot):
    return mot == mot[::-1]

def mot_plus_long(phrase):
    mots = phrase.split()
    return max(mots, key=len)
```

---

## 🧠 **PARTIE 2 — POO Python**

**⏱ Durée conseillée : 10 minutes**

### 🔸 Exercice 4 — Classes et héritage

Crée une classe `Animal` avec un attribut `nom`, un constructeur `__init__()` et une méthode `crier()` qui retourne `"..."`.

Puis crée une classe `Chien` qui hérite de `Animal` et redéfinit la méthode `crier()` pour retourner `"Wouf !"`.

#### BONUS :

Crée une fonction qui prend une liste d’`Animal` et affiche leur cri.

---

## ✅ CORRIGÉ PARTIE 2 :

```python
class Animal:
    def __init__(self, nom):
        self.nom = nom

    def crier(self):
        return "..."

class Chien(Animal):
    def crier(self):
        return "Wouf !"

def faire_crier_animaux(animaux):
    for animal in animaux:
        print(animal.nom, ":", animal.crier())
```

---

## 🔧 **PARTIE 3 — Odoo : Mini Cas Pratique**

**⏱ Durée conseillée : 15–20 minutes**

### 🔸 Contexte :

Tu travailles sur un module `écurie`. On te demande de créer un modèle `stable.cheval` avec les règles suivantes :

### 🔹 Objectif :

1. Créer les champs suivants :

   * `name` (char)
   * `age` (integer)
   * `est_vieux` (boolean calculé si age > 15)

2. Ajouter une contrainte qui empêche d’avoir un âge négatif

3. Créer un bouton `action_marquer_comme_retraité` qui met `est_vieux = True`

---

## ✅ CORRIGÉ PARTIE 3 :

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

