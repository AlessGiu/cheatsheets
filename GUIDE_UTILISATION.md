# 🐎 Guide d'Utilisation - FFE Competition Scraper

## 🚀 Démarrage Rapide

### 1. Test de Base (Sans Installation)
```bash
python3 demo_simple.py
```
Ce script teste la connectivité et fonctionne avec Python standard.

### 2. Installation Complète
```bash
./start.sh
```
Le script interactif guide l'installation et le démarrage.

### 3. Utilisation Manuelle

#### Installation des dépendances
```bash
pip install requests beautifulsoup4 flask pandas lxml
```

#### Lancer l'interface web
```bash
python3 app.py
```
Puis aller sur: http://localhost:5000

## 🔍 Exemples de Recherche

### Rechercher les épreuves "E" (Endurance)
```python
from ffe_scraper import FFEScraper

scraper = FFEScraper()
endurance = scraper.search_competitions_by_discipline('E')

print(f"Trouvé {len(endurance)} compétitions d'endurance")
for comp in endurance[:5]:
    print(f"- {comp['nom']} à {comp['lieu']}")
```

### Export CSV
```python
# Sauvegarder les résultats
scraper.save_to_csv(endurance, 'endurance_concours.csv')
```

## 🌐 Interface Web

### Page d'Accueil (/)
- ✅ Recherche par discipline
- ✅ Filtres rapides (E, D, CSO, CCE, etc.)
- ✅ Barre de recherche textuelle
- ✅ Export CSV des résultats

### Recherche Avancée (/search)
- ✅ Filtres multiples (discipline, niveau, région, statut)
- ✅ Vue cartes et tableau
- ✅ Tri par colonnes
- ✅ Statistiques temps réel

## 📋 Disciplines Disponibles

| Code | Nom Complet |
|------|-------------|
| **E** | Endurance |
| **D** | Dressage |
| **CSO** | Concours de Saut d'Obstacles |
| **CCE** | Concours Complet d'Équitation |
| **TREC** | Techniques de Randonnée Équestre |
| **ATT** | Attelage |
| **VOL** | Voltige |
| **EE** | Équitation Éthologique |

## 🛠️ Dépannage

### Problème d'installation
```bash
# Si les dépendances ne s'installent pas
pip install --user requests beautifulsoup4 flask pandas

# Ou avec break-system-packages
pip install --break-system-packages requests beautifulsoup4 flask pandas
```

### Erreur de connexion
- Vérifiez votre connexion internet
- Le site FFE peut être temporairement indisponible
- Testez avec: `python3 demo_simple.py`

### Import Error
```bash
# Vérifiez que Python trouve les modules
python3 -c "import requests, bs4, flask, pandas; print('OK')"
```

## 📊 Structure des Données

Chaque compétition contient:
```python
{
    'nom': 'Nom du concours',
    'discipline': 'E',  # Code discipline
    'niveau': 'Amateur',
    'date': '2024-01-15',
    'lieu': 'Ville, Département',
    'organisateur': 'Club',
    'statut': 'Ouvert',
    'url': 'https://ffecompet.ffe.com/...'
}
```

## 🔧 Personnalisation

### Ajouter une discipline
Modifiez `ffe_scraper.py`, méthode `get_disciplines_list()`:
```python
disciplines = [
    'E', 'D', 'CSO', 'CCE',
    'VOTRE_NOUVELLE_DISCIPLINE'
]
```

### Changer le port web
Dans `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## ⚡ Commandes Utiles

```bash
# Test rapide
python3 demo_simple.py

# Installation et démarrage interactif
./start.sh

# Démarrage direct de l'interface web
python3 app.py

# Test du scraper complet
python3 test_scraper.py

# Recherche spécifique en ligne de commande
python3 -c "
from ffe_scraper import FFEScraper
scraper = FFEScraper()
results = scraper.search_competitions_by_discipline('E')
print(f'Trouvé {len(results)} compétitions')
"
```

## 📱 Utilisation Mobile

L'interface web est responsive et fonctionne sur mobile:
- Adaptée aux petits écrans
- Filtres tactiles
- Navigation simple

---

💡 **Conseil**: Commencez par `python3 demo_simple.py` pour tester la connectivité, puis utilisez `./start.sh` pour l'installation complète.