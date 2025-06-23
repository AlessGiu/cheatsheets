
---

## ⚙️ Odoo ORM – C’est quoi d’abord ?

Quand tu codes dans Odoo, tu travailles avec des **modèles** Python qui sont liés à des **tables SQL**.
Par exemple :

```python
class Horse(models.Model):
    _name = 'stable.horse'
```

Ce modèle correspond à une table SQL qui contient **des chevaux**.
Et grâce à l’ORM d’Odoo (Object Relational Mapper), tu peux manipuler la base **sans jamais écrire une seule ligne de SQL.**

---

## 🧩 Les 3 MÉTHODES DE BASE : `create`, `write`, `unlink`

### ✨ 1. `create(vals)` → Créer une fiche

Imagine que tu veux **ajouter un cheval** dans ton écurie.
Tu dois **remplir un formulaire avec ses infos** : nom, âge, race, etc.
En code, c’est ce que fait `create`.

### ▶️ Exemple concret :

```python
self.env['stable.horse'].create({
    'name': 'Tornado',
    'age': 7,
    'breed': 'Selle Français'
})
```

🔹 `self.env['stable.horse']` → C’est le modèle
🔹 `.create({...})` → Crée une nouvelle fiche cheval avec les champs indiqués

> 🧠 En base de données, ça va créer une **nouvelle ligne** dans la table `stable_horse`.

---

### ✏️ 2. `write(vals)` → Modifier une fiche

Tu veux **modifier un cheval existant** ? Tu fais un `write`.
C’est comme **éditer une fiche** dans l’interface Odoo.

### ▶️ Exemple concret :

```python
cheval = self.env['stable.horse'].browse(5)
cheval.write({
    'age': 8
})
```

🔹 `.browse(5)` → Va chercher le cheval avec l’ID 5
🔹 `.write({...})` → Met à jour les champs passés en argument

> 🧠 En SQL, ça fait un `UPDATE` sur la ligne avec l’ID 5.

---

### ❌ 3. `unlink()` → Supprimer une fiche

Tu veux **supprimer un cheval** ? Tu fais un `unlink`.

### ▶️ Exemple concret :

```python
cheval = self.env['stable.horse'].browse(5)
cheval.unlink()
```

🔹 Supprime totalement la fiche du cheval (⚠️ définitif !)

> 🧠 En SQL, ça fait un `DELETE FROM stable_horse WHERE id = 5`

---

## 🔄 POURQUOI LES SURCHARGER (override) ?

En tant que dev sénior, on surcharge ces méthodes quand on veut :

| 🎯 Besoin métier                                            | 👉 Solution           |
| ----------------------------------------------------------- | --------------------- |
| Exécuter une action quand un cheval est créé                | `create()`            |
| Vérifier une condition avant d'enregistrer une modification | `write()`             |
| Interdire la suppression de certains chevaux                | `unlink()`            |
| Remplir un champ automatiquement                            | `create()`            |
| Envoyer une notification                                    | `create()`, `write()` |

---

## 💡 Surcharge dans ton module écurie : exemples commentés

---

### ✅ Surcharge de `create` : ajouter un identifiant automatique

```python
from odoo import models, api, _
from odoo.exceptions import UserError

class Horse(models.Model):
    _name = 'stable.horse'

    @api.model
    def create(self, vals):
        # S'il n'y a pas d'identifiant, on le génère automatiquement
        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('stable.horse') or _('New')
        
        res = super().create(vals)
        _logger.info(f"Cheval créé : {res.name}")
        return res
```

---

### ✅ Surcharge de `write` : interdire un âge négatif

```python
def write(self, vals):
    for record in self:
        if 'age' in vals and vals['age'] < 0:
            raise UserError("L'âge d'un cheval ne peut pas être négatif.")
    return super().write(vals)
```

---

### ✅ Surcharge de `unlink` : interdire de supprimer un cheval s’il a des rations

```python
def unlink(self):
    for record in self:
        if record.ration_ids:
            raise UserError("Impossible de supprimer un cheval qui a des rations attribuées.")
    return super().unlink()
```

---

## 🧠 Résumé simplifié

| Méthode    | Quand tu l'utilises                  | Que fait-elle ? | Tu la surcharges pour…                     |
| ---------- | ------------------------------------ | --------------- | ------------------------------------------ |
| `create()` | Quand tu ajoutes un enregistrement   | INSERT en base  | Ajouter des règles ou valeurs automatiques |
| `write()`  | Quand tu modifies un enregistrement  | UPDATE en base  | Vérifier ou réagir aux modifications       |
| `unlink()` | Quand tu supprimes un enregistrement | DELETE en base  | Bloquer certaines suppressions             |

---

## 🧪 Tester tout ça (console développeur Odoo)

Va dans Odoo → `Paramètres` → `Technique` → `Console développeur` ou active-la dans l'interface dev :

```python
# Créer
env['stable.horse'].create({'name': 'Spirit', 'age': 4})

# Modifier
horse = env['stable.horse'].browse(2)
horse.write({'age': 5})

# Supprimer
horse.unlink()
```

---

