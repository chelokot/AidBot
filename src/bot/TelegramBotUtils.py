# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import telebot
from typing import List

from src.database.data_types.ColumnNames import ColumnNames
from src.database.data_types.ProposalRequest import ProposalRequest
import datetime


class TelegramBotUtils:
    __welcome_words = {
        'ru': 'Привет',
        'en': 'Hello',
        'ua': 'Привіт',
    }

    __explanation = {
        'ru': 'Постарайтесь описать свою проблему максимально чётко, используя 10-20 слов. Попытайтесь описать какую '
              'конкретно помощь вы ищете(какие специалисты могут вам помочь, какая услуга или вещи вам нужны). Наш '
              'алгоритм автоматически предложит вам подходящих волонтеров и их контакты',
        'en': 'Try to describe your problem as clearly as possible using 10-20 words. Try to describe what kind of '
              'help you are looking for (which specialists can help you, what kind of service or things you need). '
              'Our algorithm will automatically suggest you suitable volunteers and their contacts',
        'ua': 'Спробуйте ясно описати свою проблему використовуючи 10-20 слів. Спробуйте описати яку саме допомогу ви '
              'шукаєте(які спеціалісти можуть вам допомогти, яка послуга або речі вам потрібні). Наш алгоритм '
              'автоматично запропонує вам підходящих волонтерів та їх контакти',
    }

    __received = {
        'ru': 'Я получил ваше сообщение. Пожалуйста, подождите',
        'en': 'I received your message. Please wait',
        'ua': 'Я отримав ваше повідомлення. Будь ласка, зачекайте',
    }

    @staticmethod
    def get_welcome_message_text(localization: str) -> str:
        return TelegramBotUtils.__welcome_words[localization]

    @staticmethod
    def get_explanation_message_text(localization: str) -> str:
        return TelegramBotUtils.__explanation[localization]

    @staticmethod
    def get_received_message_text(localization: str) -> str:
        return TelegramBotUtils.__received[localization]

    @staticmethod
    def get_next_and_previous_buttons(localization: str, start: int):
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
        if start != 0:
            buttons.add(telebot.types.InlineKeyboardButton(text=previous_text, callback_data='previous'),
                        telebot.types.InlineKeyboardButton(text=next_text, callback_data='next'))
        else:
            buttons.add(telebot.types.InlineKeyboardButton(text=next_text, callback_data='next'))
        return buttons

    @staticmethod
    def get_pretty_text(proposal: ProposalRequest, localization: str) -> str:
        """
        This function used to get pretty text from some specific proposal
        Such text will be inserted into message to user
        """
        name        = proposal.get_characteristic(ColumnNames.proposal_name)
        description = proposal.get_characteristic(ColumnNames.description)
        contact     = proposal.get_characteristic(ColumnNames.proposal_contact)
        comment     = proposal.get_characteristic(ColumnNames.proposal_comment)
        location    = proposal.get_characteristic(ColumnNames.proposal_location)
        services    = proposal.get_characteristic(ColumnNames.proposal_services)
        date_time   = proposal.get_characteristic(ColumnNames.proposal_date_time)
        pretty_text = ""
        if name is not None:
            pretty_text += name + "\n"
        if description is not None:
            pretty_text += description + "\n"
        if contact is not None:
            pretty_text += contact + " | "
        if location is not None:
            pretty_text += location
        pretty_text += "\n"
        if comment is not None:
            pretty_text += comment + " | "
        if services is not None:
            pretty_text += services
        pretty_text += "\n"
        if date_time is not None:
            pretty_text += TelegramBotUtils.date_time_to_pretty_text(date_time, localization)
        return pretty_text

    @staticmethod
    def format_proposal_results(proposals: List[ProposalRequest], localization: str) -> str:
        """
        This function takes list of proposals, formats each of them into pretty text and returns
        all of them as one string
        """
        return '\n\n'.join([TelegramBotUtils.get_pretty_text(proposal, localization) for proposal in proposals])

    @staticmethod
    def date_time_to_pretty_text(date_time: str, localization: str) -> str:
        """
        This function takes date_time in format '2020-05-05T12:00:00.000Z' and returns it in format '05-05-2020'
        With also adding 'Дата: ' or 'Date: ' before it
        """
        try:
            original_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            date_time = datetime.datetime.strptime(date_time, original_date_format) # type: datetime.datetime
            date_format = '%d-%m-%Y'
            if localization == 'ru':
                return f'Дата: {date_time.strftime(date_format)}'
            elif localization == 'en':
                return f'Date: {date_time.strftime(date_format)}'
            elif localization == 'ua':
                return f'Дата {date_time.strftime(date_format)}'
            else:
                return f'{date_time.strftime(date_format)}'
        except Exception as e:
            print(e, date_time)
            return date_time
