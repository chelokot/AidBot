import psycopg

import openai
from utils import config
from openai.embeddings_utils import get_embedding, cosine_similarity

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
    descriptions = [description[0] for description in descriptions]
    return descriptions


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    embeddings_json = openai.Embedding.create(input=[text], model=model)['data']
    return embeddings_json[0]['embedding']


def search(embedding, n=5):
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                 password=config.password, host=config.host)
    cursor = connection.execute(f"SELECT * FROM information ORDER BY embedding <-> '{embedding}' LIMIT {n}")
    return [item for item in cursor]
