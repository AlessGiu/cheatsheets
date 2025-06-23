
---

# 🧠 1. Qu’est-ce que `_inherit` dans Odoo ?

L’attribut `_inherit` permet à un modèle de **reprendre et étendre un modèle existant** (natif ou personnalisé).

Tu peux :

| Action                         | Exemple                           |
| ------------------------------ | --------------------------------- |
| Ajouter un champ               | `ajouter une photo à res.partner` |
| Modifier une méthode           | `personnaliser le create()`       |
| Ajouter un bouton, une statbox | `ajouter un bouton à la vue form` |

➡️ C’est **l’héritage structurel**, c’est-à-dire que tu continues à **utiliser le même modèle**, mais tu **l’enrichis**.

---

# 🧩 2. Comment fonctionne `_inherit` techniquement ?

```python
class MonExtension(models.Model):
    _inherit = 'stable.horse'

    # champs supplémentaires
    champ_x = fields.Boolean()
```

Cela **n’ajoute pas un nouveau modèle**. Cela **modifie l'existant**, comme si tu faisais un patch.

Il n’y a **pas de `_name`** défini ici (sinon, tu changes de modèle).

---

# 🛠️ 3. Tutoriel pas-à-pas – Étendre un modèle avec `_inherit`

## 🎯 Objectif : Ajouter une colonne "identifiant unique" et un champ "photo" au modèle `stable.horse`

### Étape 1 – Fichier Python

```python
# models/stable_horse.py

from odoo import models, fields

class HorseExtension(models.Model):
    _inherit = 'stable.horse'

    identifiant_unique = fields.Char(string="Identifiant Unique")
    photo = fields.Binary(string="Photo du cheval")
```

✅ On ne déclare **pas** de `_name` ici
✅ `_inherit` correspond exactement au nom du modèle à étendre

---

### Étape 2 – Mise à jour de la vue XML

```xml
<!-- views/stable_horse_form.xml -->

<odoo>
    <record id="stable_horse_form_view_inherited" model="ir.ui.view">
        <field name="name">stable.horse.form.inherit</field>
        <field name="model">stable.horse</field>
        <field name="inherit_id" ref="mon_module.stable_horse_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//sheet/group" position="inside">
                <field name="identifiant_unique"/>
                <field name="photo"/>
            </xpath>
        </field>
    </record>
</odoo>
```

✅ On utilise `inherit_id` pour **hériter visuellement** de la vue
✅ On localise l’endroit d’injection avec `<xpath>`

---

### Étape 3 – Mise à jour du manifest (`__manifest__.py`)

```python
'data': [
    'views/stable_horse_form.xml',
],
```

---

### Étape 4 – Redémarre ton serveur Odoo et mets à jour ton module :

```bash
./odoo-bin -u mon_module -d ma_base
```

---

# 🔁 4. Surcharge de méthode (ex: `write`, `create`)

Tu peux personnaliser le comportement d’un modèle sans casser ce qui existe :

```python
class HorseExtension(models.Model):
    _inherit = 'stable.horse'

    def write(self, vals):
        res = super().write(vals)
        if 'identifiant_unique' in vals:
            self.message_post(body="Identifiant modifié.")
        return res
```

✅ Le `super()` appelle la méthode d’origine (de base)
✅ Tu ajoutes ta logique métier sans tout écraser

---

# 🧪 5. Exemple complet pour ton module `écurie`

Tu veux ajouter :

* un champ `dernier_soin`
* un champ `veto` (Many2one vers `res.partner`)
* un log à chaque update

```python
class HorseVetExtension(models.Model):
    _inherit = 'stable.horse'

    dernier_soin = fields.Date(string="Dernier soin")
    veto_id = fields.Many2one('res.partner', string="Vétérinaire")

    def write(self, vals):
        res = super().write(vals)
        if 'dernier_soin' in vals:
            self.message_post(body=f"Soin enregistré : {vals['dernier_soin']}")
        return res
```

---

# 🧨 6. Erreurs fréquentes à éviter

| Erreur                                      | Explication                                          |
| ------------------------------------------- | ---------------------------------------------------- |
| Oublier `super()`                           | Tu perds tout le comportement original               |
| Déclarer un `_name` avec `_inherit`         | Tu changes de modèle (c’est `_inherits` dans ce cas) |
| Mal écrire le nom du modèle dans `_inherit` | Odoo ne trouve pas le modèle à modifier              |
| Ne pas mettre à jour le XML correctement    | Le champ n’apparaîtra pas dans la vue                |

---

# 📌 7. Résumé / Fiche Mémo

### ✔ Pour étendre un modèle existant (res.partner, product.template, ton modèle, etc.) :

```python
class Extension(models.Model):
    _inherit = 'nom.du.modele'

    mon_champ = fields.Char()
```

### ✔ Pour modifier la vue liée :

```xml
<record id="view_inherited" model="ir.ui.view">
    <field name="inherit_id" ref="nom_du_module_vue_form"/>
    <field name="model">nom.du.modele</field>
    <field name="arch" type="xml">
        <xpath expr="//sheet/group" position="inside">
            <field name="mon_champ"/>
        </xpath>
    </field>
</record>
```

---

