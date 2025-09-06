"""
Script de test pour vérifier la structure du bot sans les vraies clés API
"""
import sys
import os

# Ajouter le dossier src au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Simuler les variables d'environnement pour le test
os.environ.setdefault('SPOTIFY_CLIENT_ID', 'test_id')
os.environ.setdefault('SPOTIFY_CLIENT_SECRET', 'test_secret')
os.environ.setdefault('SPOTIFY_REDIRECT_URI', 'http://localhost:8080/callback')
os.environ.setdefault('META_ACCESS_TOKEN', 'test_token')
os.environ.setdefault('INSTAGRAM_USER_ID', 'test_user_id')
os.environ.setdefault('POSTING_TIME', '07:30')
os.environ.setdefault('TIMEZONE', 'Europe/Paris')

def test_imports():
    """Test des imports sans exécution réelle"""
    try:
        print("🔍 Test des imports...")
        
        # Test config
        from config import logger, SPOTIFY_CLIENT_ID
        print("✅ Config importé avec succès")
        
        # Test spotify_client (sans vraie connexion)
        print("🎵 Test Spotify client...")
        from spotify_client import SpotifyClient
        print("✅ SpotifyClient importé avec succès")
        
        # Test threads_client
        print("💬 Test Threads client...")
        from threads_client import ThreadsClient
        print("✅ ThreadsClient importé avec succès")
        
        # Test scheduler
        print("⏰ Test Scheduler...")
        from scheduler import PostScheduler
        print("✅ PostScheduler importé avec succès")
        
        print("\n🎉 Tous les imports fonctionnent !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_structure():
    """Test de la structure générale"""
    try:
        print("\n📋 Test de la structure...")
        
        # Vérifier les fichiers
        required_files = [
            'src/config.py',
            'src/spotify_client.py', 
            'src/threads_client.py',
            'src/scheduler.py',
            'requirements.txt'
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file}")
            else:
                print(f"❌ {file} manquant")
                return False
        
        # Vérifier le dossier logs
        if os.path.exists('logs'):
            print("✅ Dossier logs présent")
        else:
            print("❌ Dossier logs manquant")
            os.makedirs('logs', exist_ok=True)
            print("✅ Dossier logs créé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de structure: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'application Spotify-Threads Bot\n")
    
    structure_ok = test_structure()
    imports_ok = test_imports()
    
    if structure_ok and imports_ok:
        print("\n✅ Structure de l'application validée !")
        print("💡 Pour utiliser l'application sur le serveur :")
        print("   1. Assurez-vous que toutes les dépendances sont installées")
        print("   2. Créez le fichier .env avec vos vraies clés API")
        print("   3. Utilisez: python3 -m src.main pour lancer l'application")
    else:
        print("\n❌ Des problèmes ont été détectés")
        sys.exit(1)
