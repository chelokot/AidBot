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
from src.database.data_types.BotRequest import BotRequest
from src.config.DatabaseConfig import user_table_name
from src.database.data_types.ColumnNames import ColumnNames
from pgvector.psycopg import register_vector


class BotRequestsTable:
    __conn = DatabaseConnection()

    def __int__(self):
        self.connection = self.__conn.get_instance().conn   # type: psycopg.connection.Connection
        self.all_string_columns_names = ColumnNames.all_bot_request_string_columns_names

    def add(self, request: BotRequest):
        cursor = self.connection.cursor()
        query = request.get_insertion_query(user_table_name)
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
        Creates a table with name user_information if it does not exist from ColumnNames.request_string_columns, id and embedding.
        If table already exists, it adds columns from ColumnNames.request_string_columns and embedding if they do not exist.
        """
        self.connection.execute('CREATE EXTENSION IF NOT EXISTS vector')
        request_string_columns = [f"{column_name} {ColumnNames.length[column_name]}" for column_name in self.all_string_columns_names]
        self.connection.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} 
                    (id SERIAL PRIMARY KEY, {", ".join(request_string_columns)}, embedding vector(1536))
                """)
        self.connection.execute(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS embedding vector(1536)')
        for request_string_column in request_string_columns:
            self.connection.execute(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {request_string_column}')

        register_vector(self.connection)


