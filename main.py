from sniper.database import init_db
from sniper.telegram_bot import telegram_command_loop

if __name__ == "__main__":
    init_db()
    telegram_command_loop()
