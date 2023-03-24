import telebot
from utils import config, embedding, database, formatting

bot = telebot.TeleBot(config.bot_token)

# Start bot method
@bot.message_handler(commands=['start'])
def start(message):
    localization = message.from_user.language_code
    welcome_message = f'{formatting.welcome_words[localization]}, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    welcome_message_line2 = f'{formatting.explanation[localization]}'
    bot.send_message(message.chat.id, welcome_message + '\n' + welcome_message_line2, parse_mode='html')


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
    database.insert_data_from_user(user_details)
    localization = message.from_user.language_code
    bot.send_message(message.chat.id, formatting.received[localization])
    result = formatting.format_search_result(embedding.search(user_embedding))
    bot.send_message(message.chat.id, result[:4000])

database.create_user_table(config.user_table_name)
database.add_embedding_column(config.user_table_name)
bot.polling(none_stop=True)
