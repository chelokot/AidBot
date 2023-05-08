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

import psycopg
from src.database.DatabaseConnection import DatabaseConnection
from src.database.ProposalsRequestsTable import ProposalsRequestsTable
from src.database.data_types.BotRequest import BotRequest
from src.config.DatabaseConfig import user_table_name
from src.database.data_types.ColumnNames import ColumnNames


class BotRequestsTable(ProposalsRequestsTable):
    __conn = DatabaseConnection()

    def __init__(self):
        super().__init__()
        self.connection = self.__conn.get_instance().conn  # type: psycopg.connection.Connection
        self.all_string_columns_names = ColumnNames.all_bot_request_string_columns_names
        self.table_name = user_table_name

    def add(self, request: BotRequest):
        super().add(request)

    def get_request(self, table_name: str, answer_message_id: int):
        cursor = self.connection.cursor()
        query = f"""SELECT ({", ".join(ColumnNames.all_bot_request_string_columns_names)}, {ColumnNames.proposal_embedding})
                    FROM {table_name}
                    WHERE {ColumnNames.bot_request_answer_message_id} = '{answer_message_id}'"""
        results = cursor.execute(query).fetchone()
        embedding = results[-1]
        user_proposal = None
        for result in results:
            user_proposal = BotRequest(
                characteristics=dict(zip(ColumnNames.all_bot_request_string_columns_names, result)),
                embedder=None,
                embedding=embedding
            )
        return user_proposal

    def update_start(self, table_name: str, start: int, answer_message_id: int):
        cursor = self.connection.cursor()
        query = f"""UPDATE {table_name} SET {ColumnNames.bot_request_start} = {start} 
                    WHERE {ColumnNames.bot_request_answer_message_id} = '{answer_message_id}'"""
        try:
            cursor.execute(query)
            cursor.close()
        except Exception as e:
            print(query)
            print(e)
        finally:
            cursor.close()
