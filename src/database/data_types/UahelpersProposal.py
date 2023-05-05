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

from src.database.data_types.ProposalRequest import ProposalRequest
from typing import Dict, Optional

from src.embeddings.Embedding import Embedding
from src.embeddings.TextEmbedder import TextEmbedder
from src.bot.TelegramBotUtils import TelegramBotUtils

from src.database.data_types.ColumnNames import ColumnNames



class UahelpersProposal(ProposalRequest):
    def __init__(self,
                 characteristics: Dict[str, str],
                 embedder: Optional[TextEmbedder],
    ):
        self._characteristics = characteristics
        self._embedder = embedder
        self._embedding = self._embedder.get_embedding(self.get_full_text()) if self._embedder is not None else None

    def get_characteristic(self, characteristic: str) -> Optional[str]:
        return self._characteristics.get(characteristic, None)

    def get_full_text(self) -> str:
        name        = self.get_characteristic(ColumnNames.proposal_name)
        description = self.get_characteristic(ColumnNames.proposal_description)
        comment     = self.get_characteristic(ColumnNames.proposal_comment)
        location    = self.get_characteristic(ColumnNames.proposal_location)
        services    = self.get_characteristic(ColumnNames.proposal_services)
        full_text = ""
        if name is not None:
            full_text += name
        if description is not None:
            full_text += ", " + description
        if comment is not None:
            full_text += ", " + comment
        if location is not None:
            full_text += ", " + location # For now, I add it to embedding, but we should handle it smarter -- compare with user location when possible
        if services is not None:
            full_text += ", " + services
        return full_text

    def get_pretty_text(self, localization: str) -> str:
        name        = self.get_characteristic(ColumnNames.proposal_name)
        description = self.get_characteristic(ColumnNames.proposal_description)
        contact     = self.get_characteristic(ColumnNames.proposal_contact)
        comment     = self.get_characteristic(ColumnNames.proposal_comment)
        location    = self.get_characteristic(ColumnNames.proposal_location)
        services    = self.get_characteristic(ColumnNames.proposal_services)
        date_time   = self.get_characteristic(ColumnNames.proposal_date_time)
        pretty_text = ""
        if name is not None:
            pretty_text += name + "\n"
        if description is not None:
            pretty_text += description + "\n"
        if contact is not None:
            pretty_text += contact + " | "
        if location is not None:
            pretty_text += location
        pretty_text += "\n"
        if comment is not None:
            pretty_text += comment + " | "
        if services is not None:
            pretty_text += services
        pretty_text += "\n"
        if date_time is not None:
            pretty_text += TelegramBotUtils.date_time_to_pretty_text(date_time, localization)
        return pretty_text

    @property
    def embedding(self) -> Embedding:
        return self._embedding
