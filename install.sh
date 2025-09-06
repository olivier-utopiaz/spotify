#!/bin/bash

echo "🚀 Installation des dépendances pour le bot Spotify-Threads..."

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Installation des packages
echo "📦 Installation des packages Python..."
pip3 install -r requirements.txt

# Création des dossiers nécessaires
echo "📁 Création des dossiers..."
mkdir -p logs

# Vérification des installations
echo "✅ Vérification des installations..."
python3 -c "
try:
    import spotipy
    import requests
    import schedule
    import loguru
    print('✅ Toutes les dépendances sont installées')
except ImportError as e:
    print(f'❌ Erreur d\'importation: {e}')
    exit(1)
"

echo "🎉 Installation terminée !"
echo "💡 N'oubliez pas de créer votre fichier .env avec vos clés API"
