import telebot
import os
import sqlite3

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def telegram_command_loop():
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(commands=['wallets'])
    def handle_wallets(message):
        bot.send_message(message.chat.id, "📡 Tracked wallets go here.")

    @bot.message_handler(commands=['limit'])
    def handle_limit(message):
        bot.send_message(message.chat.id, "💰 Daily Limit: $30 USD")

    @bot.message_handler(commands=['report'])
    def handle_report(message):
        try:
            conn = sqlite3.connect("trades.db")
            c = conn.cursor()
            c.execute("SELECT COUNT(*), SUM(profit) FROM trades")
            count, total_profit = c.fetchone()
            conn.close()
            bot.send_message(message.chat.id, f"📊 Trades: {count}
💵 Total Profit: ${total_profit or 0:.2f}")
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Error generating report: {e}")

    return bot

def send_telegram_message(text):
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    bot.send_message(TELEGRAM_CHAT_ID, text)
