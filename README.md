# Threads Music Bot

Bot d'automatisation pour poster quotidiennement des recommandations musicales sur son compte Threads.
Il est nécessaire d'utiliser l'ID de son profil Insta dans le cas ou vous utilisez celui-ci pour gérer votre compte @Threads. **Il est important** cependant que votre compte Instagram soit de type **"Professionnel ou Creator"**

## Installation de Python sur votre environnement

### Windows
1. Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
2. Lancez l'installateur et cochez la case "Add Python to PATH"
3. Vérifiez l'installation en ouvrant un terminal (cmd) :
```bash
python --version
```

### macOS
1. Avec Homebrew (recommandé) :
```bash
brew install python
```
2. Ou téléchargez depuis [python.org](https://www.python.org/downloads/)
3. Vérifiez l'installation :
```bash
python3 --version
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Pour vérifier l'installation :
```bash
python3 --version
```

### Création de l'environnement virtuel (dans votre dossier de travail)
Une fois Python installé, créez un environnement virtuel :

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

Activation de l'environnement :
```bash
# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

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
- `.env` : Variables d'environnement (Attention à ne pas le publier sur votre repo distant, idem pour le fichier .cache)
- `requirements.txt` : Dépendances Python

## Fichier Utile

Dans le dossier 'utils' vous trouverez un fichier nommé 'spotify-bot.service' à créer sur votre serveur linux. Cela permet d'automatiser la tâche via un service au lieu d'une tâche Cron. Il va permettre de lancer votre environnement Python et de lancer le fichier "src/scheduler.py"
```bash
vim /etc/systemd/system/spotify-bot.service
```