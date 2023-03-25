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
    user_details = [user_text, user_id, f"{user_embedding}", 0, 5]
    user_details = ", ".join([f"'{value}'" for value in user_details])

    database.insert_data_from_user(user_details)

    localization = message.from_user.language_code
    bot.send_message(message.chat.id, formatting.received[localization])
    result = formatting.format_search_result(embedding.search(user_embedding))

    # We want to have buttons "Next" and "Previous" to show more results
    buttons = formatting.get_next_and_previous_buttons(localization)
    
    api_reply = bot.send_message(message.chat.id, result[:4000], reply_markup=buttons, parse_mode='html')

    # we want to save message_id to access user request later if they click on "Next" or "Previous"
    database.insert_reply_message_id(api_reply.message_id, user_text, user_id)


# Callback handler
# We want to have buttons "Next" and "Previous" to show more results
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        localization = call.from_user.language_code
        if call.data == 'next' or call.data == 'previous':
            request_embedding, start, amount = database.get_request(call.message.message_id)[0]
            start = int(start)
            amount = int(amount)
            if call.data == 'next':
                start += amount
                buttons = formatting.get_next_and_previous_buttons(localization, start)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=formatting.format_search_result(embedding.search(request_embedding, start, amount)))
                database.update_start(start, call.message.message_id)
            elif call.data == 'previous':
                if(start>0):
                    start -= amount
                    start = max(0, start)
                    buttons = formatting.get_next_and_previous_buttons(localization, start)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=formatting.format_search_result(embedding.search(request_embedding, start, amount)))
                    database.update_start(start, call.message.message_id)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=buttons)

database.add_start_and_amount_columns(config.user_table_name)
database.add_reply_message_id_column(config.user_table_name)
database.add_embedding_column(config.user_table_name)
bot.polling(none_stop=True)
