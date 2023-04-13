# AidBot - Telegram bot project for finding volunteer help using semantic search
# Copyright (C) 2023
# Anastasia Mayorova aka EternityRei  <anastasiamayorova2003@gmail.com>
#    Andrey Vlasenko aka    chelokot   <andrey.vlasenko.work@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import psycopg
from pgvector.psycopg import register_vector
from utils import config
from utils.connection import Connection


def insert_data_from_site(list_of_values):
    connection = Connection.get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO {config.site_table_name} (id, name, description, contact, 
            comment, location, services, user_id, date_time, embedding) VALUES (default,{list_of_values}) """)
    except Exception as ex:
        print(f"""INSERT INTO {config.site_table_name} (name, description, contact, 
                    comment, location, services, user_id, date_time, embedding) VALUES ({list_of_values}) """)
        print(ex)
    finally:
        cursor.close()


def insert_data_from_user(list_of_user_values):
    connection = Connection.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO {config.user_table_name} (id, user_text, 
                                                user_id, embedding, start, amount) VALUES (default,{list_of_user_values})""")

    except Exception as ex:
        print(f"""INSERT INTO {config.user_table_name} (id, user_text, 
                                                user_id, embedding, start, amount) VALUES (default,{list_of_user_values})""")
        print(ex)
    finally:
        cursor.close()


def insert_reply_message_id(reply_message_id, user_text, user_id):
    connection = Connection.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE {config.user_table_name} SET reply_message_id = '{reply_message_id}' 
                                WHERE user_text = '{user_text}' AND user_id = '{user_id}'""")
    except Exception as ex:
        print(f"""UPDATE {config.user_table_name} SET reply_message_id = '{reply_message_id}' 
                                WHERE user_text = '{user_text}' AND user_id = '{user_id}'""")
        print(ex)
    finally:
        cursor.close()


def get_request(reply_message_id):
    connection = Connection.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT (embedding, start, amount) FROM {config.user_table_name} WHERE reply_message_id = '{reply_message_id}'""")
            return cursor.fetchone()
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()


def update_start(start, reply_message_id):
    connection = Connection.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE {config.user_table_name} SET start = {start} 
                                WHERE reply_message_id = '{reply_message_id}'""")
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()


def add_embedding_column(database_name):
    connection = Connection.get_connection()
    connection.execute('CREATE EXTENSION IF NOT EXISTS vector')

    connection.execute(f'ALTER TABLE {database_name} ADD COLUMN IF NOT EXISTS embedding vector(1536)')
    register_vector(connection)
    
def add_start_and_amount_columns(database_name):
    connection = Connection.get_connection()

    connection.execute(f'ALTER TABLE {database_name} ADD COLUMN IF NOT EXISTS start int')
    connection.execute(f'ALTER TABLE {database_name} ADD COLUMN IF NOT EXISTS amount int')

def add_reply_message_id_column(database_name):
    connection = Connection.get_connection()

    connection.execute(f'ALTER TABLE {database_name} ADD COLUMN IF NOT EXISTS reply_message_id varchar(50)')