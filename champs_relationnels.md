
---

## 📌 1. C’est quoi un **champ relationnel** dans Odoo ?

Un **champ relationnel** est un champ **qui lie deux modèles entre eux**.
Il permet de **connecter des données** et de **naviguer** entre les objets.

> Tu ne stockes pas une simple valeur (comme du texte), tu **références un autre enregistrement**.

Exemple concret :

* Un employé travaille dans un département → tu fais une **relation entre le modèle `hr.employee` et `hr.department`**.

---

## 📦 2. Les **3 types de relations** possibles

| Type        | Utilisation               | Logique base de données | Exemples                                  |
| ----------- | ------------------------- | ----------------------- | ----------------------------------------- |
| `Many2one`  | Plusieurs A → 1 B         | Clé étrangère dans A    | "Plusieurs rations pour un cheval"        |
| `One2many`  | 1 A → plusieurs B         | Champ inverse           | "Un cheval a plusieurs rations"           |
| `Many2many` | Plusieurs A ↔ Plusieurs B | Table de liaison        | "Un cheval vu par plusieurs vétérinaires" |

---

## 🧠 3. Pourquoi utiliser un champ relationnel ?

### ✨ Avantages :

✅ Évite les redondances (normalisation)
✅ Permet de **naviguer dans l'interface** (liens dynamiques)
✅ Permet de **filtrer, grouper, agréger facilement**
✅ Permet de faire des vues imbriquées (onglets, listes intégrées)
✅ Donne de la **structure logique** à ton modèle métier

---

## 🧰 4. Quand faut-il en utiliser un ?

Voici **les cas typiques** où tu dois penser à un champ relationnel :

### ✔️ 1. Tu veux **relier deux modèles**

> Une ration est liée à un cheval → champ `Many2one`

### ✔️ 2. Tu veux afficher **une liste d’objets liés**

> Un cheval a plusieurs rations → champ `One2many`

### ✔️ 3. Tu veux une **relation bidirectionnelle multiple**

> Plusieurs chevaux sont suivis par plusieurs vétérinaires → `Many2many`

---

## ⚙️ 5. Comment les implémenter (structure générique)

### 🔹 `Many2one` (relation simple vers un autre objet)

```python
champ = fields.Many2one('nom.modele', string="Nom affiché")
```

💬 *"Ce modèle est lié à UN autre modèle"*

---

### 🔹 `One2many` (relation inverse du `Many2one`)

```python
champ_ids = fields.One2many('modele.enfant', 'champ_many2one', string="Enfants")
```

💬 *"Ce modèle possède plusieurs objets de l’autre modèle"*

---

### 🔹 `Many2many` (relation symétrique)

```python
champ_ids = fields.Many2many('nom.modele', string="Liste liée")
```

💬 *"Ce modèle peut être lié à plusieurs objets, et inversement"*

---

## 🧾 6. Conditions / règles à respecter

| Règle                                                       | Explication                                              |
| ----------------------------------------------------------- | -------------------------------------------------------- |
| ⚠️ `One2many` doit toujours avoir un `Many2one` en face     | Sinon Odoo ne saura pas sur quoi faire la liaison        |
| `Many2one` crée une **clé étrangère** en BDD                | Et la stocke dans la table du modèle courant             |
| `Many2many` crée une **table intermédiaire automatique**    | Sauf si tu la définis toi-même                           |
| Les noms de champs doivent rester **logiques et cohérents** | ex : `horse_id` côté `ration`, `ration_ids` côté `horse` |
| Tu peux utiliser `ondelete='cascade'` ou `'set null'`       | Pour contrôler le comportement lors d'une suppression    |

---

## 📐 7. Diagramme visuel (simplifié)

```
[Cheval] <1---n> [Ration]
         (One2many)      (Many2one)
```

```
[Cheval] <n---n> [Vétérinaire]
         (Many2many)
```

---

## 📝 Résumé en phrases claires

* **Use `Many2one`** quand tu veux dire "cet objet appartient à un autre"
* **Use `One2many`** quand tu veux dire "cet objet contient plusieurs autres"
* **Use `Many2many`** quand les deux objets peuvent avoir plusieurs liens entre eux
* Toujours créer **le côté `Many2one` en premier**, le reste suit

---

