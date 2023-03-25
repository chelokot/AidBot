from utils import config
import psycopg
class Connection:
    # This class is a singleton
    _instance = None

    def get_connection():
        if Connection._instance is None:
            Connection._instance = psycopg.connect(dbname=config.dbname, user=config.user,
                                                   password=config.password, host=config.host)
            Connection._instance.autocommit = True
        return Connection._instance