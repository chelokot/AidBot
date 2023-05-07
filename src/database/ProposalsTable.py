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
from src.database.data_types.ProposalRequest import ProposalRequest
from src.database.data_types.ColumnNames import ColumnNames

import psycopg


class ProposalsTable:
    __conn = DatabaseConnection()

    def __init__(self):
        self.connection = self.__conn.get_instance().conn  # type: psycopg.connection.Connection
        self.all_string_columns_names = ColumnNames.all_proposal_string_columns_names

    def add(self, proposal: ProposalRequest):
        cursor = self.connection.cursor()
        query  = proposal.get_insertion_query(site_table_name)
        try:
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(query)
            print(e)
        finally:
            cursor.close()

    def create_table_or_add_columns(self, table_name: str):
        """
        Creates table with name table_name if it does not exist with columns from ColumnNames.proposal_string_columns, id and embedding.
        If table already exists, it adds columns from ColumnNames.proposal_string_columns and embedding if they do not exist.
        Also registers vector extension.
        """
        self.connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
        proposal_string_columns = [
            f"{column_name} {ColumnNames.types[column_name]}" for column_name in self.all_string_columns_names
        ]
        self.connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} 
            (id SERIAL PRIMARY KEY, {", ".join(proposal_string_columns)}, embedding vector(1536))
        """)
        self.connection.execute(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS embedding vector(1536)')
        for proposal_string_column in proposal_string_columns:
            self.connection.execute(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {proposal_string_column}')

        register_vector(self.connection)

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
