import os
import telebot
from sniper.database import get_trade_count, get_total_profit

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['limit'])
def handle_limit(message):
    bot.send_message(message.chat.id, "💰 Daily Limit: $30 USD")

@bot.message_handler(commands=['report'])
def handle_report(message):
    try:
        count = get_trade_count()
        total_profit = get_total_profit()
        bot.send_message(message.chat.id, f"📊 Trades: {count}")
        bot.send_message(message.chat.id, f"💵 Total Profit: ${total_profit or 0:.2f}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error generating report: {str(e)}")

@bot.message_handler(commands=['wallets'])
def handle_wallets(message):
    bot.send_message(message.chat.id, "📡 Tracked wallets go here.")

def telegram_command_loop():
    print("🤖 Bot started listening for commands...")
    bot.polling(none_stop=True, interval=1, timeout=20, threaded=True)
