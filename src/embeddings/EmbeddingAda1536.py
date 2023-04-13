# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from typing import List
from embeddings.Embedding import Embedding

class EmbeddingAda1536(Embedding):
    def __init__(self, list: List[float]):
        if(len(list) != 1536):
            raise ValueError("EmbeddingAda1536 must be 1536-dimensional")
        if(type(list[0]) != float):
            raise ValueError("EmbeddingAda1536 must be float")
        self.list = list

    def get_list(self) -> List[float]:
        return self.list