import psycopg
from logs.logger import get_logger
from src.env import DATABASE_URL


logger = get_logger('db', 'db.log')

class SQLConnector:
    def __init__(self):
        self.connection = None
        self.connection_string = DATABASE_URL

    def create_connection(self):
        try:
            if not self.connection:
                self.connection = psycopg.connect(self.connection_string)
            return self.connection
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Connection closed!")





