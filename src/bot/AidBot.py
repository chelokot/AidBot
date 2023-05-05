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
from src.database.BotRequestsTable import BotRequestsTable
from src.bot.TelegramBotUtils import TelegramBotUtils

from src.embeddings.OpenAITextEmbedder import OpenAITextEmbedder
from src.embeddings.EmbeddingAda1536 import EmbeddingAda1536
from src.config.OpenAIConfig import openai_api_key

from src.database.data_types.BotRequest import BotRequest
from src.database.data_types.BotRequest import BOT_REQUEST_MESSAGE_TEXT

class AidBot:
    __proposals_table = ProposalsTable()
    __bot_requests_table = BotRequestsTable()
    __openai_text_embedder = OpenAITextEmbedder(openai_api_key, EmbeddingAda1536)
    __telebot = None

    def __init__(self, token):
        if AidBot.__telebot is not None:
            raise Exception("TelegramBot class is a singleton! Use get_instance() method to get the instance.")
        else:
            self.bot = telebot.TeleBot(token)  # type: telebot.TeleBot
            AidBot.__telebot = self

            @self.bot.message_handler(commands=['start'])
            def start(message):
                localization = message.from_user.language_code
                welcome_message = f'{TelegramBotUtils.get_welcome_message_text(localization)}, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
                welcome_message_line2 = f'{TelegramBotUtils.get_explanation_message_text(localization)}'
                self.bot.send_message(message.chat.id, welcome_message + '\n' + welcome_message_line2, parse_mode='html')

            @self.bot.message_handler(content_types=['text'])
            def get_user_text(message):
                user_text = message.text # type: str
                user_id = message.from_user.id # type: int
                localization = message.from_user.language_code # type: str

                # TODO: insert user details into database
                # user_embedding = embedding.get_embedding(user_text)
                # user_details = [user_text, user_id, f"{user_embedding}", 0, 5]
                # user_details = ", ".join([f"'{value}'" for value in user_details])
                #
                # database.insert_data_from_user(user_details)

                request = BotRequest(
                    characteristics = {
                        BOT_REQUEST_MESSAGE_TEXT: user_text
                    },
                    embedder = self.__openai_text_embedder,
                    answer_message_id = None,
                    start = 0,
                    amount = 5,
                )

                self.bot.send_message(message.chat.id, TelegramBotUtils.get_received_message_text(localization))

                result = TelegramBotUtils.format_proposal_results(
                    proposals = self.__proposals_table.get_similar(request),
                    localization = localization,
                )

                # We want to have buttons "Next" and "Previous" to show more results
                buttons = TelegramBotUtils.get_next_and_previous_buttons(localization, start = 0)

                api_reply = self.bot.send_message(
                    message.chat.id, result[:4000],
                    reply_markup=buttons, parse_mode='html'
                )

                # TODO: insert reply details into database
                # we want to save message_id to access user request later if they click on "Next" or "Previous"
                # database.insert_reply_message_id(api_reply.message_id, user_text, user_id)

    def start(self):
        self.bot.polling()

    @staticmethod
    def get_instance(token):
        if AidBot.__telebot is None:
            AidBot(token)
        return AidBot.__telebot
