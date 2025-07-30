#!/usr/bin/env python3
"""
Application simple de recherche de concours FFE
Fonctionne sans dépendances externes
"""

import urllib.request
import re
import json
import csv
from html.parser import HTMLParser
from datetime import datetime

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

class FFECompetitionScraper:
    def __init__(self):
        self.competitions = []
        self.disciplines = {
            'E': 'Endurance',
            'D': 'Dressage',
            'CSO': 'Saut d\'Obstacles',
            'CCE': 'Complet',
            'HU': 'Hunter',
            'AT': 'Attelage',
            'VO': 'Voltige',
            'WE': 'Western',
            'PR': 'Polo/Para',
            'TREC': 'TREC'
        }
    
    def load_competitions(self):
        """
        Charge les compétitions depuis le site FFE
        """
        url = "https://ffecompet.ffe.com/concours"
        
        print("📡 Connexion au site FFE...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
            
            print("✅ Connexion réussie!")
            
            # Parser le HTML
            parser = FFESelectParser()
            parser.feed(content)
            
            print(f"📋 Extraction de {len(parser.options)} options...")
            
            # Traiter les compétitions
            self.competitions = []
            for option in parser.options:
                if option['value'] and option['text']:
                    comp = self._parse_competition(option['text'], option['value'])
                    self.competitions.append(comp)
            
            print(f"✅ {len(self.competitions)} compétitions chargées")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def _parse_competition(self, text, value):
        """
        Parse une compétition depuis le texte
        """
        competition = {
            'id': value,
            'nom': text,
            'discipline': '',
            'niveau': '',
            'url': f"https://ffecompet.ffe.com/concours/{value}"
        }
        
        # Extraire la discipline
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
        
        # Nettoyer le nom
        nom_clean = re.sub(r'\([A-Z]{2}\)$', '', text).strip()
        nom_clean = re.sub(r'\s+', ' ', nom_clean)
        competition['nom'] = nom_clean
        
        return competition
    
    def search_by_discipline(self, discipline):
        """
        Recherche par discipline
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
        
        results = []
        for comp in self.competitions:
            comp_discipline = comp.get('discipline', '').upper()
            comp_text = comp.get('nom', '').upper()
            
            for term in search_terms:
                if (comp_discipline == term or 
                    term in comp_discipline or 
                    term in comp_text):
                    results.append(comp)
                    break
        
        return results
    
    def search_by_text(self, text):
        """
        Recherche par texte libre
        """
        text = text.lower()
        results = []
        
        for comp in self.competitions:
            nom = comp.get('nom', '').lower()
            if text in nom:
                results.append(comp)
        
        return results
    
    def get_stats(self):
        """
        Retourne les statistiques par discipline
        """
        stats = {}
        for comp in self.competitions:
            discipline = comp.get('discipline', 'Autre')
            if discipline not in stats:
                stats[discipline] = 0
            stats[discipline] += 1
        return stats
    
    def save_to_csv(self, competitions, filename=None):
        """
        Sauvegarde en CSV
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ffe_competitions_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'nom', 'discipline', 'niveau', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for comp in competitions:
                writer.writerow(comp)
        
        print(f"💾 {len(competitions)} compétitions sauvegardées dans {filename}")
        return filename

def print_menu():
    print("\n" + "="*50)
    print("🐎 FFE Competition Search - Menu Principal")
    print("="*50)
    print("1. Charger les compétitions")
    print("2. Rechercher par discipline")
    print("3. Recherche libre")
    print("4. Afficher les statistiques")
    print("5. Sauvegarder les résultats en CSV")
    print("6. Quitter")
    print("="*50)

def print_disciplines():
    disciplines = {
        'E': 'Endurance',
        'D': 'Dressage', 
        'CSO': 'Saut d\'Obstacles',
        'CCE': 'Complet',
        'HU': 'Hunter',
        'AT': 'Attelage',
        'VO': 'Voltige',
        'WE': 'Western',
        'TREC': 'TREC'
    }
    
    print("\n🏆 Disciplines disponibles:")
    for code, nom in disciplines.items():
        print(f"   {code} - {nom}")

def print_results(results, title="Résultats"):
    print(f"\n📋 {title} ({len(results)} compétitions)")
    print("-" * 60)
    
    if not results:
        print("   Aucun résultat trouvé")
        return
    
    for i, comp in enumerate(results[:20]):  # Limiter à 20 résultats
        nom = comp.get('nom', 'N/A')
        discipline = comp.get('discipline', 'N/A')
        niveau = comp.get('niveau', 'N/A')
        
        # Tronquer le nom si trop long
        if len(nom) > 50:
            nom = nom[:47] + "..."
        
        print(f"{i+1:2d}. {nom}")
        print(f"     Discipline: {discipline} | Niveau: {niveau}")
    
    if len(results) > 20:
        print(f"     ... et {len(results) - 20} autres résultats")

def main():
    scraper = FFECompetitionScraper()
    last_results = []
    
    print("🐎 Bienvenue dans FFE Competition Search")
    print("Application de recherche de concours équestres")
    
    while True:
        print_menu()
        choice = input("Votre choix (1-6): ").strip()
        
        if choice == '1':
            # Charger les compétitions
            if scraper.load_competitions():
                print("✅ Compétitions chargées avec succès!")
            else:
                print("❌ Échec du chargement")
        
        elif choice == '2':
            # Recherche par discipline
            if not scraper.competitions:
                print("⚠️  Veuillez d'abord charger les compétitions (option 1)")
                continue
            
            print_disciplines()
            discipline = input("\nEntrez le code discipline (ex: E, CSO, D): ").strip()
            
            if discipline:
                results = scraper.search_by_discipline(discipline)
                last_results = results
                print_results(results, f"Compétitions de {discipline}")
            else:
                print("❌ Code discipline invalide")
        
        elif choice == '3':
            # Recherche libre
            if not scraper.competitions:
                print("⚠️  Veuillez d'abord charger les compétitions (option 1)")
                continue
            
            text = input("Entrez votre recherche: ").strip()
            
            if text:
                results = scraper.search_by_text(text)
                last_results = results
                print_results(results, f"Recherche '{text}'")
            else:
                print("❌ Texte de recherche vide")
        
        elif choice == '4':
            # Statistiques
            if not scraper.competitions:
                print("⚠️  Veuillez d'abord charger les compétitions (option 1)")
                continue
            
            stats = scraper.get_stats()
            print(f"\n📊 Statistiques ({sum(stats.values())} compétitions total)")
            print("-" * 30)
            
            for discipline, count in sorted(stats.items()):
                if count > 0:
                    nom_discipline = scraper.disciplines.get(discipline, discipline)
                    print(f"  {discipline:4s} - {nom_discipline:15s}: {count:4d}")
        
        elif choice == '5':
            # Sauvegarder en CSV
            if not last_results:
                print("⚠️  Aucun résultat à sauvegarder. Effectuez d'abord une recherche.")
                continue
            
            filename = input("Nom du fichier (appuyez sur Entrée pour auto): ").strip()
            if not filename:
                filename = None
            
            scraper.save_to_csv(last_results, filename)
        
        elif choice == '6':
            # Quitter
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide. Choisissez entre 1 et 6.")

if __name__ == "__main__":
    main()