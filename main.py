import logging
from sniper import SniperBot

logging.basicConfig(level=logging.INFO)
logging.info(">>> MAIN.PY STARTED <<<")

if __name__ == "__main__":
    logging.info("Initializing SniperBot...")
    bot = SniperBot()
    bot.run()