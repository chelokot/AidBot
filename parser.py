import requests
from bs4 import BeautifulSoup as bs
import json
from utils import database
from utils import embedding

has_more = True
skip_value = 0
while has_more:
    url = f'https://uahelpers.com/api/volunteers/search?location=&category=&skip={skip_value}'
    response = requests.request("GET", url)

    parsed_text = bs(response.text, 'lxml')
    full_json_str = json.loads(parsed_text.find('p').text)

    has_more = full_json_str['hasMore']
    result = full_json_str['result']

    database.add_embedding_column()

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
        desc = dict_json['description']
        values_list.append(f"{embedding.get_embedding(desc)}")
        values_fixed = [value.replace("'", "") for value in values_list]
        values_list_string = ", ".join([f"'{value}'" for value in values_fixed])
        database.insert_data(values_list_string)
    skip_value += len(result)
