from sniper.telegram_bot import telegram_command_loop, send_telegram_message
from sniper.database import init_db

if __name__ == "__main__":
    init_db()
    telegram_command_loop()
