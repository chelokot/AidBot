import telebot

welcome_words = {
    'ru': 'Привет',
    'en': 'Hello',
    'ua': 'Привіт',
}

explanation = {
    'ru': 'Постарайтесь описать свою проблему максимально чётко, используя 10-20 слов. Попытайтесь описать какую конкретно помощь вы ищете(какие специалисты могут вам помочь, какая услуга или вещи вам нужны). Наш алгоритм автоматически предложит вам подходящих волонтеров и их контакты',
    'en': 'Try to describe your problem as clearly as possible using 10-20 words. Try to describe what kind of help you are looking for (which specialists can help you, what kind of service or things you need). Our algorithm will automatically suggest you suitable volunteers and their contacts',
    'ua': 'Спробуйте ясно описати свою проблему використовуючи 10-20 слів. Спробуйте описати яку саме допомогу ви шукаєте(які спеціалісти можуть вам допомогти, яка послуга або речі вам потрібні). Наш алгоритм автоматично запропонує вам підходящих волонтерів та їх контакти',
}

received = {
    'ru': 'Я получил ваше сообщение. Пожалуйста, подождите',
    'en': 'I received your message. Please wait',
    'ua': 'Я отримав ваше повідомлення. Будь ласка, зачекайте',
}


def _remove_columns_from_result(proposal):
    # We want to remove id, user_id and embedding from the result tuples
    proposal = proposal[1:-1] # id and embedding
    proposal = proposal[:-2] + (proposal[-1],) # user_id
    return proposal


def sort_by_date(proposals):
    return sorted(proposals, key=lambda x: x[6], reverse=True)


def format_proposal(proposal):
    return f"""{proposal[0]}
{proposal[1]}
{proposal[2]} | {proposal[4]}
{proposal[3]} | {proposal[5]}
Date: {proposal[6][:10]}
"""

def format_search_result(result):
    proposals = [_remove_columns_from_result(proposal) for proposal in result]
    proposals = sort_by_date(proposals)
    return "\n".join([format_proposal(proposal) for proposal in proposals])


def get_next_and_previous_buttons(localization, start = 0):
    next_text = {
        'ru': 'Далее',
        'en': 'Next',
        'ua': 'Далі',
    }[localization]
    previous_text = {
        'ru': 'Назад',
        'en': 'Previous',
        'ua': 'Назад',
    }[localization]
    buttons = telebot.types.InlineKeyboardMarkup()
    if(start != 0):
        buttons.add(telebot.types.InlineKeyboardButton(text=previous_text, callback_data='previous'),
                    telebot.types.InlineKeyboardButton(text=next_text, callback_data='next')
                    )
    else:
        buttons.add(telebot.types.InlineKeyboardButton(text=next_text, callback_data='next'))
    return buttons
