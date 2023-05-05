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

from typing import Dict, Optional
from src.embeddings.Embedding import Embedding
from src.embeddings.TextEmbedder import TextEmbedder
from abc import ABC, abstractmethod


class ProposalRequest(ABC):
    @abstractmethod
    def __init__(self, characteristics: Dict[str, str], embedder: TextEmbedder):
        pass

    @abstractmethod
    def get_full_text(self) -> str:
        pass

    @abstractmethod
    def get_characteristic(self, characteristic: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_pretty_text(self, localization: str) -> str:
        pass

    @property
    @abstractmethod
    def embedding(self) -> Embedding:
        pass


