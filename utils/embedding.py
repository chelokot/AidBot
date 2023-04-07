# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import psycopg

import openai
from utils import config
from openai.embeddings_utils import get_embedding, cosine_similarity
from deep_translator import GoogleTranslator
import functools

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


@functools.lru_cache(maxsize=100, typed=False)
def get_request_and_proposal_embedding():
    request_template = "I need help, please help me with this problem I have, I need your help. Will take will buy will receive. I don't have I need I want I HAVE PROBLEM I'm disabled I'm looking for I HAVE NOTHING THIS IS SO BAD I'm starving and I'm sick my parent need medicals"
    proposal_template = "I can help you, here is my offer, I propose to help you with this problem, I can help you will give will sell will provide. We have we can gift, look what we have for you if you need I'm strong I have staff I have experience I have some things for you I have medicals to share. Have some amount of clothing and medicals and space"
    request_embedding = get_embedding(request_template)
    proposal_embedding = get_embedding(proposal_template)
    return request_embedding, proposal_embedding


def is_actully_request(embedding, text):
    request_embedding, proposal_embedding = get_request_and_proposal_embedding()
    return 0.975*cosine_similarity(embedding, request_embedding) > cosine_similarity(embedding, proposal_embedding)


def get_full_embedding(proposition):
    desc = proposition['description']
    name = proposition['name']
    location = proposition['location'] #For now I add it to embedding, but we should handle it smarter -- compare with user location when possible
    categories = ", ".join(proposition['services'])
    full_description = name + ' ' + desc + ' ' + categories + ' ' + location
    emb  = get_embedding(GoogleTranslator(source='auto', target='en').translate(full_description))
    return emb, is_actully_request(emb, full_description)


def search(embedding, start = 0, amount=5):
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                 password=config.password, host=config.host)
    cursor = connection.execute(f"SELECT * FROM information ORDER BY embedding <-> '{embedding}' LIMIT {amount} OFFSET {start}")
    return [item for item in cursor]
