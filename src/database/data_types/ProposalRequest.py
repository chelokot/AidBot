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

from typing import Dict, Optional, List

from src.database.data_types.ColumnNames import ColumnNames
from src.embeddings.TextEmbedder import TextEmbedder
from abc import ABC, abstractmethod


class ProposalRequest:
    @staticmethod
    @abstractmethod
    def get_list_of_columns() -> List[str]:
        """
        Proposals and requests that we will get from different sources (uahelpers, other sites, directly from bot, etc.)
        will have different available info, so some columns will be empty.
        Each type of proposal/request must implement this method to return list of columns that will be filled.
        It is used while doing insert and select queries.
        ID and embedding columns are not included here, because it is obligatory for all types of proposals/requests to have them.
        """
        pass

    def __init__(self, characteristics: Dict[str, str], embedder: Optional[TextEmbedder]):
        self.embedding = None
        self._characteristics = characteristics
        self._embedder = embedder

    def get_characteristic(self, characteristic: str) -> Optional[str]:
        return self._characteristics.get(characteristic, None)

    @abstractmethod
    def get_full_text(self) -> str:
        pass

    def get_pretty_text(self, localization: str) -> str:
        name = self.get_characteristic(ColumnNames.proposal_name)
        description = self.get_characteristic(ColumnNames.description)
        contact = self.get_characteristic(ColumnNames.proposal_contact)
        comment = self.get_characteristic(ColumnNames.proposal_comment)
        location = self.get_characteristic(ColumnNames.proposal_location)
        services = self.get_characteristic(ColumnNames.proposal_services)
        date_time = self.get_characteristic(ColumnNames.proposal_date_time)
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
            from src.bot.TelegramBotUtils import TelegramBotUtils
            pretty_text += TelegramBotUtils.date_time_to_pretty_text(date_time, localization)
        return pretty_text

    def get_insertion_query(self, table_name: str) -> str:
        columns = self.get_list_of_columns()
        values = [self.get_characteristic(column) for column in columns]

        columns.append(ColumnNames.proposal_embedding)
        values.append(str(self.embedding.get_list()))
        values = [f"'{value}'" if value is not None else "NULL" for value in values]

        columns.append(ColumnNames.id)
        values.insert(0, "DEFAULT")

        return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
