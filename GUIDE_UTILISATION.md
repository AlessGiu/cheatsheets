# 🐎 Guide d'Utilisation - FFE Competition Scraper

## 🚀 Démarrage Rapide - SOLUTION FONCTIONNELLE !

### ✅ 1. Application Simple (Fonctionne immédiatement)
```bash
python3 simple_app.py
```
**Interface en ligne de commande complète** - Aucune installation requise !

### ✅ 2. Test de Base
```bash
python3 test_ffe_simple.py
```
Test rapide qui affiche les statistiques et exemples.

### 3. Interface Web (Nécessite des dépendances)
```bash
pip install requests beautifulsoup4 flask pandas
python3 app.py
```

## 🎯 Application Simple - Mode d'Emploi

L'application `simple_app.py` fonctionne **sans aucune dépendance** et offre toutes les fonctionnalités :

### Menu Principal
```
🐎 FFE Competition Search - Menu Principal
==================================================
1. Charger les compétitions
2. Rechercher par discipline  
3. Recherche libre
4. Afficher les statistiques
5. Sauvegarder les résultats en CSV
6. Quitter
```

### Exemple d'Utilisation

1. **Lancez l'application** :
   ```bash
   python3 simple_app.py
   ```

2. **Chargez les données** (Option 1) :
   - Connecte au site FFE
   - Extrait ~3 300 compétitions
   - Durée : 5-10 secondes

3. **Recherchez par discipline** (Option 2) :
   - Tapez `E` pour Endurance → ~135 compétitions
   - Tapez `CSO` pour Saut d'Obstacles → ~1 143 compétitions  
   - Tapez `D` pour Dressage → ~566 compétitions

4. **Sauvegardez en CSV** (Option 5) :
   - Exporte les derniers résultats de recherche
   - Format : `ffe_competitions_YYYYMMDD_HHMMSS.csv`

## 📋 Disciplines Disponibles

| Code | Nom Complet | Nb Compétitions* |
|------|-------------|------------------|
| **E** | Endurance | ~135 |
| **D** | Dressage | ~566 |
| **CSO** | Saut d'Obstacles | ~1 143 |
| **CCE** | Complet | ~278 |
| **HU** | Hunter | ~306 |
| **AT** | Attelage | ~246 |
| **VO** | Voltige | ~90 |
| **WE** | Western | ~257 |
| **TREC** | TREC | ~5 |
| **PR** | Polo/Para | ~60 |

*Nombres approximatifs extraits lors des tests

## 🔍 Exemples de Recherche

### Recherche par Discipline "E" (Endurance)
```bash
python3 simple_app.py
# Choisir option 1 puis option 2
# Entrer: E
```

**Résultat** : Liste de toutes les compétitions d'endurance avec :
- Nom de la compétition
- Discipline (E)
- Niveau (Amateur, Pro, etc.)

### Recherche Textuelle
```bash
# Option 3 dans le menu
# Entrer: "Master"
```
Trouve toutes les compétitions contenant "Master" dans le nom.

## 📊 Données Extraites

Chaque compétition contient :
```json
{
    "id": "12345",
    "nom": "Master d'Endurance Amateur Elite GP (160 Km)",
    "discipline": "E",
    "niveau": "Amateur",
    "url": "https://ffecompet.ffe.com/concours/12345"
}
```

## 🛠️ Dépannage

### Erreur de connexion
```bash
❌ Erreur lors du chargement: [SSL: CERTIFICATE_VERIFY_FAILED]
```
**Solution** : Le site FFE peut être temporairement indisponible. Réessayez plus tard.

### Aucun résultat pour une discipline
- Vérifiez l'orthographe : `E`, `CSO`, `D` (sensible à la casse)
- Certaines disciplines peuvent avoir peu de compétitions

### Interface Web ne fonctionne pas
- Utilisez l'application simple : `python3 simple_app.py`
- Ou installez les dépendances : `pip install requests beautifulsoup4 flask pandas`

## ⚡ Commandes Rapides

```bash
# Test rapide (affiche statistiques)
python3 test_ffe_simple.py

# Application complète
python3 simple_app.py

# Interface web (si dépendances installées)
python3 app.py

# Recherche rapide Endurance depuis la ligne de commande
python3 -c "
import sys
sys.path.append('.')
from simple_app import FFECompetitionScraper
scraper = FFECompetitionScraper()
scraper.load_competitions()
results = scraper.search_by_discipline('E')
print(f'Trouvé {len(results)} compétitions d\\'endurance')
for i, comp in enumerate(results[:5]):
    print(f'{i+1}. {comp[\"nom\"]}')
"
```

## 🎯 Cas d'Usage Typiques

### Cavalier d'Endurance
1. Lancer `python3 simple_app.py`
2. Option 1 (Charger)
3. Option 2 (Rechercher) → `E`
4. Option 5 (Exporter CSV)

### Organisation de Concours  
1. Option 4 (Statistiques) pour voir la répartition
2. Option 3 (Recherche libre) → "votre région"
3. Analyser la concurrence

### Étude de Marché
1. Charger toutes les données
2. Exporter en CSV
3. Analyser dans Excel/LibreOffice

## 📱 Avantages de la Solution

✅ **Fonctionne immédiatement** - Aucune installation  
✅ **Données réelles** - ~3 300 compétitions extraites  
✅ **Filtrage efficace** - Par discipline et texte libre  
✅ **Export CSV** - Pour analyse dans Excel  
✅ **Interface simple** - Menu en ligne de commande  
✅ **Rapide** - Chargement en 5-10 secondes  

---

💡 **Conseil** : Commencez par `python3 simple_app.py` - c'est la solution la plus fiable et complète !