from flask import Flask, render_template, request, jsonify, send_file
from ffe_scraper import FFEScraper
import pandas as pd
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre-cle-secrete-ffe'

# Initialize the scraper
scraper = FFEScraper()

@app.route('/')
def index():
    """
    Page d'accueil avec interface de recherche
    """
    disciplines = scraper.get_disciplines_list()
    return render_template('index.html', disciplines=disciplines)

@app.route('/api/competitions')
def get_competitions():
    """
    API endpoint pour récupérer les compétitions
    """
    # Paramètres de recherche
    discipline = request.args.get('discipline', '')
    page = int(request.args.get('page', 1))
    search_term = request.args.get('search', '')
    
    try:
        if discipline:
            # Recherche par discipline spécifique
            competitions = scraper.search_competitions_by_discipline(discipline)
        else:
            # Récupération de toutes les compétitions
            competitions = scraper.get_all_competitions(max_pages=5)
        
        # Filtrage par terme de recherche si fourni
        if search_term:
            competitions = [
                comp for comp in competitions
                if search_term.lower() in comp.get('nom', '').lower() or
                   search_term.lower() in comp.get('lieu', '').lower() or
                   search_term.lower() in comp.get('organisateur', '').lower()
            ]
        
        return jsonify({
            'success': True,
            'competitions': competitions,
            'total': len(competitions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/disciplines')
def get_disciplines():
    """
    API endpoint pour récupérer la liste des disciplines
    """
    try:
        disciplines = scraper.get_disciplines_list()
        return jsonify({
            'success': True,
            'disciplines': disciplines
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/export/csv')
def export_csv():
    """
    Exporter les résultats en CSV
    """
    discipline = request.args.get('discipline', '')
    search_term = request.args.get('search', '')
    
    try:
        if discipline:
            competitions = scraper.search_competitions_by_discipline(discipline)
        else:
            competitions = scraper.get_all_competitions(max_pages=5)
        
        # Filtrage par terme de recherche si fourni
        if search_term:
            competitions = [
                comp for comp in competitions
                if search_term.lower() in comp.get('nom', '').lower() or
                   search_term.lower() in comp.get('lieu', '').lower() or
                   search_term.lower() in comp.get('organisateur', '').lower()
            ]
        
        # Créer le fichier CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ffe_competitions_{timestamp}.csv"
        
        df = pd.DataFrame(competitions)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return send_file(filename, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/search')
def search_page():
    """
    Page de recherche avancée
    """
    disciplines = scraper.get_disciplines_list()
    return render_template('search.html', disciplines=disciplines)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Créer le dossier templates s'il n'existe pas
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Créer le dossier static s'il n'existe pas
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/css')
        os.makedirs('static/js')
    
    print("🐎 FFE Competition Web Interface")
    print("=" * 40)
    print("Accédez à l'interface web sur: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)