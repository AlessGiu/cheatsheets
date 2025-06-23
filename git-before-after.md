
---

## ✅ AVANT DE TRAVAILLER : Check-in

| Étape                                         | Pourquoi                               | Commande / Action                                   |
| --------------------------------------------- | -------------------------------------- | --------------------------------------------------- |
| 1️⃣ `cd` vers ton dossier projet              | Te placer au bon endroit               | `cd ~/odoo-dev/ton-module`                          |
| 2️⃣ Vérifie si Git est bien là                | Pas de versioning = danger             | `git status`                                        |
| 3️⃣ Récupère les dernières modifs             | Toujours travailler sur du code à jour | `git pull origin ta-branche`                        |
| 4️⃣ Active ton environnement Python (si venv) | Évite les erreurs de dépendance        | `source venv/bin/activate`                          |
| 5️⃣ Lance ton serveur Odoo                    | Pour tester dès que tu codes           | `./odoo-bin -d ta_db -u ton_module`                 |
| 6️⃣ Vérifie les logs Odoo                     | Si erreur au démarrage                 | `tail -f logs/odoo.log` ou observe dans le terminal |

> 💡 Bonus : si tu bosses sur une branche **partagée**, vérifie avec ton équipe s’il y a eu des **modifs manuelles ou conflits récents**.

---

## ✅ APRÈS AVOIR TRAVAILLÉ : Check-out

| Étape                      | Pourquoi                                     | Commande / Action                                               |
| -------------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| 1️⃣ Vérifie `git status`   | Voir ce que tu as modifié                    | `git status`                                                    |
| 2️⃣ Ajoute et commit       | Sauvegarder ton travail localement           | `git add . && git commit -m "feat: vue Kanban rations chevaux"` |
| 3️⃣ Push sur GitHub        | Sauvegarde distante + partage avec l’équipe  | `git push origin ta-branche`                                    |
| 4️⃣ Désactive ton venv     | Remettre ton environnement propre            | `deactivate`                                                    |
| 5️⃣ Note ce que tu as fait | Pour le rapport de stage, le scrum ou Jira   | 2 lignes max dans un fichier `journal.md` ou Notion             |
| 6️⃣ Ferme proprement       | Pas de processus Odoo qui tournent pour rien | `ctrl + c`, `exit`, éteindre Docker, etc.                       |

---

## 🧠 Résumé visuel (checklist rapide)

### ✅ AVANT :

* [ ] `git pull`
* [ ] `git status`
* [ ] `source venv/bin/activate`
* [ ] Lancer Odoo
* [ ] Vérifier les logs

### ✅ APRÈS :

* [ ] `git status`
* [ ] `git add`, `commit`, `push`
* [ ] `deactivate`
* [ ] Noter ce que j’ai fait
* [ ] Fermer Odoo

---

## 📦 Bonus : Script "start\_dev.sh" et "stop\_dev.sh"

Tu peux même automatiser tout ça :

```bash
# start_dev.sh
#!/bin/bash
cd ~/odoo-dev/ton-module
git pull origin ta-branche
source ../venv/bin/activate
./odoo-bin -d ta_db -u ton_module
```

```bash
# stop_dev.sh
#!/bin/bash
git add .
git commit -m "WIP: sauvegarde fin de session"
git push origin ta-branche
deactivate
```

---
