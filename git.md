Parfait CK 👨‍💻 ! En tant que stagiaire Python/Odoo, si tu veux bien travailler en équipe et en entreprise, **maîtriser Git et GitHub** est **essentiel**. Voici **tout ce que tu dois savoir** pour travailler comme un vrai pro dès aujourd’hui.

---

## 🔧 1. Qu'est-ce que Git et GitHub ?

|                 | Git                                               | GitHub                                                 |
| --------------- | ------------------------------------------------- | ------------------------------------------------------ |
| **Définition**  | Un système de contrôle de version local           | Un hébergeur de dépôt Git en ligne                     |
| **Fonction**    | Suivre l'historique des modifications de ton code | Collaborer, stocker, partager, faire des pull requests |
| **Utilisation** | En local (terminal/git bash)                      | Sur le web (github.com) et via `git remote`            |

---

## 🧱 2. Les bases **indispensables**

### ✅ Config de départ (à faire **une seule fois**)

```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton.email@example.com"
```

### 📁 Initialiser un projet Git

```bash
git init         # Lance le suivi Git dans ton projet
```

### 📦 Suivre les fichiers

```bash
git add .        # Ajoute tous les fichiers modifiés pour commit
git add mon_fichier.py  # Ajoute un fichier spécifique
```

### 🧾 Enregistrer un commit

```bash
git commit -m "Ajout de la vue kanban pour les chevaux"
```

### 📜 Voir les changements

```bash
git status       # Voir les fichiers modifiés
git log          # Historique des commits
git diff         # Détails des modifications
```

---

## 🌐 3. Travailler avec GitHub

### 🔗 Lier ton dépôt local à GitHub

1. Crée un repo vide sur [GitHub](https://github.com)
2. Copie l’URL HTTPS ou SSH
3. Dans ton terminal :

```bash
git remote add origin https://github.com/TonUser/mon-projet.git
git push -u origin main  # Envoie le code
```

### 🔄 Récupérer ou mettre à jour depuis GitHub

```bash
git pull origin main     # Récupère les dernières modifs
git push origin main     # Envoie tes commits
```

---

## 🌿 4. Travailler proprement avec les **branches**

### 🔧 Pourquoi ?

* Ne jamais travailler directement sur `main`
* Facilite la collaboration et les tests

```bash
git checkout -b ma-branche-fonctionnalité
# ... tu travailles ...
git add .
git commit -m "Ajout de la fiche cheval"
git push origin ma-branche-fonctionnalité
```

> Tu peux ensuite faire une **pull request** (PR) sur GitHub pour intégrer ton travail dans `main`

---

## 🚀 5. Cas typique en entreprise (Exemple Odoo)

| Étape | Action                                                    |
| ----- | --------------------------------------------------------- |
| 1     | Tu crées une **branche** `ajout/vue-kanban` depuis `main` |
| 2     | Tu **codes** la fonctionnalité dans ton module Odoo       |
| 3     | Tu **commit** régulièrement avec des messages clairs      |
| 4     | Tu fais un `push`                                         |
| 5     | Tu crées une **pull request (PR)**                        |
| 6     | Ton tuteur vérifie, commente, et valide                   |
| 7     | Tu merges sur `main`                                      |

---

## ✍️ 6. Bonnes pratiques Git

* **Un commit = une idée claire**
* Toujours tester avant de pousser
* Jamais de `password` ou `key` dans Git
* Nom de branche explicite : `fix/bug-ration-affichage` ou `feat/vue-gantt`

---

## 🛡️ 7. Fichiers utiles

* `.gitignore` → pour exclure les fichiers inutiles :

```gitignore
*.pyc
__pycache__/
*.log
.env
.idea/
.vscode/
```

---

## 🧠 Résumé pour ton stage

| À maîtriser      | Commande                             |
| ---------------- | ------------------------------------ |
| Init dépôt       | `git init`                           |
| Suivi fichier    | `git add`                            |
| Commit           | `git commit -m "..."`                |
| Lien avec GitHub | `git remote add origin` + `git push` |
| Branche          | `git checkout -b ma-branche`         |
| Pull/Push        | `git pull`, `git push`               |
| Voir l’état      | `git status`, `git log`              |

---

## 🧰 Outils bonus à installer

* [GitHub Desktop](https://desktop.github.com/) (si tu préfères le visuel)
* VS Code avec l'extension **GitLens**
* Interface en ligne de commande : Git Bash ou terminal intégré

---

Si tu veux, je peux te faire un **mini pense-bête PDF** à coller à côté de ton écran 🔖. Tu veux ?

Et dis-moi aussi si tu veux qu’on fasse un **exercice pratique** ensemble (par exemple : créer une branche et faire une PR comme en entreprise).
