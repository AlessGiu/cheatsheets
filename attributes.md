
---

## 🔐 1. `groups` : **restreindre l’accès à certains champs selon les droits utilisateurs**

### ✅ À quoi ça sert ?

Tu peux **cacher ou rendre accessible un champ uniquement pour certains groupes** d'utilisateurs (ex. : `stable.group_manager`, `base.group_user`, `account.group_account_manager`, etc.).

---

### 📌 Exemple :

```python
medical_notes = fields.Text(
    string="Notes vétérinaires",
    groups="stable.group_stable_manager"
)
```

👉 Seuls les utilisateurs du **groupe `stable.group_stable_manager`** verront ce champ.

---

### 👀 Où trouver le nom du groupe ?

Tu peux utiliser :

* Des groupes existants (`base.group_user`, `base.group_system`)
* Ou créer les tiens dans ton `security/ir.model.access.csv` ou dans les vues XML.

---

## 🔍 2. `domain` : **filtrer dynamiquement les valeurs affichées dans un champ**

### ✅ À quoi ça sert ?

Quand tu as un champ `Many2one`, tu peux **filtrer les valeurs possibles** selon certaines conditions.

---

### 📌 Exemple dans ton module écurie :

Imaginons un champ `veterinarian_id` lié à des employés Odoo :

```python
veterinarian_id = fields.Many2one(
    'hr.employee',
    string="Vétérinaire attitré",
    domain="[('job_title', 'ilike', 'vétérinaire')]"
)
```

👉 Résultat : dans le champ, **seuls les employés dont le titre contient "vétérinaire"** seront affichés.

---

### ✨ Domain dynamique (en fonction d’un autre champ) :

Ex. : tu veux sélectionner une ration disponible **uniquement pour l’espèce du cheval** :

```python
ration_id = fields.Many2one(
    'stable.ration',
    string="Ration",
    domain="[('species', '=', species)]"
)
```

⚠️ Attention, ici `species` doit être un champ du même modèle.

---

## ⚰️ 3. `ondelete` : **comportement quand l’objet parent est supprimé**

### ✅ À quoi ça sert ?

Quand tu as une relation `Many2one`, que se passe-t-il si **l'objet lié est supprimé** ?
Tu choisis ça avec `ondelete`.

---

### 🔧 Valeurs possibles :

| Valeur     | Comportement                                                   |
| ---------- | -------------------------------------------------------------- |
| `cascade`  | Supprime les enregistrements enfants en même temps             |
| `set null` | Met le champ à `False` (vide)                                  |
| `restrict` | Empêche la suppression si des enregistrements enfants existent |

---

### 📌 Exemple dans ton module écurie :

```python
owner_id = fields.Many2one(
    'res.partner',
    string="Propriétaire",
    ondelete='set null'
)
```

👉 Si le partenaire est supprimé, `owner_id` est mis à vide.

Autre exemple :

```python
stable_id = fields.Many2one(
    'stable.stable',
    string="Écurie",
    ondelete='restrict'
)
```

👉 Impossible de supprimer une écurie si des chevaux y sont encore associés.

---

## 🧠 Résumé rapide

| Attribut   | Sert à...                             | Exemple                                                              |
| ---------- | ------------------------------------- | -------------------------------------------------------------------- |
| `groups`   | Restreindre l’accès selon les droits  | `groups="stable.group_manager"`                                      |
| `domain`   | Filtrer les valeurs visibles          | `domain="[('species', '=', species)]"`                               |
| `ondelete` | Gérer la suppression d’un lien parent | `ondelete='restrict'` / `ondelete='set null'` / `ondelete='cascade'` |

---
