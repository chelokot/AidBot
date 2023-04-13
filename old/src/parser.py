# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup as bs
import json
from utils import database
from utils import embedding
from utils import config

has_more = True
skip_value = 0
database.add_embedding_column(config.site_table_name)
while has_more:
    url = f'https://uahelpers.com/api/volunteers/search?location=&category=&skip={skip_value}'
    response = requests.request("GET", url)

    parsed_text = bs(response.text, 'lxml')
    full_json_str = json.loads(parsed_text.find('p').text)

    has_more = full_json_str['hasMore']
    result = full_json_str['result']

    for proposition in result:
        values_list = []
        proposition_json = json.dumps(proposition)
        dict_json = json.loads(proposition_json)
        for tag in dict_json:
            values = dict_json[tag]
            if type(values) == list:
                values_list.append(", ".join(values))
            else:
                values_list.append(values)
        print()
        if len(values_list) == 7:
            values_list.append("null")

        emb, is_request = embedding.get_full_embedding(dict_json)
        
        if not is_request:
            values_list.append(f"{emb}")
            values_fixed = [value.replace("'", "") for value in values_list]
            values_list_string = ", ".join([f"'{value}'" for value in values_fixed])
            database.insert_data_from_site(values_list_string)
    skip_value += len(result)
