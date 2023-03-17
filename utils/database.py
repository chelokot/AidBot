import psycopg
from pgvector.psycopg import register_vector
from utils import config


def insert_data(list_of_values):

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


def add_embedding_column():
    connection = psycopg.connect(dbname=config.dbname, user=config.user,
                                  password=config.password, host=config.host)
    connection.autocommit = True
    connection.execute('CREATE EXTENSION IF NOT EXISTS vector')

    connection.execute('ALTER TABLE information DROP COLUMN IF EXISTS embedding')
    connection.execute('ALTER TABLE information ADD COLUMN embedding vector(1536)')
    register_vector(connection)
