import requests
from bs4 import BeautifulSoup as bs
import json


def into_tuple(value):
    return tuple(i for i in value)


has_more = True
skip_value = 0
while has_more:
    url = f'https://uahelpers.com/api/volunteers/search?location=&category=&skip={skip_value}'
    response = requests.request("GET", url)
    parsed_text = bs(response.text, 'lxml')
    full_json_str = json.loads(parsed_text.find('p').text)
    has_more = full_json_str['hasMore']
    result = full_json_str['result']
    result_json = json.dumps(result[0])  # THIS
    dict_json = json.loads(result_json)
    for tag in dict_json:  # THIS
        values = dict_json[tag]
        if type(values) == list:
            tuple_values = into_tuple(values)
            print(tuple_values.__getitem__(0))
        else:
            print(values)
    skip_value += 9
