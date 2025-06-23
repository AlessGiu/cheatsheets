Voici la traduction du tutoriel sur `default` et `context` en Odoo :

---

## 1. Qu’est-ce que `default` ?

- `default` sert à définir une valeur par défaut pour un champ lors de la création d’un nouvel enregistrement ou d’un wizard.
- Cela peut être une valeur statique, une fonction, ou une valeur passée dynamiquement via le contexte.

**Exemple dans un modèle :**
```python
python
from odoo import models, fields

class MonModele(models.Model):
    _name = 'mon.modele'
    name = fields.Char(default='Nom par défaut')
    date = fields.Date(default=fields.Date.today)
```

---

## 2. Qu’est-ce que le `context` ?

- Le `context` est un dictionnaire qui transporte des informations supplémentaires lors des appels de méthodes, des actions et de l’affichage des vues.
- Il sert à passer des valeurs dynamiques, des préférences utilisateur ou à contrôler la logique (comme définir des valeurs par défaut).

**Exemple :**
- Quand tu ouvres un wizard via un bouton, tu peux passer des valeurs dans le contexte pour pré-remplir les champs.

---

## 3. Comment utiliser `default` et `context` ensemble

### a) Valeur par défaut statique en Python

```python
python
class MonWizard(models.TransientModel):
    _name = 'mon.wizard'
    name = fields.Char(default='Bonjour')
```

### b) Valeur par défaut dynamique via le contexte

```python
python
class MonWizard(models.TransientModel):
    _name = 'mon.wizard'
    partner_id = fields.Many2one('res.partner')
    name = fields.Char(default=lambda self: self.env.context.get('default_name', ''))

    def action_confirm(self):
        active_id = self.env.context.get('active_id')
        # Utiliser active_id pour la logique métier
```

### c) Passer des valeurs par défaut via le contexte dans une action

```xml
xml
<record id="action_mon_wizard" model="ir.actions.act_window">
    <field name="name">Mon Wizard</field>
    <field name="res_model">mon.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field>
    <field name="context">{'default_name': 'Nom pré-rempli', 'default_partner_id': active_id}</field>
</record>
```

---

## 4. Comment ça marche ?

- Quand tu ouvres un formulaire ou un wizard, Odoo regarde dans le contexte les clés comme `default_nom_champ`.
- Si trouvé, il utilise cette valeur comme valeur par défaut pour le champ.

---

## 5. Cas d’usage typiques

- Pré-remplir un wizard avec les données de l’enregistrement courant.
- Définir une société, une date ou un utilisateur par défaut.
- Passer des informations entre actions et wizards.

---

## 6. Points clés

- Utilise `default` dans la définition des champs pour des valeurs statiques ou calculées.
- Utilise le `context` pour passer des valeurs dynamiques, surtout dans les actions ou les appels de boutons.
- En Python, accède au contexte avec `self.env.context`.

---

**Résumé :**  
- `default` définit les valeurs initiales des champs.
- `context` transmet des infos dynamiques et peut définir des valeurs par défaut via `default_nom_champ`.
- Combine les deux pour des formulaires et wizards flexibles et conviviaux dans Odoo.