#!/usr/bin/env python3
"""
Demo simple du scraper FFE - Version basique
Fonctionne avec les bibliothèques Python standard uniquement
"""

import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

def simple_ffe_demo():
    """
    Démonstration simple d'extraction de données FFE
    """
    print("🐎 FFE Competition Scraper - Demo Simple")
    print("=" * 50)
    
    url = "https://ffecompet.ffe.com/concours"
    
    try:
        # Simple HTTP request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("📡 Connexion au site FFE...")
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            
        print("✅ Connexion réussie!")
        print(f"📄 Taille de la page: {len(content)} caractères")
        
        # Simple pattern matching pour extraire des informations
        print("\n🔍 Recherche de données de concours...")
        
        # Recherche de patterns simples
        patterns = {
            'concours': r'concours|competition',
            'dates': r'\d{2}[/-]\d{2}[/-]\d{4}',
            'disciplines': r'\b[EDC][SO]?[OE]?\b',
            'lieux': r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*',
        }
        
        results = {}
        for name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            results[name] = len(set(matches))  # Unique matches
            
        print("📊 Résultats d'analyse:")
        for name, count in results.items():
            print(f"   - {name.capitalize()}: {count} éléments trouvés")
        
        # Disciplines équestres disponibles
        disciplines = [
            'E (Endurance)',
            'D (Dressage)', 
            'CSO (Saut d\'Obstacles)',
            'CCE (Complet)',
            'TREC (Randonnée)',
            'ATT (Attelage)',
            'VOL (Voltige)'
        ]
        
        print(f"\n🏆 Disciplines équestres supportées:")
        for discipline in disciplines:
            print(f"   - {discipline}")
            
        print(f"\n💡 Pour une extraction complète, installez les dépendances:")
        print(f"   pip install requests beautifulsoup4 flask pandas")
        print(f"\n🚀 Puis lancez: python3 app.py")
        
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ Erreur de connexion: {e}")
        print("   Vérifiez votre connexion internet")
        return False
        
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def show_usage_examples():
    """
    Affiche des exemples d'utilisation
    """
    print("\n📚 Exemples d'utilisation complète:")
    print("=" * 40)
    
    examples = [
        {
            'title': 'Rechercher les compétitions d\'endurance',
            'code': '''from ffe_scraper import FFEScraper
scraper = FFEScraper()
endurance = scraper.search_competitions_by_discipline('E')
print(f"Trouvé {len(endurance)} compétitions")'''
        },
        {
            'title': 'Interface web',
            'code': '''python3 app.py
# Puis aller sur http://localhost:5000'''
        },
        {
            'title': 'Export CSV',
            'code': '''competitions = scraper.get_all_competitions()
scraper.save_to_csv(competitions, 'concours_ffe.csv')'''
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}:")
        print(f"   {example['code']}")

if __name__ == "__main__":
    success = simple_ffe_demo()
    
    if success:
        show_usage_examples()
        print(f"\n✨ Demo terminée avec succès!")
    else:
        print(f"\n💥 Demo échouée. Vérifiez votre connexion.")
        
    print(f"\n📖 Consultez README.md pour plus d'informations.")