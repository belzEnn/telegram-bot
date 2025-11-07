import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

# Command processingd
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Command: ...")

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
