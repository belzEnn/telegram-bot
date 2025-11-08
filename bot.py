import telebot
from telebot import types
from config import BOT_TOKEN
from services.weather_api import get_weather
from services.currency import convert_currency

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "👋 Hello!\n\n *Use /help to get a list of commands*", parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, "*List of bot commands*\n/help - List of commands\n/weather <city> - Weather in the selected city\n/convert <amount> <from> <to> - Currency conversion", parse_mode='Markdown')

#
@bot.message_handler(commands=['weather'])
def cmd_weather(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2 and parts[1].strip():
        city_raw = parts[1]
        reply = get_weather(city_raw)
        bot.send_message(message.chat.id, reply, parse_mode='Markdown')
        return

    msg = bot.send_message(message.chat.id, "Please send the city name (e.g. Kyiv)")
    bot.register_next_step_handler(msg, handle_city_step)
    
@bot.message_handler(commands=["convert"])
def convert_command(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Please use format: `/convert 1000 UAH USD`", parse_mode="Markdown")
        return

    query = parts[1]
    result = convert_currency(query)
    bot.reply_to(message, result, parse_mode="Markdown")

def handle_city_step(message):
    city_raw = message.text or ""
    reply = get_weather(city_raw)
    bot.send_message(message.chat.id, reply, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
