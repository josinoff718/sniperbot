import logging
from sniper_bot import start_bot  # Assuming the core logic is in this function/module

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Sniper Bot is starting...")
    try:
        start_bot()
    except Exception as e:
        logger.error(f"❌ Bot crashed with error: {e}")

if __name__ == "__main__":
    main()
 
