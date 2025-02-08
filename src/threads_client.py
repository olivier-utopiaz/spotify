import requests
from config import (
    META_ACCESS_TOKEN,
    INSTAGRAM_USER_ID,
    GREETINGS,
    MORNING_MESSAGES,
    logger
)
import random
from datetime import datetime

class ThreadsClient:
    def __init__(self):
        self.access_token = META_ACCESS_TOKEN
        self.api_url = "https://graph.threads.net/v1.0"
        self.user_id = INSTAGRAM_USER_ID
        logger.info("Threads client initialized")

    def create_post(self, album_info):
        """Crée et publie un post sur Threads"""
        try:
            # Jour de la semaine en français
            days = {
                0: 'lundi', 1: 'mardi', 2: 'mercredi', 3: 'jeudi',
                4: 'vendredi', 5: 'samedi', 6: 'dimanche'
            }
            current_day = days[datetime.now().weekday()]

            # Construire le message
            greeting = random.choice(GREETINGS)
            morning_msg = random.choice(MORNING_MESSAGES).format(current_day)
            
            message = f"""{greeting}
{morning_msg}
Pas trop ronchon en ce début de matinée 🙂‍↔️

Non. Bon cool, un p'tit café ☕️ ou un thé 🍵 et c'est parti pour s'écouter du bon son 🔊
Ce matin, ça sera ambiance {album_info['genre']} 🔊 🤩

Un peu de soleil pour nos oreilles ☀️
👨‍🎤 Artiste : {album_info['artist']}
💿 Album : {album_info['name']}
📆 Année : {album_info['release_date']}
🎶 Genre : #{album_info['genre'].capitalize()}

🎧 Écouter : {album_info['url']}"""

            # Étape 1 : Créer un conteneur de post
            create_endpoint = f"{self.api_url}/{self.user_id}/threads"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            data = {
                'text': message,
                'media_type': 'TEXT'
            }

            # Envoi de la requête POST
            response = requests.post(create_endpoint, json=data, headers=headers)

            if response.status_code == 200:
                creation_id = response.json().get('id')
                logger.info(f"Post container created successfully with ID: {creation_id}")
            else:
                logger.error(f"Failed to create post container. Status: {response.status_code}")
                logger.error(f"Response: {response.json()}")
                return False

            # Étape 2 : Publier le conteneur
            publish_endpoint = f"{self.api_url}/{self.user_id}/threads_publish"
            data_publish = {
                    'creation_id': creation_id,
                    'access_token': self.access_token
                }

            response = requests.post(publish_endpoint, json=data_publish, headers=headers)

            if response.status_code == 200:
                post_id = response.json().get('id')
                logger.info(f"Post published successfully with ID: {post_id}")
                return True
            else:
                logger.error(f"Failed to publish post. Status: {response.status_code}")
                logger.error(f"Response: {response.json()}")
                return False

        except Exception as e:
            logger.error(f"Error creating or publishing post: {str(e)}")
            return False
