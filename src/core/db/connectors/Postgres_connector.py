import psycopg
from logs.logger import get_logger
from src.env import DATABASE_URL


logger = get_logger('db', 'db.log')

class SQLConnector:
    def __init__(self):
        self.connection = None
        self.connection_string = DATABASE_URL

    def open_connection(self):
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


    def execute_query(self, query, params=None):
        if self.connection is None:
            raise ConnectionError("The connection is not opened for this object!")

        if not query or query.strip() == '':
            raise ValueError("Query could not be empty")

        try:
            with self.connection.cursor() as cursor:
                logger.debug(f"Executing query: {query}" + (f" | Params: {params}" if params else ""))

                cursor.execute(query, params) if params else cursor.execute(query)

                if cursor.description:
                    result = cursor.fetchall()
                    logger.debug(f"Query returned {len(result)} rows")
                    return result

                self.connection.commit()
                logger.debug(f"Query affected {cursor.rowcount} rows")
                return cursor.rowcount

        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Query failed, rollback executed") from e
            