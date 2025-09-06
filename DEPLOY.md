# 🎵 Guide de déploiement - Bot Spotify-Threads

## 📋 Prérequis sur le serveur

### 1. Python et dépendances
```bash
# Vérifier Python 3
python3 --version

# Installer pip si nécessaire
sudo apt update
sudo apt install python3-pip

# Installer git si nécessaire
sudo apt install git
```

### 2. Cloner le projet
```bash
git clone <your-repo-url>
cd spotify
```

### 3. Installation des dépendances
```bash
# Rendre le script d'installation exécutable
chmod +x install.sh

# Installer les dépendances
./install.sh
```

## 🔑 Configuration des clés API

### 1. Créer le fichier .env
```bash
cp .env.example .env
nano .env
```

### 2. Remplir avec vos vraies clés :
```bash
# Spotify API Credentials
SPOTIFY_CLIENT_ID=votre_spotify_client_id
SPOTIFY_CLIENT_SECRET=votre_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback

# Meta/Threads API Credentials  
META_APP_ID=votre_meta_app_id
META_APP_SECRET=votre_meta_app_secret
META_ACCESS_TOKEN=votre_access_token

# Meta/Instagram User ID
INSTAGRAM_USER_ID=votre_instagram_user_id

# Configuration
POSTING_TIME=07:30
TIMEZONE=Europe/Paris
```

## 🧪 Tests avant déploiement

### 1. Test de la structure
```bash
python3 run_bot.py --test
```

### 2. Test de l'environnement
```bash
python3 run_bot.py --check-env
```

### 3. Test d'un post immédiat
```bash
python3 run_bot.py --post-now
```

## 🚀 Lancement en production

### Mode normal (avec scheduler)
```bash
python3 run_bot.py
```

### Mode daemon avec systemd
```bash
# Copier le fichier de service
sudo cp utils/spotify-bot.service /etc/systemd/system/

# Éditer le fichier pour adapter les chemins
sudo nano /etc/systemd/system/spotify-bot.service

# Recharger systemd
sudo systemctl daemon-reload

# Activer le service
sudo systemctl enable spotify-bot.service

# Démarrer le service
sudo systemctl start spotify-bot.service

# Vérifier le statut
sudo systemctl status spotify-bot.service
```

## 📊 Monitoring et logs

### Voir les logs en temps réel
```bash
tail -f logs/threads_bot.log
```

### Logs du service systemd
```bash
sudo journalctl -u spotify-bot.service -f
```

## 🔧 Dépannage

### Problèmes courants

1. **ModuleNotFoundError** : Vérifiez que toutes les dépendances sont installées
   ```bash
   pip3 list | grep -E "(spotipy|requests|schedule|loguru)"
   ```

2. **Erreur de clés API** : Vérifiez le fichier .env
   ```bash
   python3 run_bot.py --check-env
   ```

3. **Problème de permissions** : Vérifiez les permissions des fichiers
   ```bash
   chmod +x run_bot.py install.sh
   ```

4. **Erreur Threads API** : Vérifiez que votre token est valide et que vous avez les bonnes permissions

### Token expiré (Error 401)
Si vous obtenez une erreur 401 avec "Session has expired" :
```bash
# Utiliser le script de diagnostic/renouvellement
python3 refresh_token.py

# Ou vérifier manuellement
python3 diagnose_threads.py
```

⚠️ **Important** : Les tokens Meta expirent régulièrement (60 jours max). Vous devrez les renouveler périodiquement.

### Structure des fichiers sur le serveur
```
spotify/
├── run_bot.py              # Script principal ✅
├── install.sh              # Installation ✅  
├── requirements.txt        # Dépendances ✅
├── .env                    # Clés API (à créer) ❗
├── src/
│   ├── __init__.py         # Package ✅
│   ├── config.py           # Configuration ✅
│   ├── spotify_client.py   # Client Spotify ✅
│   ├── threads_client.py   # Client Threads ✅
│   ├── scheduler.py        # Planificateur ✅
│   └── main.py             # Main alternatif ✅
├── logs/                   # Logs (créé auto) ✅
└── utils/
    └── spotify-bot.service # Service systemd ✅
```

## 🎯 Commandes essentielles pour le serveur

```bash
# Installation complète
./install.sh

# Test complet
python3 run_bot.py --test

# Vérification environnement  
python3 run_bot.py --check-env

# Post de test
python3 run_bot.py --post-now

# Lancement normal
python3 run_bot.py

# Lancement en arrière-plan
nohup python3 run_bot.py > bot.log 2>&1 &
```
