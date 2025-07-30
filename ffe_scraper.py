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
        
        # Parameters for the search
        params = {
            'page': page,
            'limit': 50  # Number of results per page
        }
        
        # Add filters if provided
        if filters:
            params.update(filters)
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            # Try to extract JSON data if it's an AJAX response
            if 'application/json' in response.headers.get('content-type', ''):
                return response.json()
            
            # Otherwise parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._parse_competition_html(soup)
            
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return []
    
    def _parse_competition_html(self, soup):
        """
        Parse HTML content to extract competition information
        """
        competitions = []
        
        # Look for competition containers - these might be in tables or divs
        competition_elements = soup.find_all(['tr', 'div'], class_=re.compile(r'competition|concours|event', re.I))
        
        if not competition_elements:
            # Fallback: look for table rows that might contain competition data
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header row
                for row in rows:
                    comp_data = self._extract_competition_from_row(row)
                    if comp_data:
                        competitions.append(comp_data)
        else:
            for element in competition_elements:
                comp_data = self._extract_competition_from_element(element)
                if comp_data:
                    competitions.append(comp_data)
        
        return competitions
    
    def _extract_competition_from_row(self, row):
        """
        Extract competition data from a table row
        """
        cells = row.find_all(['td', 'th'])
        if len(cells) < 3:  # Need at least some basic data
            return None
            
        try:
            competition = {
                'nom': '',
                'discipline': '',
                'niveau': '',
                'date': '',
                'lieu': '',
                'organisateur': '',
                'statut': '',
                'url': ''
            }
            
            # Try to extract text from cells
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            
            # Basic mapping - this will need adjustment based on actual HTML structure
            if len(cell_texts) >= 1:
                competition['nom'] = cell_texts[0]
            if len(cell_texts) >= 2:
                competition['date'] = cell_texts[1]
            if len(cell_texts) >= 3:
                competition['lieu'] = cell_texts[2]
            if len(cell_texts) >= 4:
                competition['discipline'] = cell_texts[3]
            if len(cell_texts) >= 5:
                competition['niveau'] = cell_texts[4]
                
            # Look for links
            link = row.find('a')
            if link and link.get('href'):
                competition['url'] = urljoin(self.base_url, link.get('href'))
                
            return competition
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des données de ligne: {e}")
            return None
    
    def _extract_competition_from_element(self, element):
        """
        Extract competition data from a generic element
        """
        try:
            competition = {
                'nom': '',
                'discipline': '',
                'niveau': '',
                'date': '',
                'lieu': '',
                'organisateur': '',
                'statut': '',
                'url': ''
            }
            
            # Extract text content
            text = element.get_text(strip=True)
            
            # Look for common patterns
            competition['nom'] = text
            
            # Look for links
            link = element.find('a')
            if link and link.get('href'):
                competition['url'] = urljoin(self.base_url, link.get('href'))
                
            return competition
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des données d'élément: {e}")
            return None
    
    def search_competitions_by_discipline(self, discipline):
        """
        Search competitions filtered by discipline (E, D, CSO, etc.)
        """
        all_competitions = []
        page = 1
        
        while True:
            competitions = self.get_competitions_data(page=page)
            if not competitions:
                break
                
            # Filter by discipline
            filtered = [comp for comp in competitions 
                       if discipline.upper() in comp.get('discipline', '').upper()]
            all_competitions.extend(filtered)
            
            # Check if we need to continue pagination
            if len(competitions) < 50:  # Less than full page
                break
                
            page += 1
            time.sleep(1)  # Be respectful to the server
        
        return all_competitions
    
    def get_all_competitions(self, max_pages=10):
        """
        Get all competitions with pagination
        """
        all_competitions = []
        
        for page in range(1, max_pages + 1):
            print(f"Récupération page {page}...")
            competitions = self.get_competitions_data(page=page)
            
            if not competitions:
                break
                
            all_competitions.extend(competitions)
            
            # Stop if we got less than a full page
            if len(competitions) < 50:
                break
                
            time.sleep(1)  # Be respectful to the server
        
        return all_competitions
    
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
        # Common equestrian disciplines
        disciplines = [
            'E',      # Endurance
            'D',      # Dressage
            'CSO',    # Concours de Saut d'Obstacles
            'CCE',    # Concours Complet d'Equitation
            'TREC',   # Techniques de Randonnée Équestre de Compétition
            'PTV',    # Pony-Trot-Voltige
            'ATT',    # Attelage
            'VOL',    # Voltige
            'EE',     # Équitation Éthologique
            'POLO',   # Polo
            'HORSE',  # Horse-Ball
        ]
        return disciplines

def main():
    """
    Example usage of the FFE scraper
    """
    scraper = FFEScraper()
    
    print("🐎 FFE Competition Scraper")
    print("=" * 40)
    
    # Get sample data
    print("Récupération des données de concours...")
    competitions = scraper.get_all_competitions(max_pages=3)
    
    if competitions:
        print(f"✅ {len(competitions)} concours récupérés")
        
        # Save to CSV
        filename = scraper.save_to_csv(competitions)
        
        # Show sample data
        print("\n📋 Exemple de données:")
        for i, comp in enumerate(competitions[:5]):
            print(f"{i+1}. {comp.get('nom', 'N/A')} - {comp.get('discipline', 'N/A')} - {comp.get('date', 'N/A')}")
    else:
        print("❌ Aucun concours trouvé")

if __name__ == "__main__":
    main()