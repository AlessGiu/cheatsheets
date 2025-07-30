# FFE Competition Scraper & Web Interface

🐎 **Extracteur et interface web pour les compétitions équestres FFE**

Ce projet permet d'extraire les données des concours équestres depuis le site [ffecompet.ffe.com](https://ffecompet.ffe.com/concours) et de les filtrer par disciplines (E, D, CSO, etc.) via une interface web simple et intuitive.

## 🚀 Fonctionnalités

- **Extraction automatique** des données de concours FFE
- **Filtrage par disciplines** (Endurance, Dressage, CSO, CCE, etc.)
- **Interface web moderne** avec recherche et filtres
- **Export CSV** des résultats
- **Recherche textuelle** par nom, lieu, organisateur
- **Vue cartes et tableau** pour l'affichage des résultats

## 📋 Disciplines Supportées

| Code | Discipline |
|------|------------|
| **E** | Endurance |
| **D** | Dressage |
| **CSO** | Concours de Saut d'Obstacles |
| **CCE** | Concours Complet d'Équitation |
| **TREC** | Techniques de Randonnée Équestre de Compétition |
| **PTV** | Pony-Trot-Voltige |
| **ATT** | Attelage |
| **VOL** | Voltige |
| **EE** | Équitation Éthologique |
| **POLO** | Polo |
| **HORSE** | Horse-Ball |

## 🛠️ Installation

### Prérequis

- Python 3.8 ou plus récent
- Connexion internet pour accéder au site FFE

### Installation des dépendances

```bash
# Cloner ou télécharger le projet
git clone <repository-url>
cd ffe-competition-scraper

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances principales

- `requests` - Pour les requêtes HTTP
- `beautifulsoup4` - Pour l'analyse HTML
- `flask` - Pour l'interface web
- `pandas` - Pour la manipulation des données
- `lxml` - Parser XML/HTML rapide

## 🏃‍♂️ Utilisation

### 1. Test du scraper

Vérifiez que tout fonctionne correctement :

```bash
python test_scraper.py
```

### 2. Utilisation en ligne de commande

```python
from ffe_scraper import FFEScraper

# Initialiser le scraper
scraper = FFEScraper()

# Rechercher les compétitions d'endurance
endurance_competitions = scraper.search_competitions_by_discipline('E')

# Obtenir toutes les compétitions
all_competitions = scraper.get_all_competitions(max_pages=5)

# Sauvegarder en CSV
scraper.save_to_csv(endurance_competitions, 'endurance_concours.csv')
```

### 3. Interface Web

Lancez l'interface web pour une utilisation interactive :

```bash
python app.py
```

Puis ouvrez votre navigateur sur : `http://localhost:5000`

## 🌐 Interface Web

### Page d'accueil (`/`)
- Recherche simple par discipline
- Filtres rapides
- Affichage en cartes
- Export CSV

### Recherche avancée (`/search`)
- Filtres multiples (discipline, niveau, région, statut, période)
- Vue cartes et tableau
- Tri par colonnes
- Statistiques en temps réel

## 📊 Données Extraites

Chaque compétition contient les informations suivantes :

```python
{
    'nom': 'Nom du concours',
    'discipline': 'E',  # Code discipline
    'niveau': 'Amateur/Pro/Elite',
    'date': '2024-01-15',
    'lieu': 'Ville, Département',
    'organisateur': 'Club organisateur',
    'statut': 'Ouvert/Clos/Complet',
    'url': 'https://ffecompet.ffe.com/...'
}
```

## 🔧 Configuration Avancée

### Personnaliser les disciplines

Modifiez la méthode `get_disciplines_list()` dans `ffe_scraper.py` :

```python
def get_disciplines_list(self):
    disciplines = [
        'E',      # Endurance
        'D',      # Dressage
        'CSO',    # Saut d'Obstacles
        # Ajoutez vos disciplines personnalisées
    ]
    return disciplines
```

### Ajuster le scraping

- **Pagination** : Modifiez `max_pages` dans les appels de méthodes
- **Délais** : Ajustez `time.sleep()` pour être respectueux du serveur
- **Headers** : Personnalisez les headers HTTP dans `__init__()`

## 🚨 Limitations et Bonnes Pratiques

### Respect du site web
- Le scraper inclut des délais entre les requêtes
- Limitez le nombre de pages récupérées
- Respectez les conditions d'utilisation du site FFE

### Gestion des erreurs
- Le script gère les erreurs de connectivité
- Les données manquantes sont marquées comme `N/A`
- Logs détaillés pour le débogage

### Performance
- Utilisez la mise en cache pour éviter les requêtes répétées
- Limitez les requêtes simultanées
- Sauvegardez régulièrement les données extraites

## 📁 Structure du Projet

```
ffe-competition-scraper/
├── ffe_scraper.py          # Module principal de scraping
├── app.py                  # Application Flask
├── test_scraper.py         # Tests et validation
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
├── templates/             # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   └── search.html       # Recherche avancée
└── static/               # Fichiers statiques (créé automatiquement)
    ├── css/
    └── js/
```

## 🔍 Exemple d'Usage - Recherche d'Endurance

```python
from ffe_scraper import FFEScraper

# Créer une instance du scraper
scraper = FFEScraper()

# Rechercher toutes les compétitions d'endurance
print("Recherche des compétitions d'endurance...")
endurance = scraper.search_competitions_by_discipline('E')

print(f"Trouvé {len(endurance)} compétitions d'endurance")

# Afficher les 5 premières
for comp in endurance[:5]:
    print(f"- {comp['nom']} à {comp['lieu']} le {comp['date']}")

# Sauvegarder en CSV
scraper.save_to_csv(endurance, 'endurance_2024.csv')
print("Données sauvegardées dans endurance_2024.csv")
```

## 🛡️ Disclaimer

Ce projet est développé à des fins éducatives et de recherche. Il utilise les données publiquement disponibles sur le site ffecompet.ffe.com. 

- Respectez les conditions d'utilisation du site FFE
- N'abusez pas des requêtes automatiques
- Utilisez les données de manière responsable

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez votre connexion internet
2. Assurez-vous que toutes les dépendances sont installées
3. Consultez les logs d'erreur
4. Testez avec `test_scraper.py`

## 📝 Changelog

### Version 1.0.0
- ✅ Extraction des données FFE
- ✅ Filtrage par disciplines
- ✅ Interface web avec Flask
- ✅ Export CSV
- ✅ Recherche avancée
- ✅ Documentation complète

---

**Développé avec ❤️ pour la communauté équestre française**