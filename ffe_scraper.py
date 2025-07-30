import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import re
import time
from urllib.parse import urljoin, parse_qs, urlparse

class FFEScraper:
    def __init__(self):
        self.base_url = "https://ffecompet.ffe.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_competitions_data(self, page=1, filters=None):
        """
        Extracts competition data from FFE website
        """
        url = f"{self.base_url}/concours"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._parse_competition_html(soup)
            
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return []
    
    def _parse_competition_html(self, soup):
        """
        Parse HTML content to extract competition information from select options
        """
        competitions = []
        
        # Rechercher le select qui contient les compétitions
        select_element = soup.find('select')
        if not select_element:
            print("Aucun élément select trouvé")
            return competitions
            
        options = select_element.find_all('option')
        print(f"Trouvé {len(options)} options dans le select")
        
        for option in options:
            value = option.get('value', '')
            text = option.get_text(strip=True)
            
            # Ignorer les options vides ou sans valeur
            if not value or not text or value == "":
                continue
                
            competition = self._parse_competition_text(text, value)
            if competition:
                competitions.append(competition)
        
        return competitions
    
    def _parse_competition_text(self, text, value):
        """
        Parse competition text to extract structured information
        """
        try:
            competition = {
                'id': value,
                'nom': text,
                'discipline': '',
                'niveau': '',
                'date': '',
                'lieu': '',
                'organisateur': '',
                'statut': '',
                'url': f"{self.base_url}/concours/{value}" if value else ''
            }
            
            # Extraire la discipline depuis le texte
            # Chercher les codes de discipline courants
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
            
            # Extraire le niveau (Amateur, Pro, Elite, etc.)
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
            
            # Nettoyer le nom pour enlever les codes techniques
            nom_clean = re.sub(r'\([A-Z]{2}\)$', '', text).strip()
            nom_clean = re.sub(r'\s+', ' ', nom_clean)
            competition['nom'] = nom_clean
            
            return competition
            
        except Exception as e:
            print(f"Erreur lors de l'analyse du texte '{text}': {e}")
            return None
    
    def search_competitions_by_discipline(self, discipline):
        """
        Search competitions filtered by discipline (E, D, CSO, etc.)
        """
        all_competitions = self.get_competitions_data()
        
        # Normaliser la discipline recherchée
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
        for comp in all_competitions:
            comp_discipline = comp.get('discipline', '').upper()
            comp_text = comp.get('nom', '').upper()
            
            # Vérifier si la discipline correspond
            for term in search_terms:
                if (comp_discipline == term or 
                    term in comp_discipline or 
                    term in comp_text):
                    filtered.append(comp)
                    break
        
        return filtered
    
    def get_all_competitions(self, max_pages=10):
        """
        Get all competitions (for this site, it's all in one page)
        """
        print("Récupération de toutes les compétitions...")
        competitions = self.get_competitions_data()
        print(f"Total récupéré: {len(competitions)} compétitions")
        return competitions
    
    def save_to_csv(self, competitions, filename=None):
        """
        Save competitions data to CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ffe_competitions_{timestamp}.csv"
        
        df = pd.DataFrame(competitions)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Données sauvegardées dans {filename}")
        return filename
    
    def get_disciplines_list(self):
        """
        Extract list of available disciplines from the website
        """
        # Disciplines équestres françaises courantes
        disciplines = [
            'E',      # Endurance  
            'D',      # Dressage
            'CSO',    # Concours de Saut d'Obstacles
            'CCE',    # Concours Complet d'Équitation
            'HU',     # Hunter
            'AT',     # Attelage
            'VO',     # Voltige
            'WE',     # Western
            'TREC',   # Techniques de Randonnée Équestre de Compétition
            'PR',     # Polo/Para
        ]
        return disciplines
    
    def get_competition_stats(self):
        """
        Get statistics about competitions by discipline
        """
        competitions = self.get_all_competitions()
        stats = {}
        
        for comp in competitions:
            discipline = comp.get('discipline', 'Autre')
            if discipline not in stats:
                stats[discipline] = 0
            stats[discipline] += 1
            
        return stats

def main():
    """
    Example usage of the FFE scraper
    """
    scraper = FFEScraper()
    
    print("🐎 FFE Competition Scraper - Version améliorée")
    print("=" * 50)
    
    # Get sample data
    print("Récupération des données de concours...")
    competitions = scraper.get_all_competitions()
    
    if competitions:
        print(f"✅ {len(competitions)} concours récupérés")
        
        # Afficher les statistiques par discipline
        stats = scraper.get_competition_stats()
        print(f"\n📊 Répartition par discipline:")
        for discipline, count in sorted(stats.items()):
            print(f"   - {discipline}: {count} compétitions")
        
        # Save to CSV
        filename = scraper.save_to_csv(competitions)
        
        # Show sample data
        print("\n📋 Exemples de données:")
        for i, comp in enumerate(competitions[:10]):
            nom = comp.get('nom', 'N/A')[:50] + "..." if len(comp.get('nom', '')) > 50 else comp.get('nom', 'N/A')
            print(f"{i+1}. {nom} - {comp.get('discipline', 'N/A')} - {comp.get('niveau', 'N/A')}")
            
        # Test recherche par discipline
        print(f"\n🔍 Test recherche discipline 'E' (Endurance):")
        endurance = scraper.search_competitions_by_discipline('E')
        print(f"   Trouvé {len(endurance)} compétitions d'endurance")
        
        if endurance:
            for i, comp in enumerate(endurance[:3]):
                print(f"   {i+1}. {comp.get('nom', 'N/A')}")
    else:
        print("❌ Aucun concours trouvé")

if __name__ == "__main__":
    main()