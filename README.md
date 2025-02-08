# Threads Music Bot

Bot d'automatisation pour poster quotidiennement des recommandations musicales sur Threads.

## Configuration

1. Créez un fichier `.env` basé sur `.env.example`
2. Remplissez les informations d'API requises :
   - Créez une application sur [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Créez une application sur [Meta for Developers](https://developers.facebook.com)

## Installation

```bash
pip install -r requirements.txt
```

## Structure du projet

- `src/`
  - `config.py` : Configuration et variables d'environnement
  - `spotify_client.py` : Client pour l'API Spotify
  - (autres modules à venir)
- `logs/` : Fichiers de logs
- `.env` : Variables d'environnement (Attention à ne pas le publier sur votre)
- `requirements.txt` : Dépendances Python