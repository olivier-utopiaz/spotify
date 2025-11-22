#!/usr/bin/env python3
"""
Script pour lister les permissions disponibles et générer un token Threads
"""
import os
import requests
import webbrowser
from urllib.parse import urlencode

def generate_auth_url():
    """Génère l'URL d'autorisation pour obtenir un token avec les bonnes permissions"""
    
    app_id = os.getenv('META_APP_ID') or input("📱 Entrez votre META_APP_ID: ")
    redirect_uri = "https://localhost/"  # URI simple pour récupérer le code
    
    # Permissions Threads essentielles
    scope = "threads_basic,threads_content_publish,instagram_basic"
    
    params = {
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'response_type': 'code',
        'state': 'threads_bot_auth'
    }
    
    auth_url = f"https://threads.net/oauth/authorize?{urlencode(params)}"
    
    print("🔗 URL d'autorisation générée:")
    print("=" * 60)
    print(auth_url)
    print("=" * 60)
    
    print("\n📋 Instructions:")
    print("1. Copiez cette URL dans votre navigateur")
    print("2. Connectez-vous avec le compte lié à votre app")
    print("3. Autorisez les permissions demandées")
    print("4. Récupérez le 'code' dans l'URL de redirection")
    print("5. Utilisez ce code pour obtenir un access_token")
    
    open_browser = input("\n🌐 Ouvrir automatiquement dans le navigateur ? (y/n): ")
    if open_browser.lower() == 'y':
        webbrowser.open(auth_url)
    
    return auth_url

def exchange_code_for_token():
    """Échange un code d'autorisation contre un access token"""
    
    app_id = os.getenv('META_APP_ID') or input("📱 META_APP_ID: ")
    app_secret = os.getenv('META_APP_SECRET') or input("🔐 META_APP_SECRET: ")
    redirect_uri = "https://localhost/"
    
    code = input("📝 Entrez le code d'autorisation récupéré: ")
    
    url = "https://graph.threads.net/oauth/access_token"
    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            
            print(f"\n✅ Token obtenu:")
            print(f"🔑 {access_token}")
            
            # Échanger pour un token long
            print(f"\n🔄 Échange pour un token long...")
            long_token = exchange_for_long_lived(app_id, app_secret, access_token)
            
            if long_token:
                print(f"\n🎉 TOKEN FINAL À UTILISER:")
                print(f"META_ACCESS_TOKEN={long_token}")
            
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def exchange_for_long_lived(app_id, app_secret, short_token):
    """Échange un token court contre un token long"""
    
    url = "https://graph.facebook.com/v22.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            print(f"⚠️ Impossible d'obtenir un token long: {response.text}")
            return short_token
            
    except Exception as e:
        print(f"⚠️ Erreur échange token long: {e}")
        return short_token

def main():
    print("🔐 Générateur de Token Threads")
    print("=" * 40)
    
    choice = input("""
Que voulez-vous faire ?
1. Générer une URL d'autorisation
2. Échanger un code contre un token
3. Les deux étapes

Votre choix (1/2/3): """)
    
    if choice in ['1', '3']:
        generate_auth_url()
        
    if choice in ['2', '3']:
        print("\n" + "="*40)
        exchange_code_for_token()

if __name__ == "__main__":
    # Charger les variables d'environnement si disponibles
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main()
