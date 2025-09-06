#!/usr/bin/env python3
"""
Script de diagnostic pour l'API Threads
Vérifie la configuration et teste les endpoints API
"""
import os
import requests
import json
from src.config import META_ACCESS_TOKEN, INSTAGRAM_USER_ID, logger

def test_threads_api():
    """Test de l'API Threads avec diagnostic détaillé"""
    
    print("🔍 Diagnostic de l'API Threads")
    print("=" * 40)
    
    # Vérification des variables
    if not META_ACCESS_TOKEN or META_ACCESS_TOKEN == 'test_token':
        print("❌ META_ACCESS_TOKEN manquant ou invalide")
        return False
    
    if not INSTAGRAM_USER_ID or INSTAGRAM_USER_ID == 'test_user_id':
        print("❌ INSTAGRAM_USER_ID manquant ou invalide") 
        return False
    
    print(f"✅ Token présent: {META_ACCESS_TOKEN[:10]}...")
    print(f"✅ User ID: {INSTAGRAM_USER_ID}")
    
    # Test 1: Vérification du token
    print("\n📋 Test 1: Vérification du token...")
    try:
        url = f"https://graph.threads.net/v1.0/{INSTAGRAM_USER_ID}"
        params = {
            'fields': 'id,username,account_type',
            'access_token': META_ACCESS_TOKEN
        }
        
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Utilisateur: {data.get('username', 'N/A')}")
            print(f"✅ Type: {data.get('account_type', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Test de création de post (sans publication)
    print("\n📋 Test 2: Test de création de conteneur...")
    try:
        url = f"https://graph.threads.net/v1.0/{INSTAGRAM_USER_ID}/threads"
        headers = {
            'Authorization': f'Bearer {META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        data = {
            'text': '🧪 Test de diagnostic du bot - ce message ne sera pas publié',
            'media_type': 'TEXT'
        }
        
        response = requests.post(url, json=data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            container_id = response.json().get('id')
            print(f"✅ Conteneur créé: {container_id}")
            
            # Ne pas publier le test, juste vérifier qu'on peut créer
            print("ℹ️ Conteneur non publié (test uniquement)")
            return True
        else:
            print(f"❌ Erreur création: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de création: {e}")
        return False

def check_api_permissions():
    """Vérifie les permissions de l'API"""
    print("\n📋 Vérification des permissions...")
    
    required_permissions = [
        'threads_basic',
        'threads_content_publish'
    ]
    
    print("Permissions requises:")
    for perm in required_permissions:
        print(f"  - {perm}")
    
    print("\n💡 Assurez-vous que votre app Meta a ces permissions")
    print("💡 Le token doit être de type 'User Access Token'")
    print("💡 L'utilisateur doit avoir confirmé l'utilisation de Threads")

if __name__ == "__main__":
    # Vérifier si on a les vraies clés
    if (not os.getenv('META_ACCESS_TOKEN') or 
        os.getenv('META_ACCESS_TOKEN') == 'test_token'):
        print("❌ Aucune vraie clé API détectée")
        print("💡 Configurez votre fichier .env avec les vraies clés pour ce test")
        exit(1)
    
    success = test_threads_api()
    check_api_permissions()
    
    if success:
        print("\n✅ API Threads fonctionnelle !")
    else:
        print("\n❌ Problèmes détectés avec l'API Threads")
        print("\n🔧 Solutions possibles:")
        print("  1. Vérifiez que votre token est valide et non expiré")
        print("  2. Vérifiez les permissions de votre app Meta")
        print("  3. Vérifiez que l'INSTAGRAM_USER_ID est correct")
        print("  4. Vérifiez que l'utilisateur a activé Threads")
