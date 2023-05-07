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

from src.database.DatabaseConnection import DatabaseConnection
from src.config.DatabaseConfig import site_table_name
from pgvector.psycopg import register_vector

from typing import List

from src.database.ProposalsRequestsTable import ProposalsRequestsTable
from src.database.data_types.ProposalRequest import ProposalRequest
from src.database.data_types.ColumnNames import ColumnNames

import psycopg


class ProposalsTable(ProposalsRequestsTable):
    __conn = DatabaseConnection()

    def __init__(self):
        super().__init__()
        self.connection = self.__conn.get_instance().conn  # type: psycopg.connection.Connection
        self.all_string_columns_names = ColumnNames.all_proposal_string_columns_names

    def get_similar(self, request: ProposalRequest, start: int = 0, amount: int = 5) -> List[ProposalRequest]:
        embedding = request.embedding
        cursor = self.connection.cursor()
        cursor.execute(
            f"""SELECT {', '.join(ColumnNames.all_proposal_string_columns_names)}
            FROM {site_table_name} 
            ORDER BY embedding <-> %s 
            LIMIT %s OFFSET %s""",
            (str(embedding.get_list()), amount, start)
        )

        results = cursor.fetchall()
        cursor.close()
        proposals = []
        for result in results:
            proposals.append(
                ProposalRequest(
                    characteristics = dict(zip(ColumnNames.all_proposal_string_columns_names, result)),
                    embedder = None
                )
            )

        return proposals
