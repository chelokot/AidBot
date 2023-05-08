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

from typing import Dict, List, Optional, Any

from src.database.data_types.ColumnNames import ColumnNames
from src.embeddings.Embedding import Embedding
from src.embeddings.TextEmbedder import TextEmbedder
from src.database.data_types.ProposalRequest import ProposalRequest


class BotRequest(ProposalRequest):
    @staticmethod
    def get_list_of_string_columns() -> List[str]:
        return [
            ColumnNames.description,
            ColumnNames.bot_request_start, ColumnNames.bot_request_amount, ColumnNames.bot_request_answer_message_id
        ]

    def __init__(self, characteristics: Dict[str, Any], embedder: Optional[TextEmbedder], embedding: Optional[Embedding] = None):
        super().__init__(characteristics, embedder)
        self.embedding = (self._embedder.get_embedding(self.get_full_text()) if self._embedder is not None else None) \
            if embedding is None else embedding

    def get_full_text(self) -> str:
        message_text = self.get_characteristic(ColumnNames.description)
        if message_text is None:
            return ""
        return message_text

