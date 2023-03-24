import telebot
from utils import config, embedding, database

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
    user_text = message.text
    user_id = message.from_user.id
    user_embedding = embedding.get_embedding(user_text)
    user_details = [user_text, user_id, f"{user_embedding}"]
    user_details = ", ".join([f"'{value}'" for value in user_details])
    database.add_embedding_column(config.user_table_name)
    database.insert_data_from_user(user_details)
    bot.send_message(message.chat.id, f'I recieved your message. Please wait')
    result = [embedding.search(user_embedding)]
    print(len(result))
    # bot.send_message(message.chat.id, f'{embedding.search(user_embedding)}'[:1500])


bot.polling(none_stop=True)
