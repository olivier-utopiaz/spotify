#!/usr/bin/env python3
"""
Script pour vérifier et renouveler le token Meta/Threads
"""
import os
import requests
import json
from datetime import datetime
import sys

def check_current_token():
    """Vérifie le token actuel"""
    access_token = os.getenv('META_ACCESS_TOKEN')
    user_id = os.getenv('INSTAGRAM_USER_ID')
    
    if not access_token:
        print("❌ META_ACCESS_TOKEN non trouvé dans l'environnement")
        return False
    
    print(f"🔍 Vérification du token: {access_token[:20]}...")
    
    # Test du token
    url = f"https://graph.threads.net/v1.0/{user_id}"
    params = {
        'fields': 'id,username,account_type',
        'access_token': access_token
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Token valide - Utilisateur: {data.get('username', 'N/A')}")
            return True
        else:
            error_data = response.json()
            print(f"❌ Token invalide - Status: {response.status_code}")
            print(f"❌ Erreur: {error_data.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def get_token_info():
    """Obtient des informations sur le token"""
    access_token = os.getenv('META_ACCESS_TOKEN')
    
    if not access_token:
        return
    
    # Vérifier les informations du token
    url = "https://graph.facebook.com/v22.0/me"
    params = {
        'fields': 'id,name',
        'access_token': access_token
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"📋 Token appartient à: {data.get('name', 'N/A')}")
        else:
            print(f"⚠️ Impossible d'obtenir les infos du token")
    except:
        pass

def exchange_for_long_lived_token():
    """Échange un token court contre un token long"""
    app_id = os.getenv('META_APP_ID')
    app_secret = os.getenv('META_APP_SECRET')
    current_token = os.getenv('META_ACCESS_TOKEN')
    
    if not all([app_id, app_secret, current_token]):
        print("❌ Impossible d'échanger le token - variables manquantes")
        print("   Vérifiez META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN")
        return None
    
    print("🔄 Tentative d'échange pour un token long...")
    
    url = "https://graph.facebook.com/v22.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': current_token
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            new_token = data.get('access_token')
            expires_in = data.get('expires_in', 'Unknown')
            
            print(f"✅ Nouveau token obtenu !")
            print(f"🕒 Expire dans: {expires_in} secondes")
            print(f"🔑 Nouveau token: {new_token[:30]}...")
            
            return new_token
        else:
            print(f"❌ Échec de l'échange - Status: {response.status_code}")
            print(f"❌ Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'échange: {e}")
        return None

def main():
    print("🔐 Diagnostic du token Meta/Threads")
    print("=" * 50)
    
    # Vérifier le token actuel
    is_valid = check_current_token()
    
    if is_valid:
        print("\n✅ Token valide - Aucune action nécessaire")
        get_token_info()
        return
    
    print("\n🔄 Token invalide - Tentative de renouvellement...")
    
    # Essayer d'échanger pour un token long
    new_token = exchange_for_long_lived_token()
    
    if new_token:
        print("\n📝 NOUVEAU TOKEN À UTILISER:")
        print(f"META_ACCESS_TOKEN={new_token}")
        print("\n💡 Mettez à jour votre fichier .env avec ce nouveau token")
    else:
        print("\n❌ Impossible de renouveler automatiquement")
        print("\n🔧 Solutions manuelles:")
        print("1. Allez sur https://developers.facebook.com")
        print("2. Sélectionnez votre app")
        print("3. Outils > Access Token Tool")
        print("4. Générez un nouveau User Access Token")
        print("5. Permissions requises: threads_basic, threads_content_publish")
        print("6. Échangez-le contre un Long-lived token")

if __name__ == "__main__":
    # Charger les variables d'environnement si un fichier .env existe
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main()
