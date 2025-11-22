# 🎵 Spotify Threads Bot

Bot d'automatisation qui publie quotidiennement des recommandations musicales (albums aléatoires par genre) sur votre compte Threads.

## 📋 Prérequis

- **Python 3.10** ou supérieur
- Un compte **Spotify Developer** (pour l'API)
- Un compte **Instagram Professionnel ou Créateur** (lié à une Page Facebook)
- Un serveur Linux (Ubuntu/Debian recommandé) pour la production

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/olivier-utopiaz/spotify.git
cd spotify
```

### 2. Créer l'environnement virtuel
```bash
# Création de l'environnement
python3 -m venv .venv

# Activation
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Variables d'environnement
Créez un fichier `.env` à la racine du projet :
```bash
cp .env.example .env  # Si le fichier exemple existe, sinon créez-le
nano .env
```

Remplissez le fichier avec vos clés :
```ini
# Spotify Configuration
SPOTIFY_CLIENT_ID="votre_client_id"
SPOTIFY_CLIENT_SECRET="votre_client_secret"
SPOTIFY_REDIRECT_URI="http://localhost:8080/callback"

# Meta/Threads Configuration
META_APP_ID="votre_app_id"
META_APP_SECRET="votre_app_secret"
META_ACCESS_TOKEN="votre_token_longue_duree"
INSTAGRAM_USER_ID="votre_user_id"

# Bot Configuration
POSTING_TIME="07:30"  # Heure de publication
TIMEZONE="Europe/Paris"
```

### 2. Obtenir les Tokens
Des scripts utilitaires sont disponibles dans le dossier `scripts/` pour vous aider :

- **Générer un token Threads** :
  ```bash
  python scripts/generate_token.py
  ```
  Suivez les instructions pour obtenir votre `META_ACCESS_TOKEN`.

- **Vérifier la configuration** :
  ```bash
  python scripts/diagnose_threads.py
  ```

## 🛠️ Utilisation

### Mode Test
Pour vérifier que tout fonctionne sans attendre l'heure programmée :
```bash
python run_bot.py --test
```

### Lancement manuel
Pour lancer le bot directement (il attendra l'heure configurée) :
```bash
python run_bot.py
```

Pour forcer une publication immédiate :
```bash
python run_bot.py --post-now
```

## 🏭 Mise en Production (Serveur Linux)

Pour que le bot tourne en permanence et redémarre automatiquement en cas de crash ou de reboot du serveur, nous utilisons **systemd**.

### 1. Préparer le fichier de service
Un modèle est disponible dans `utils/spotify-bot.service`. Copiez-le et éditez-le :

```bash
# Copier le fichier vers systemd
sudo cp utils/spotify-bot.service /etc/systemd/system/spotify-bot.service

# Éditer le fichier pour mettre vos propres chemins
sudo nano /etc/systemd/system/spotify-bot.service
```

⚠️ **Important** : Modifiez les lignes suivantes dans le fichier :
- `User=votre_utilisateur` (ex: `ubuntu` ou `root`)
- `WorkingDirectory=/home/votre_utilisateur/spotify` (chemin absolu vers le projet)
- `ExecStart=/home/votre_utilisateur/spotify/.venv/bin/python run_bot.py` (chemin vers python dans le venv)

### 2. Activer et démarrer le service

```bash
# Recharger la configuration systemd
sudo systemctl daemon-reload

# Activer le démarrage automatique au boot
sudo systemctl enable spotify-bot

# Démarrer le service maintenant
sudo systemctl start spotify-bot
```

### 3. Vérifier le statut et les logs

Pour voir si le bot tourne bien :
```bash
sudo systemctl status spotify-bot
```

Pour voir les logs en temps réel :
```bash
# Logs du service systemd
journalctl -u spotify-bot -f

# Ou consulter les logs de l'application
tail -f logs/threads_bot.log
```

### Alternative : Tâche Cron (Plus simple)

Si vous ne voulez pas laisser tourner un processus en permanence, vous pouvez utiliser une tâche **Cron** qui lancera le script une fois par jour.

1. Ouvrez l'éditeur de crontab :
```bash
crontab -e
```

2. Ajoutez la ligne suivante pour exécuter le bot tous les jours à 07h30 :
```bash
# m h  dom mon dow   command
30 07 * * * cd /home/votre_utilisateur/spotify && /home/votre_utilisateur/spotify/.venv/bin/python run_bot.py --post-now >> /home/votre_utilisateur/spotify/logs/cron.log 2>&1
```

⚠️ **Note** : Avec cette méthode, le paramètre `POSTING_TIME` dans le fichier `.env` est ignoré, c'est l'heure de la Cron qui fait foi.

## 📦 Structure du Projet

```
.
├── run_bot.py           # Point d'entrée principal
├── requirements.txt     # Dépendances
├── src/                 # Code source
│   ├── config.py        # Configuration
│   ├── spotify_client.py
│   ├── threads_client.py
│   └── scheduler.py
├── scripts/             # Outils de maintenance
│   ├── generate_token.py
│   └── diagnose_threads.py
└── utils/               # Fichiers utilitaires (systemd, etc.)
```