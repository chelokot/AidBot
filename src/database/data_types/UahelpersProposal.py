# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from src.database.data_types import ProposalRequest
from typing import List, Dict, Generic, TypeVar, Optional, Tuple

from src.embeddings.Embedding import Embedding
from src.embeddings.TextEmbedder import TextEmbedder
from src.bot.TelegramBotUtils import TelegramBotUtils

EmbedType = TypeVar('EmbedType', bound=Embedding)

UAHELPERS_PROPOSAL_NAME        = "name"
UAHELPERS_PROPOSAL_DESCRIPTION = "description"
UAHELPERS_PROPOSAL_CONTACT     = "contact"
UAHELPERS_PROPOSAL_COMMENT     = "comment"
UAHELPERS_PROPOSAL_LOCATION    = "location"
UAHELPERS_PROPOSAL_SERVICES    = "services"
UAHELPERS_PROPOSAL_DATE_TIME   = "date_time"

class UahelpersProposal(Generic[EmbedType], ProposalRequest):
    def __init__(self,
                 characteristics: Dict[str, str],
                 embedder: TextEmbedder[EmbedType],
    ):
        self._characteristics = characteristics
        self._embedder = embedder
        self._embedding = self._embedder.get_embedding(self.get_full_text())
    
    def get_characteristic(self, characteristic: str) -> Optional[str]:
        return self._characteristics.get(characteristic, None)

    def get_full_text(self) -> str:
        name        = self.get_characteristic(UAHELPERS_PROPOSAL_NAME)
        description = self.get_characteristic(UAHELPERS_PROPOSAL_DESCRIPTION)
        comment     = self.get_characteristic(UAHELPERS_PROPOSAL_COMMENT)
        location    = self.get_characteristic(UAHELPERS_PROPOSAL_LOCATION)
        services    = self.get_characteristic(UAHELPERS_PROPOSAL_SERVICES)
        full_text = ""
        if name is not None:
            full_text += name
        if description is not None:
            full_text += ", " + description
        if comment is not None:
            full_text += ", " + comment
        if location is not None:
            full_text += ", " + location
        if services is not None:
            full_text += ", " + services
        return full_text
    
    def get_pretty_text(self, localization:str) -> str:
        name        = self.get_characteristic(UAHELPERS_PROPOSAL_NAME)
        description = self.get_characteristic(UAHELPERS_PROPOSAL_DESCRIPTION)
        contact     = self.get_characteristic(UAHELPERS_PROPOSAL_CONTACT)
        comment     = self.get_characteristic(UAHELPERS_PROPOSAL_COMMENT)
        location    = self.get_characteristic(UAHELPERS_PROPOSAL_LOCATION)
        services    = self.get_characteristic(UAHELPERS_PROPOSAL_SERVICES)
        date_time   = self.get_characteristic(UAHELPERS_PROPOSAL_DATE_TIME)
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