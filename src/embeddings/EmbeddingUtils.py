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

from src.embeddings.TextEmbedder import TextEmbedder
from typing import Tuple, TypeVar
from src.embeddings.Embedding import Embedding
import functools
from openai.embeddings_utils import cosine_similarity

EmbedType = TypeVar('EmbedType', bound=Embedding)


class EmbeddingUtils:
    @staticmethod
    def check_is_request(model: TextEmbedder[EmbedType], embedding: EmbedType) -> bool:
        request_embedding, proposal_embedding = EmbeddingUtils._get_default_request_and_proposal_embeddings(model)
        return 0.975 * cosine_similarity(embedding.get_list(), request_embedding.get_list()) > cosine_similarity(embedding.get_list(), proposal_embedding.get_list())

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def _get_default_request_and_proposal_embeddings(model: TextEmbedder[EmbedType]) -> Tuple[EmbedType, EmbedType]:
        request_template = "I need help, please help me with this problem I have, I need your help. Will take will " \
                           "buy will receive. I don't have I need I want I HAVE PROBLEM I'm disabled I'm looking for " \
                           "I HAVE NOTHING THIS IS SO BAD I'm starving and I'm sick my parent need medicals"
        proposal_template = "I can help you, here is my offer, I propose to help you with this problem, I can help " \
                            "you will give will sell will provide. We have we can gift, look what we have for you if " \
                            "you need I'm strong I have staff I have experience I have some things for you I have " \
                            "medicals to share. Have some amount of clothing and medicals and space"
        request_embedding = model.get_embedding(request_template)
        proposal_embedding = model.get_embedding(proposal_template)
        return request_embedding, proposal_embedding
