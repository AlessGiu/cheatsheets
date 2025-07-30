#!/usr/bin/env python3
"""
Script de test pour le scraper FFE
"""

from ffe_scraper import FFEScraper
import sys

def test_scraper():
    """
    Test basic functionality of the FFE scraper
    """
    print("🧪 Test du FFE Scraper")
    print("=" * 50)
    
    # Initialize scraper
    scraper = FFEScraper()
    
    try:
        # Test 1: Get disciplines list
        print("\n1. Test récupération des disciplines...")
        disciplines = scraper.get_disciplines_list()
        print(f"✅ {len(disciplines)} disciplines disponibles: {', '.join(disciplines)}")
        
        # Test 2: Search for a specific discipline (E for Endurance)
        print("\n2. Test recherche par discipline (E - Endurance)...")
        endurance_competitions = scraper.search_competitions_by_discipline('E')
        print(f"✅ {len(endurance_competitions)} compétitions d'endurance trouvées")
        
        if endurance_competitions:
            print("   Exemples:")
            for i, comp in enumerate(endurance_competitions[:3]):
                print(f"   - {comp.get('nom', 'N/A')} ({comp.get('lieu', 'N/A')})")
        
        # Test 3: Get general competitions
        print("\n3. Test récupération générale (première page)...")
        all_competitions = scraper.get_all_competitions(max_pages=1)
        print(f"✅ {len(all_competitions)} compétitions récupérées")
        
        if all_competitions:
            print("   Exemples:")
            for i, comp in enumerate(all_competitions[:3]):
                print(f"   - {comp.get('nom', 'N/A')} - {comp.get('discipline', 'N/A')}")
        
        # Test 4: Save to CSV
        if all_competitions:
            print("\n4. Test sauvegarde CSV...")
            filename = scraper.save_to_csv(all_competitions, "test_competitions.csv")
            print(f"✅ Données sauvegardées dans {filename}")
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_connectivity():
    """
    Test basic web connectivity to FFE website
    """
    print("\n🌐 Test de connectivité web...")
    
    try:
        import requests
        response = requests.get("https://ffecompet.ffe.com", timeout=10)
        
        if response.status_code == 200:
            print("✅ Connexion au site FFE réussie")
            return True
        else:
            print(f"⚠️  Site FFE accessible mais retourne le code: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Impossible de se connecter au site FFE: {e}")
        return False

if __name__ == "__main__":
    print("🐎 FFE Competition Scraper - Tests")
    print("=" * 60)
    
    # Test connectivity first
    if not test_web_connectivity():
        print("\n⚠️  Problème de connectivité. Vérifiez votre connexion internet.")
        sys.exit(1)
    
    # Run scraper tests
    success = test_scraper()
    
    if success:
        print("\n✨ Tous les tests sont passés! Le scraper est prêt à être utilisé.")
        sys.exit(0)
    else:
        print("\n💥 Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)