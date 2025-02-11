import schedule
import time
from datetime import datetime
import pytz
import os
from config import TIMEZONE, logger
from spotify_client import SpotifyClient
from threads_client import ThreadsClient
import argparse
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement depuis .env

POSTING_TIME = os.getenv('POSTING_TIME')

class PostScheduler:
    def __init__(self):
        self.spotify = SpotifyClient()
        self.threads = ThreadsClient()
        self.timezone = pytz.timezone(TIMEZONE)
        logger.info("PostScheduler initialized")

    def post_daily_recommendation(self):
        """Publie une recommandation musicale quotidienne"""
        try:
            # Obtenir un genre et un album aléatoire
            genre = self.spotify.get_random_genre()
            album = self.spotify.get_random_album_by_genre(genre)

            if album:
                # Créer et publier le post
                success = self.threads.create_post(album)
                if success:
                    logger.info(f"Daily post successful for album: {album['name']}")
                else:
                    logger.error("Failed to create post")
            else:
                logger.error("Failed to get album recommendation")

        except Exception as e:
            logger.error(f"Error in daily posting routine: {str(e)}")

    def start(self):
        """Démarre le planificateur"""
        try:
            # Test immédiat
            logger.info("Running immediate test post...")
            self.post_daily_recommendation()
            
            # Puis planification normale
            schedule.every().day.at(POSTING_TIME).do(self.post_daily_recommendation)
            logger.info("Scheduler started")

            while True:
                schedule.run_pending()
                time.sleep(60)

        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PostScheduler CLI")
    parser.add_argument("--post-now", action="store_true", help="Force immediate posting and exit")
    args = parser.parse_args()

    scheduler = PostScheduler()

    if args.post_now:
        scheduler.post_daily_recommendation()
    else:
        scheduler.start()