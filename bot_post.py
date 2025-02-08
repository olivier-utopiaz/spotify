from spotify_client import SpotifyClient
from threads_client import ThreadsClient
from config import logger

def test_bot():
    try:
        # Test du client Spotify
        logger.info("Testing Spotify client...")
        spotify = SpotifyClient()
        genre = spotify.get_random_genre()
        album = spotify.get_random_album_by_genre(genre)
        
        if album:
            logger.info(f"Successfully retrieved album: {album['name']} by {album['artist']}")
            
            # Test du client Threads
            logger.info("Testing Threads client...")
            threads = ThreadsClient()
            success = threads.create_post(album)
            
            if success:
                logger.info("Test successful! Post created on Threads")
            else:
                logger.error("Failed to create post on Threads")
        else:
            logger.error("Failed to get album from Spotify")
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_bot()