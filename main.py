import logging
from trades.sniper import run_bot

logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    logging.info("Starting sniper bot in DEBUG mode...")
    run_bot()