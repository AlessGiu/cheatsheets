
---

## 🧠 C’est quoi une action planifiée (cron) dans Odoo ?

Une **action planifiée (cron)** est une **tâche automatique** qu’Odoo exécute à intervalle régulier (toutes les heures, tous les jours, toutes les minutes, etc.).

En backend, c’est un job qui :

* est stocké dans le modèle `ir.cron`
* peut appeler n’importe quelle méthode Python de ton module
* s’exécute **en tâche de fond** grâce à l’horloge (`cron`) du système et le `odoo-bin` qui tourne

---

## 🧰 À quoi ça sert ?

Quelques exemples concrets dans ton **module d’écurie** :

* ⏰ Mettre à jour automatiquement l’état de santé des chevaux chaque nuit
* 📦 Vérifier chaque matin s’il manque de la nourriture ou du matériel
* 🐴 Envoyer un email hebdo au gérant de l’écurie avec un rapport de rations
* 🚨 Créer des alertes si un cheval n’a pas été nourri depuis plus de 24h

---

## 🧑‍💻 Comment implémenter un `cron` dans ton module Odoo ?

Tu as deux étapes :

---

### **1. Écrire la méthode Python**

Exemple : on va créer une méthode qui vérifie si un cheval n’a pas mangé depuis 24h.

```python
from odoo import models, fields, api
from datetime import datetime, timedelta

class StableHorse(models.Model):
    _name = 'stable.horse'
    _description = 'Horse'

    name = fields.Char()
    last_fed = fields.Datetime(string="Dernier repas")
    alert = fields.Boolean(string="Alerte !", default=False)

    def check_feeding_alert(self):
        """Active l'alerte si le cheval n'a pas mangé depuis +24h"""
        threshold = datetime.now() - timedelta(hours=24)
        horses = self.search([('last_fed', '<=', threshold)])
        horses.write({'alert': True})
```

---

### **2. Créer un fichier `data/cron.xml` pour enregistrer la tâche**

```xml
<!-- data/cron.xml -->
<odoo>
  <data noupdate="1">

    <record id="ir_cron_check_horse_feeding" model="ir.cron">
      <field name="name">Check Horse Feeding</field>
      <field name="model_id" ref="module_name.model_stable_horse"/>
      <field name="state">code</field>
      <field name="code">model.check_feeding_alert()</field>
      <field name="interval_number">1</field>
      <field name="interval_type">hours</field>
      <field name="numbercall">-1</field> <!-- infini -->
      <field name="active">True</field>
    </record>

  </data>
</odoo>
```

N’oublie pas d’ajouter ce fichier dans ton `__manifest__.py` :

```python
'data': [
    'data/cron.xml',
],
```

---

## 🔍 Que font ces champs dans `ir.cron` ?

| Champ                               | Rôle                                         |
| ----------------------------------- | -------------------------------------------- |
| `model_id`                          | modèle sur lequel appeler la méthode         |
| `code`                              | code exécuté (souvent `model.ma_methode()` ) |
| `interval_number` + `interval_type` | fréquence d’exécution                        |
| `numbercall = -1`                   | signifie que ça s'exécute **à l’infini**     |
| `active = True`                     | doit être actif sinon ne s’exécute jamais    |

---

## 🧪 Debug & test

1. Va dans Odoo > Paramètres > Technique > Actions planifiées
2. Tu verras ta tâche "Check Horse Feeding"
3. Tu peux cliquer sur **"Exécuter manuellement"** pour tester
4. Regarde les logs du serveur pour les erreurs

---

## ✅ Résumé

| Étape | Action                                           |
| ----- | ------------------------------------------------ |
| 1     | Écris une méthode dans ton modèle                |
| 2     | Déclare la tâche dans un fichier XML (`ir.cron`) |
| 3     | Ajoute ce XML dans le `__manifest__`             |
| 4     | (Optionnel) Vérifie dans l’interface Odoo        |

---

