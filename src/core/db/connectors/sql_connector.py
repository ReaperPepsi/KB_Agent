import pyodbc
from logs.logger import get_logger

logger = get_logger('db', 'db.log')


class SQLConnector:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connection_string = (
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={self.config['server']};"  # sau IP-ul instanței tale
                f"Database={self.config['database']};"
                f"UID={self.config['user']};"
                f"PWD={self.config['password']};"
                "TrustServerCertificate=yes;"
                "timeout = 30;"
        )

    def create_connection(self):
        self.connection = pyodbc.connect(self.connection_string)
        if self.connection:
            logger.info("Connection created successfully!")
        return self.connection


    def close(self):
        if self.connection is None:
            logger.error(f"No connection was opened! Connection value = {self.connection}")
            raise ConnectionError("The connection is not opened for this object!")
        
        self.connection.close()
        self.connection = None
        logger.info("Connection closed!")
        return None


    def execute_query(self,  query, params = None):
        self.query = query
        self.params = params

        if self.connection is None:
            logger.error(f"No connection opened for this object! Connection value = {self.connection}")
            raise ConnectionError("The connection is not opened for this object!")
        
        if not self.query or self.query.strip() == '':
            logger.error(f"Empty query provided! Query value = {self.query[:6]}")
            raise ValueError("Query could not be empty")
        
        if not self.params or not self.params[0] or not self.params[1]:
            logger.error(f"Empty parameter provided! {self.params}")
            raise ValueError("Parameters could not be empty")
        

        logger.info("Starting the query execution")
        with self.connection.cursor() as cursor:
            try:
                logger.info(f"Query executing: {self.query}")
                if params != None:
                    logger.info(f"Parameters of the query: {self.params}")
                    cursor.execute(self.query, self.params)
                else:
                    cursor.execute(self.query)

                if cursor.description:
                    rezultat = cursor.fetchall()
                    return rezultat
                else:
                    self.connection.commit()
                    logger.info(f"Query executed successfully! {cursor.rowcount} affected entries")
                    return cursor.rowcount

            except Exception as e:
                self.connection.rollback()
                logger.error(f"Query terminated with the following error: {e}! Rollback!")
                raise e
                

