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

from typing import Dict, Generic, TypeVar, Optional, Tuple

from src.embeddings.Embedding import Embedding
from src.embeddings.TextEmbedder import TextEmbedder
from src.database.data_types.ProposalRequest import ProposalRequest

EmbedType = TypeVar('EmbedType', bound=Embedding)

BOT_REQUEST_MESSAGE_TEXT = "message_text"


class BotRequest(ProposalRequest[EmbedType]):
    def __init__(self,
                 characteristics: Dict[str, str],
                 embedder: TextEmbedder[EmbedType],
                 answer_message_id: Optional[int],
                 start: int,
                 amount: int,
                 ):
        self._characteristics = characteristics
        self._embedder = embedder
        self._start = start
        self._amount = amount
        self._answer_message_id = answer_message_id
        self._embedding = self._embedder.get_embedding(self.get_full_text())

    def get_characteristic(self, characteristic: str) -> Optional[str]:
        return self._characteristics.get(characteristic, None)

    def get_full_text(self) -> str:
        message_text = self.get_characteristic(BOT_REQUEST_MESSAGE_TEXT)
        if message_text is None:
            return ""
        return message_text

    def get_pretty_text(self) -> str:
        return self.get_full_text()

    def get_start_and_amount(self) -> Tuple[int, int]:
        return self._start, self._amount

    def get_answer_message_id(self) -> Optional[int]:
        return self._answer_message_id

    @property
    def embedding(self) -> EmbedType:
        return self._embedding
