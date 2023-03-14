
def insert_data(list_of_values):
    import psycopg2
    import config

    connection = psycopg2.connect(dbname=config.dbname, user=config.user,
                                  password=config.password, host=config.host)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO information (name, description, contact, 
            comment, location, services, user_id, date_time) VALUES ({list_of_values}) """)
            connection.commit()
    except Exception as ex:
        print(f"""INSERT INTO information (name, description, contact, 
                    comment, location, services, user_id, date_time) VALUES ({list_of_values}) """)
        print(ex)
    finally:
        cursor.close()
        connection.close()
