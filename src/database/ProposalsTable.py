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
from DatabaseConfig import site_table_name
from pgvector.psycopg import register_vector


class ProposalsTable:
    __conn = DatabaseConnection()

    def __int__(self):
        self.connection = self.__conn.get_instance()

    def insert_data_from_site(self, list_of_values):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO {site_table_name} (id, name, description, contact, 
                comment, location, services, user_id, date_time, embedding) VALUES (default,{list_of_values}) """)
        except Exception as ex:
            print(f"""INSERT INTO {site_table_name} (name, description, contact, 
                        comment, location, services, user_id, date_time, embedding) VALUES ({list_of_values}) """)
            print(ex)
        finally:
            cursor.close()

    def add_embedding_column(self, database_name: object) -> object:
        self.connection.execute('CREATE EXTENSION IF NOT EXISTS vector')

        self.connection.execute(f'ALTER TABLE {database_name} ADD COLUMN IF NOT EXISTS embedding vector(1536)')
        register_vector(self.connection)

    def __del__(self):
        self.connection.close()

