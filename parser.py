import requests
from bs4 import BeautifulSoup as bs
import json


has_more = True
skip_value = 0
while has_more:
    url = f'https://uahelpers.com/api/volunteers/search?location=&category=&skip={skip_value}'
    response = requests.request("GET", url)

    parsed_text = bs(response.text, 'lxml')
    full_json_str = json.loads(parsed_text.find('p').text)

    has_more = full_json_str['hasMore']
    result = full_json_str['result']

    for proposition in result:
        proposition_json = json.dumps(proposition)
        dict_json = json.loads(proposition_json)
        for tag in dict_json:
            values = dict_json[tag]
            if type(values) == list:
                print(tag, ", ".join(values))
            else:
                print(tag, values)
        print()

    skip_value += 9
