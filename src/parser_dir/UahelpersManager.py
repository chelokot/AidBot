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

import requests
from bs4 import BeautifulSoup as bs
import json
from src.database.ProposalsTable import ProposalsTable
from src.embeddings.EmbeddingUtils import EmbeddingUtils
from src.embeddings.OpenAITextEmbedder import OpenAITextEmbedder
from src.config.BotConfig import api_key


class UahelpersManager:
    __has_more = True
    __skip_value = 0

    @staticmethod
    def __get_list_from_tag(dict_json, values_list):
        for tag in dict_json:
            values = dict_json[tag]
            if type(values) == list:
                values_list.append(", ".join(values))
            else:
                values_list.append(values)
        return values_list

    @staticmethod
    def __full_description(dict_json):
        desc = dict_json['description']
        name = dict_json['name']
        location = dict_json['location']  # For now, I add it to embedding, but we should handle it smarter -- compare with user location when possible
        categories = ", ".join(dict_json['services'])
        full_description = name + ' ' + desc + ' ' + categories + ' ' + location
        return full_description

    def __check_and_insert_data(self, is_request, values_list, emb):
        if not is_request:
            values_list.append(f"{emb}")
            values_fixed = [value.replace("'", "") for value in values_list]
            values_list_string = ", ".join([f"'{value}'" for value in values_fixed])
            self.db.insert_data_from_site(values_list_string)

    def __init__(self, dbname):
        self.db = ProposalsTable()
        self.db.add_embedding_column(dbname)
        self.ai = OpenAITextEmbedder(api_key)

        while self.__has_more:
            url = f'https://uahelpers.com/api/volunteers/search?location=&category=&skip={self.__skip_value}'
            response = requests.request("GET", url)

            parsed_text = bs(response.text, 'lxml')
            full_json_str = json.loads(parsed_text.find('p').text)

            self.__has_more = full_json_str['hasMore']
            result = full_json_str['result']

            for proposition in result:
                values_list = []
                proposition_json = json.dumps(proposition)
                dict_json = json.loads(proposition_json)

                values_list = self.__get_list_from_tag(dict_json, values_list)

                full_desc = self.__full_description(dict_json)

                emb = self.ai.get_embedding(full_desc, True)
                is_request = EmbeddingUtils.check_is_request(full_desc, emb)

                self.__check_and_insert_data(is_request, values_list, emb)
            self.__skip_value += len(result)



