
---

## 🧪 **1. Exercices Python Classiques (Algorithmiques)**

### 🔁 Boucles, conditions, fonctions

* Écrire une fonction qui retourne les nombres pairs d’une liste
* Trouver le plus grand mot dans une chaîne
* Compter le nombre d’occurrences d’un mot ou d’un caractère

> *Exemple* :

```python
def mots_longs(chaine):
    mots = chaine.split()
    return max(mots, key=len)
```

---

## 📦 **2. Orienté Objet (POO)**

### Très fréquent :

* Créer une classe `Animal` avec `nom`, `age`, `crier()`
* Hériter une classe `Chien` qui redéfinit `crier()`
* Manipuler des listes d'objets (filtrer les chiens âgés > 10 ans)

> *Exemple* :

```python
class Animal:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

    def crier(self):
        return "..."

class Chien(Animal):
    def crier(self):
        return "Wouf !"
```

---

## 🛠️ **3. Cas Pratiques Odoo (très courant)**

### ✅ Types de questions :

* Créer un modèle avec `fields.Char`, `fields.One2many`, etc.
* Ajouter une méthode `@api.depends`
* Ajouter une action (bouton)
* Ajouter une contrainte ou `@api.onchange`
* Simuler une vue Kanban ou un domaine (`domain=[('age', '>', 5)]`)

> *Exemple* :
> **Créer un modèle `stable.cheval` avec un champ calculé `est_vieux` si l’âge > 15, une contrainte qui empêche un âge négatif, et un bouton `action_retourner_ecurie()`**

---

## 📊 **4. SQL (parfois)**

Surtout si la société fait des reporting/BI dans Odoo.

### Exemples :

* Écrire une requête SQL simple : `SELECT`, `JOIN`, `GROUP BY`
* Requêtes sur les modèles `res_partner`, `sale_order`, etc.

> *Exemple* :

```sql
SELECT name, date_order
FROM sale_order
WHERE amount_total > 1000;
```

---

## 📋 **5. Lecture de code Odoo**

Très courant en entretien :

> *Voici un extrait de modèle Odoo. Peux-tu expliquer ce que fait cette méthode ?*

Tu dois :

* Expliquer la logique Python
* Expliquer l’usage du décorateur
* Comprendre les champs utilisés

---

## 💡 Astuce : Ce que les recruteurs veulent voir

| Compétence           | Ce qu’ils vérifient                   |
| -------------------- | ------------------------------------- |
| Logique Python       | Bonne base en POO, syntaxe propre     |
| Connaissance d’Odoo  | Familiarité avec modèles, champs, API |
| Compréhension métier | Compréhension du contexte fonctionnel |
| Capacité à apprendre | Lecture, compréhension de code        |
| Propreté du code     | Variables claires, logique lisible    |

---

## 📚 Tu veux t’entraîner comme en vrai entretien ?

