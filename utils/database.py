import psycopg
from pgvector.psycopg import register_vector
from utils import config


def insert_data_from_site(list_of_values):
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                 password=config.password, host=config.host)
    connection.autocommit = True

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO information (id, name, description, contact, 
            comment, location, services, user_id, date_time, embedding) VALUES (default,{list_of_values}) """)
    except Exception as ex:
        print(f"""INSERT INTO information (name, description, contact, 
                    comment, location, services, user_id, date_time, embedding) VALUES ({list_of_values}) """)
        print(ex)
    finally:
        cursor.close()
        connection.close()


def insert_data_from_user(list_of_user_values):
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                 password=config.password, host=config.host)
    connection.autocommit = True

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO user_information (id, user_text, 
                                                user_id, embedding) VALUES (default,{list_of_user_values}) """)
    except Exception as ex:
        print(f"""INSERT INTO user_information (id, user_text, 
                                                user_id, embedding) VALUES ({list_of_user_values})""")
        print(ex)
    finally:
        cursor.close()
        connection.close()


def create_user_table(table_name):
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                 password=config.password, host=config.host)
    connection.autocommit = True
    connection.execute('CREATE EXTENSION IF NOT EXISTS vector')

    connection.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        user_text VARCHAR(1000),
                        user_id VARCHAR(100),
                        embedding vector(1536)
                        )""")
    register_vector(connection)
    connection.close()


def add_embedding_column(database_name):
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                  password=config.password, host=config.host)
    connection.autocommit = True
    connection.execute('CREATE EXTENSION IF NOT EXISTS vector')

    connection.execute(f'ALTER TABLE {database_name} ADD COLUMN IF NOT EXISTS embedding vector(1536)')
    register_vector(connection)
