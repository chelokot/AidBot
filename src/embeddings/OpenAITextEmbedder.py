# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>
from typing import Type

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or any later version. This
# program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

from src.embeddings.TextEmbedder import TextEmbedder
from src.embeddings.Embedding import Embedding
from src.embeddings.EmbeddingAda1536 import EmbeddingAda1536

import openai
from deep_translator import GoogleTranslator


class OpenAITextEmbedder(TextEmbedder):
    def __init__(self, api_key: str, embedding_type: Type = EmbeddingAda1536):
        self.api_key = api_key
        self.embedding_type = embedding_type

    def get_embedding(self, text: str, translate: bool = True) -> Embedding:
        openai.api_key = self.api_key
        if self.embedding_type == EmbeddingAda1536:
            text = text.replace("\n", " ")
            if translate:
                text = GoogleTranslator(source='auto', target='en').translate(text)
            embeddings_json = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
            return EmbeddingAda1536(embeddings_json['data'][0]['embedding'])
        else:
            raise NotImplementedError(f"Embedding type {self.embedding_type} is not supported with OpenAI API")
