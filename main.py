# main.py

from sniper.telegram_bot import bot

if __name__ == "__main__":
    print("Starting SniperBot polling...")
    bot.polling(none_stop=True)
