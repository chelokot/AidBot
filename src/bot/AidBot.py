# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or any later version. This
# program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

import telebot
from src.database.ProposalsTable import ProposalsTable
from src.bot.TelegramBotUtils import TelegramBotUtils


class AidBot:
    __proporsals_table = ProporsalsTable()
    __bot_requests_table = BotRequestsTable()
    __telebot = None

    def __init__(self, token):
        if AidBot.__telebot is not None:
            raise Exception("TelegramBot class is a singleton! Use get_instance() method to get the instance.")
        else:
            self.bot = telebot.TeleBot(token)
            AidBot.__telebot = self

            @self.bot.message_handler(commands=['start'])
            def start(message):
                localization = message.from_user.language_code
                welcome_message = f'{TelegramBotUtils.get_welcome_message_text(localization)}, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
                welcome_message_line2 = f'{TelegramBotUtils.get_explanation_message_text(localization)}'
                self.bot.send_message(message.chat.id, welcome_message + '\n' + welcome_message_line2, parse_mode='html')

    @staticmethod
    def get_instance(token):
        if AidBot.__telebot is None:
            AidBot(token)
        return AidBot.__telebot
