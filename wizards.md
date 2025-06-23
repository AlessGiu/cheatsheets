Voici la traduction complète du texte en français :

---

Un **wizard** dans Odoo est un type spécial de modèle transitoire (`transient.model`) utilisé pour créer des boîtes de dialogue interactives (pop-ups) pour les utilisateurs. Ils sont généralement utilisés pour des opérations temporaires : confirmations, imports de données, actions en masse ou formulaires en plusieurs étapes.

---

### 1. Qu'est-ce qu'un Wizard ?

- **Un modèle temporaire** : Les données ne sont pas stockées de manière permanente dans la base de données.
- **Interaction utilisateur** : Utilisé pour des pop-ups, des assistants ou des formulaires en plusieurs étapes.
- **Cas d'usage courants** : Confirmations, actions groupées, import/export de données, processus guidés.

---

### 2. Quand utiliser un Wizard ?

- Lorsque vous avez besoin d'un pop-up pour recueillir des informations utilisateur avant une action spécifique.
- Pour des processus en plusieurs étapes (ex. : un assistant de configuration).
- Pour des actions en masse sur des enregistrements (ex. : modifier plusieurs enregistrements à la fois).

---

### 3. Comment créer un Wizard ?

#### a) Définir le modèle du Wizard

Utilisez `models.TransientModel` au lieu de `models.Model`.

```python
# custom_module/wizards/my_wizard.py
from odoo import models, fields, api

class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _description = 'Mon exemple de Wizard'

    name = fields.Char('Nom')
    description = fields.Text('Description')

    def action_confirm(self):
        # Votre logique ici
        return {'type': 'ir.actions.act_window_close'}
```

#### b) Créer la vue du Wizard

```xml
<!-- custom_module/views/my_wizard_views.xml -->
<odoo>
  <record id="view_my_wizard_form" model="ir.ui.view">
    <field name="name">my.wizard.form</field>
    <field name="model">my.wizard</field>
    <field name="arch" type="xml">
      <form string="Mon Wizard">
        <group>
          <field name="name"/>
          <field name="description"/>
        </group>
        <footer>
          <button string="Confirmer" type="object" name="action_confirm" class="btn-primary"/>
          <button string="Annuler" special="cancel" class="btn-secondary"/>
        </footer>
      </form>
    </field>
  </record>
</odoo>
```

#### c) Ajouter une action pour ouvrir le Wizard

```xml
<record id="action_my_wizard" model="ir.actions.act_window">
  <field name="name">Mon Wizard</field>
  <field name="res_model">my.wizard</field>
  <field name="view_mode">form</field>
  <field name="target">new</field> <!-- 'new' = pop-up -->
</record>
```

#### d) Ajouter un bouton pour lancer le Wizard

Exemple : Ajouter un bouton dans un autre modèle pour ouvrir le wizard.

```xml
<button name="%(action_my_wizard)d" string="Ouvrir le Wizard" type="action" class="btn-primary"/>
```

---

### 4. Points clés

- **TransientModel** : Les données sont automatiquement supprimées (pas de stockage permanent).
- **target="new"** : Ouvre le wizard sous forme de boîte de dialogue modale.
- **Boutons** : Utilisez `type="object"` pour les méthodes Python, `special="cancel"` pour fermer.

---

### 5. Exemples d'utilisation

- Confirmation d'une commande de vente.
- Mise à jour groupée d'enregistrements.
- Import de données avec saisie utilisateur.
- Assistant de configuration en plusieurs étapes.

---

### 6. Conseils

- Utilisez toujours `TransientModel` pour les wizards.
- Nettoyez après vous : les wizards sont supprimés automatiquement, mais évitez d'y stocker des données sensibles.
- Utilisez `return {'type': 'ir.actions.act_window_close'}` pour fermer le wizard.

---

**Résumé :**  
Les wizards sont des pop-ups temporaires et interactifs dans Odoo, idéaux pour des actions guidées ou des opérations en masse. Définissez un `TransientModel`, créez une vue formulaire et déclenchez-le via une action pour une expérience utilisateur fluide.

--- 

J'espère que cette traduction vous sera utile ! Si vous avez besoin de précisions ou d'adaptations, n'hésitez pas à me le dire.