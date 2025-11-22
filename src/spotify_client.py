import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional, Dict, Any
from .config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    MUSIC_GENRES,
    logger
)
import random

class SpotifyClient:
    def __init__(self) -> None:
        # Utiliser Client Credentials Flow pour éviter les problèmes de serveur local
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        logger.info("Spotify client initialized with Client Credentials")

    def get_random_album_by_genre(self, genre: str) -> Optional[Dict[str, Any]]:
        """Récupère un album aléatoire pour un genre donné"""
        try:
            # Recherche d'albums pour le genre
            results = self.sp.search(
                q=f"genre:{genre}",
                type="album",
                limit=50
            )
            
            if not results['albums']['items']:
                logger.warning(f"No albums found for genre: {genre}")
                return None
            
            album = random.choice(results['albums']['items'])
            
            return {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'release_date': album['release_date'][:4],  # Année uniquement
                'genre': genre,
                'url': album['external_urls']['spotify']
            }
        except Exception as e:
            logger.error(f"Error getting album for genre {genre}: {str(e)}")
            return None

    def get_random_genre(self) -> str:
        """Retourne un genre aléatoire depuis la liste des genres configurés"""
        return random.choice(list(MUSIC_GENRES.keys()))