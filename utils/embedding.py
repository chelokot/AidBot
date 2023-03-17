
import psycopg

import openai
import config

openai.api_key = config.api_key


def get_descriptions():
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                 password=config.password, host=config.host)
    connection.autocommit = True
    descriptions = []
    try:
        descriptions = connection.execute('SELECT description from information').fetchall()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
    print(descriptions)
    descriptions = [description[0] for description in descriptions]
    return descriptions


def get_description_embedding(list_of_descriptions, model="text-embedding-ada-002"):
    list_of_descriptions = [item.replace("\n", " ") for item in list_of_descriptions]
    embeddings_json = openai.Embedding.create(input=list_of_descriptions, model=model)['data']
    return [item['embedding'] for item in embeddings_json]


def get_user_text_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    embeddings_json = openai.Embedding.create(input=[text], model=model)['data']
    return [item['embedding'] for item in embeddings_json]


list_of_desc = get_descriptions()
# print(list_of_desc)
print(get_description_embedding(list_of_desc))
