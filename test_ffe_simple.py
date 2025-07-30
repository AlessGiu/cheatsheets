#!/usr/bin/env python3
"""
Test simple du scraper FFE avec les bibliothèques standard
"""

import urllib.request
import re
from html.parser import HTMLParser

class FFESelectParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_select = False
        self.options = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'select':
            self.in_select = True
        elif tag == 'option' and self.in_select:
            value = ''
            for attr, val in attrs:
                if attr == 'value':
                    value = val
                    break
            self.current_option = {'value': value, 'text': ''}
    
    def handle_data(self, data):
        if self.in_select and hasattr(self, 'current_option'):
            self.current_option['text'] += data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'select':
            self.in_select = False
        elif tag == 'option' and hasattr(self, 'current_option'):
            if self.current_option['value'] and self.current_option['text']:
                self.options.append(self.current_option)
            delattr(self, 'current_option')

def parse_competition_text(text, value):
    """
    Parse competition text to extract structured information
    """
    competition = {
        'id': value,
        'nom': text,
        'discipline': '',
        'niveau': '',
        'url': f"https://ffecompet.ffe.com/concours/{value}"
    }
    
    # Extraire la discipline depuis le texte
    discipline_patterns = {
        'E': r'\(EN\)|Endurance',
        'D': r'\(DR\)|Dressage',
        'CSO': r'\(SO\)|Saut.*Obstacles',
        'CCE': r'\(CE\)|Complet',
        'HU': r'\(HU\)|Hunter',
        'AT': r'\(AT\)|Attelage',
        'VO': r'\(VO\)|Voltige',
        'WE': r'\(WE\)|Western',
        'PR': r'\(PR\)|Polo',
        'TREC': r'TREC',
    }
    
    for discipline, pattern in discipline_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            competition['discipline'] = discipline
            break
    
    # Extraire le niveau
    niveau_patterns = [
        r'Amateur|Am\s*\d*',
        r'Pro|Professional', 
        r'Elite',
        r'Préparatoire',
        r'Formation',
        r'Enseignant',
        r'Jeune|Junior',
        r'Cadet|Benjamin',
        r'Senior',
        r'Poney'
    ]
    
    for pattern in niveau_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            competition['niveau'] = match.group(0)
            break
    
    # Extraire des informations sur la hauteur pour CSO
    height_match = re.search(r'\(([0-9]+[.,][0-9]+)\s*m?\)', text)
    if height_match:
        height = height_match.group(1).replace(',', '.')
        if competition['discipline'] == 'CSO' or 'SO' in text:
            competition['niveau'] += f" ({height}m)"
    
    # Nettoyer le nom
    nom_clean = re.sub(r'\([A-Z]{2}\)$', '', text).strip()
    nom_clean = re.sub(r'\s+', ' ', nom_clean)
    competition['nom'] = nom_clean
    
    return competition

def search_by_discipline(competitions, discipline):
    """
    Filter competitions by discipline
    """
    discipline_mapping = {
        'E': ['E', 'EN', 'Endurance'],
        'D': ['D', 'DR', 'Dressage'], 
        'CSO': ['CSO', 'SO', 'Saut'],
        'CCE': ['CCE', 'CE', 'Complet'],
        'HU': ['HU', 'Hunter'],
        'AT': ['AT', 'Attelage'],
        'VO': ['VO', 'Voltige'],
        'WE': ['WE', 'Western'],
        'TREC': ['TREC'],
    }
    
    search_terms = discipline_mapping.get(discipline.upper(), [discipline.upper()])
    
    filtered = []
    for comp in competitions:
        comp_discipline = comp.get('discipline', '').upper()
        comp_text = comp.get('nom', '').upper()
        
        for term in search_terms:
            if (comp_discipline == term or 
                term in comp_discipline or 
                term in comp_text):
                filtered.append(comp)
                break
    
    return filtered

def main():
    print("🐎 Test FFE Scraper Simple")
    print("=" * 40)
    
    url = "https://ffecompet.ffe.com/concours"
    
    try:
        print("📡 Connexion au site FFE...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        print("✅ Connexion réussie!")
        
        # Parser le HTML pour extraire les options du select
        parser = FFESelectParser()
        parser.feed(content)
        
        print(f"📋 Trouvé {len(parser.options)} options dans le select")
        
        # Traiter les compétitions
        competitions = []
        for option in parser.options:
            if option['value'] and option['text']:
                comp = parse_competition_text(option['text'], option['value'])
                competitions.append(comp)
        
        print(f"✅ {len(competitions)} compétitions traitées")
        
        # Statistiques par discipline
        stats = {}
        for comp in competitions:
            discipline = comp.get('discipline', 'Autre')
            if discipline not in stats:
                stats[discipline] = 0
            stats[discipline] += 1
        
        print(f"\n📊 Répartition par discipline:")
        for discipline, count in sorted(stats.items()):
            if count > 0:
                print(f"   - {discipline}: {count} compétitions")
        
        # Exemples de données
        print("\n📋 Exemples de compétitions:")
        for i, comp in enumerate(competitions[:5]):
            nom = comp.get('nom', 'N/A')[:60] + "..." if len(comp.get('nom', '')) > 60 else comp.get('nom', 'N/A')
            print(f"{i+1}. {nom}")
            print(f"    Discipline: {comp.get('discipline', 'N/A')} | Niveau: {comp.get('niveau', 'N/A')}")
        
        # Test recherche par discipline "E"
        print(f"\n🔍 Test recherche discipline 'E' (Endurance):")
        endurance = search_by_discipline(competitions, 'E')
        print(f"   Trouvé {len(endurance)} compétitions d'endurance")
        
        if endurance:
            print("   Exemples:")
            for i, comp in enumerate(endurance[:3]):
                print(f"   {i+1}. {comp.get('nom', 'N/A')}")
        
        # Test recherche par discipline "CSO"
        print(f"\n🔍 Test recherche discipline 'CSO' (Saut d'Obstacles):")
        cso = search_by_discipline(competitions, 'CSO')
        print(f"   Trouvé {len(cso)} compétitions de saut")
        
        if cso:
            print("   Exemples:")
            for i, comp in enumerate(cso[:3]):
                print(f"   {i+1}. {comp.get('nom', 'N/A')} - {comp.get('niveau', 'N/A')}")
        
        print(f"\n🎉 Test réussi ! Extraction de données fonctionnelle.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ Le scraper fonctionne correctement!")
        print("💡 Installez les dépendances pour utiliser l'interface web complète:")
        print("   pip install requests beautifulsoup4 flask pandas")
    else:
        print("\n💥 Test échoué.")