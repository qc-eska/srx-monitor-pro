import telebot
from config import TELEGRAM_TOKEN, CHAT_ID

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_alert(message: str):
    bot.send_message(CHAT_ID, message)
