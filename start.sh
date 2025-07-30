#!/bin/bash

echo "🐎 FFE Competition Scraper - Setup & Start"
echo "=========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3; then
    echo "❌ Python3 is required but not found."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check pip
if ! command_exists pip3 && ! command_exists pip; then
    echo "❌ pip is required but not found."
    exit 1
fi

# Use pip3 if available, otherwise pip
PIP_CMD="pip3"
if ! command_exists pip3; then
    PIP_CMD="pip"
fi

echo "✅ Using pip: $PIP_CMD"

# Try to create virtual environment
echo "🔧 Setting up virtual environment..."
if python3 -m venv venv 2>/dev/null; then
    echo "✅ Virtual environment created"
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Dependencies installed in virtual environment"
    PYTHON_CMD="./venv/bin/python"
else
    echo "⚠️  Virtual environment creation failed, trying system-wide install..."
    
    # Try system installation with --break-system-packages
    if $PIP_CMD install -r requirements.txt --break-system-packages 2>/dev/null; then
        echo "✅ Dependencies installed system-wide"
        PYTHON_CMD="python3"
    else
        echo "⚠️  System installation also failed, trying --user install..."
        if $PIP_CMD install -r requirements.txt --user 2>/dev/null; then
            echo "✅ Dependencies installed for user"
            PYTHON_CMD="python3"
        else
            echo "❌ Failed to install dependencies. Please install manually:"
            echo "   pip3 install requests beautifulsoup4 flask pandas lxml"
            exit 1
        fi
    fi
fi

# Test installation
echo "🧪 Testing installation..."
if $PYTHON_CMD -c "import requests, bs4, flask, pandas; print('All modules imported successfully')" 2>/dev/null; then
    echo "✅ All dependencies are available"
else
    echo "❌ Some dependencies are missing. Please check the installation."
    exit 1
fi

# Ask user what to run
echo ""
echo "🚀 What would you like to do?"
echo "1) Test the scraper (recommended first run)"
echo "2) Start the web interface"
echo "3) Run a quick discipline search"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🧪 Running scraper tests..."
        $PYTHON_CMD test_scraper.py
        ;;
    2)
        echo "🌐 Starting web interface..."
        echo "Access the interface at: http://localhost:5000"
        echo "Press Ctrl+C to stop the server"
        $PYTHON_CMD app.py
        ;;
    3)
        echo "🔍 Quick search example - Endurance competitions..."
        $PYTHON_CMD -c "
from ffe_scraper import FFEScraper
scraper = FFEScraper()
print('Searching for Endurance competitions...')
competitions = scraper.search_competitions_by_discipline('E')
print(f'Found {len(competitions)} competitions')
if competitions:
    print('First 3 results:')
    for i, comp in enumerate(competitions[:3]):
        print(f'{i+1}. {comp.get(\"nom\", \"N/A\")} - {comp.get(\"lieu\", \"N/A\")}')
else:
    print('No competitions found or connection error.')
"
        ;;
    *)
        echo "Invalid choice. Run the script again."
        exit 1
        ;;
esac