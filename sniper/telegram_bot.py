import telebot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_telegram_message(message):
    bot.send_message(TELEGRAM_CHAT_ID, message)

def telegram_command_loop():
    @bot.message_handler(commands=['wallets'])
    def handle_wallets(message):
        bot.send_message(message.chat.id, "📡 Tracked wallets go here.")

    @bot.message_handler(commands=['limit'])
    def handle_limit(message):
        bot.send_message(message.chat.id, "💰 Daily Limit: $30 USD")

    @bot.message_handler(commands=['report'])
    def handle_report(message):
        bot.send_message(message.chat.id, "📊 Sample report: $0 profit today.")

    return bot
