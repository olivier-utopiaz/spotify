#!/usr/bin/env python3
"""
Script de lancement principal pour le bot Spotify-Threads
Usage: python3 run_bot.py [--test] [--post-now] [--help]
"""
import sys
import os
import argparse
from pathlib import Path

# Ajouter le dossier racine au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Vérifie que l'environnement est correctement configuré"""
    required_env_vars = [
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET', 
        'META_ACCESS_TOKEN',
        'INSTAGRAM_USER_ID'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Variables d'environnement manquantes:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Créez un fichier .env avec ces variables ou définissez-les dans votre environnement")
        return False
    
    return True

def test_imports():
    """Test des imports sans exécution"""
    try:
        print("🔍 Test des imports...")
        
        from src.config import logger
        print("✅ Config OK")
        
        from src.spotify_client import SpotifyClient
        print("✅ SpotifyClient OK")
        
        from src.threads_client import ThreadsClient  
        print("✅ ThreadsClient OK")
        
        from src.scheduler import PostScheduler
        print("✅ PostScheduler OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_test():
    """Lance un test simple"""
    try:
        from src.spotify_client import SpotifyClient
        from src.threads_client import ThreadsClient
        from src.config import logger
        
        print("🧪 Test du bot...")
        
        # Test Spotify (si les clés sont présentes)
        if os.getenv('SPOTIFY_CLIENT_ID') and os.getenv('SPOTIFY_CLIENT_ID') != 'test_id':
            try:
                spotify = SpotifyClient()
                genre = spotify.get_random_genre()
                print(f"✅ Spotify: Genre aléatoire = {genre}")
            except Exception as e:
                print(f"⚠️ Spotify: {e}")
        else:
            print("⚠️ Spotify: Pas de vraies clés API (mode test)")
        
        # Test Threads (simulation)
        try:
            threads = ThreadsClient()
            print("✅ Threads: Client initialisé")
        except Exception as e:
            print(f"⚠️ Threads: {e}")
        
        print("✅ Test terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Bot Spotify-Threads")
    parser.add_argument("--test", action="store_true", help="Mode test uniquement")
    parser.add_argument("--post-now", action="store_true", help="Poster immédiatement")
    parser.add_argument("--check-env", action="store_true", help="Vérifier l'environnement")
    
    args = parser.parse_args()
    
    print("🎵 Bot Spotify-Threads")
    print("=" * 30)
    
    # Vérification de base des imports
    if not test_imports():
        print("❌ Problème avec les imports")
        sys.exit(1)
    
    # Vérification de l'environnement
    if args.check_env:
        if check_environment():
            print("✅ Environnement correctement configuré")
        sys.exit(0)
    
    # Mode test
    if args.test:
        if run_test():
            print("✅ Tests passés")
        else:
            print("❌ Tests échoués")
        sys.exit(0)
    
    # Vérification de l'environnement pour l'exécution normale
    if not check_environment():
        print("\n💡 Utilisez --test pour tester sans les vraies clés API")
        sys.exit(1)
    
    # Exécution normale
    try:
        from src.scheduler import PostScheduler
        
        scheduler = PostScheduler()
        
        if args.post_now:
            print("📤 Post immédiat...")
            scheduler.post_daily_recommendation()
        else:
            print("⏰ Démarrage du scheduler...")
            scheduler.start()
            
    except KeyboardInterrupt:
        print("\n👋 Arrêt du bot")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
