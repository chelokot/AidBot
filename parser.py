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
    skip_value += 9
    print(parsed_text.prettify())
