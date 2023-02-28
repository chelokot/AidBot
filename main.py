import telebot
import config

bot = telebot.TeleBot(config.bot_token)


# Start bot method
@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, welcome_message, parse_mode='html')


# Text handler
# Get embedding from user's text and check with parsed embeddings, which is stored in database
# If user's emb ~= stored emb -> return result
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
