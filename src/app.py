import yaml, pyodbc, sys, os
from core.db.connectors.sql_connector import SQLConnector

# Obține calea absolută a rădăcinii proiectului
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Asigură-te că e primul path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import stabil
from tests.tests import *

with open("config/config.dev.yaml", 'r') as file:
    config = yaml.full_load(file)

output = {
    "server": config['database']['server'],
    "database": config['database']['database'],
    "user": config['database']['username'],
    "password": config['database']['password']
}

inst_test = SQLConnector(output)

inst_test.create_connection()
print(inst_test.execute_query(query_test_insert_with_params[0], query_test_insert_with_params[1]))
print(inst_test.execute_query("SELECT * FROM dbo.Test"))



#inst1.close()


