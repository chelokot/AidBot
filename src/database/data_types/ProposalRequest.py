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

from typing import Dict, Optional, List, Any

from src.database.data_types.ColumnNames import ColumnNames
from src.embeddings.TextEmbedder import TextEmbedder
from abc import ABC, abstractmethod


class ProposalRequest:
    @staticmethod
    @abstractmethod
    def get_list_of_string_columns() -> List[str]:
        """
        Proposals and requests that we will get from different sources (uahelpers, other sites, directly from bot, etc.)
        will have different available info, so some columns will be empty.
        Each type of proposal/request must implement this method to return list of columns that will be filled.
        It is used while doing insert and select queries.
        ID and embedding columns are not included here, because it is obligatory for all types of proposals/requests to have them.
        """
        pass

    def __init__(self, characteristics: Dict[str, Any], embedder: Optional[TextEmbedder]):
        self.embedding = None
        self._characteristics = characteristics
        self._embedder = embedder

    def get_characteristic(self, characteristic: Any) -> Optional[Any]:
        return self._characteristics.get(characteristic, None)

    @abstractmethod
    def get_full_text(self) -> str:
        pass

    def get_insertion_query(self, table_name: str) -> str:
        # First, we get list of columns that are just strings and their corresponding values
        columns = self.get_list_of_string_columns()
        values = [self.get_characteristic(column) for column in columns]

        # Then, we get embedding
        columns.append(ColumnNames.proposal_embedding)
        values.append(str(self.embedding.get_list()))

        def error(value):
            raise ValueError(f"Value {value} is not int, float or str")

        # And format all string values with quotes '
        values = [
            (f"'{value}'" if type(value) == str else (str(value) if type(value) == int or type(value) == float else error(value)))
            if value is not None else "NULL" for value in values
        ]

        # Finally, we add ID column and its value
        columns.append(ColumnNames.id)
        values.insert(0, "DEFAULT")

        return f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
