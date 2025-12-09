import pyodbc

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
        return self.connection


    def close(self):
        if self.connection is None:
            raise ConnectionError("The connection is not opened for this object!")
        
        self.connection.close()
        self.connection = None
        print("Connection closed!")


    def test_query(self, query):
        self.query = query
         
        if self.connection is None:
            raise ConnectionError("The connection is not opened for this object!")
        
        if not self.query or self.query.strip() == '':
            raise ValueError("Query could not be empty")
        
        with self.connection.cursor() as cursor:
            cursor.execute(self.query)

        print(cursor.description)


    def execute_query(self,  query, params = None):
        self.query = query
        self.params = params

        if self.connection is None:
            raise ConnectionError("The connection is not opened for this object!")
        
        if not self.query or self.query.strip() == '':
            raise ValueError("Query could not be empty")
    
        with self.connection.cursor() as cursor:
            try:
                if params != None:
                    cursor.execute(self.query, self.params)
                else:
                    cursor.execute(self.query)
                

                if cursor.description:
                    rezultat = cursor.fetchall()
                    return rezultat
                else:
                    self.connection.commit()
                    return cursor.rowcount

            except Exception as e:
                self.connection.rollback()
                raise e

    


        
        
