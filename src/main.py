from .scheduler import PostScheduler
from .config import logger

def main():
    try:
        scheduler = PostScheduler()
        logger.info("Starting music recommendation bot")
        scheduler.start()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()