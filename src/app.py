import yaml, json
from src.core.db.connectors.sql_connector import SQLConnector
from logs.logger import get_logger

logger = get_logger('db', 'db.log')

with open("config/config.dev.yaml", 'r') as file:
    config = yaml.full_load(file)

output = {
    "server": config['database']['server'],
    "database": config['database']['database'],
    "user": config['database']['username'],
    "password": config['database']['password']
}

with open("src/data_cleansing/kb_list_cleansed.json") as file:
    data = json.load(file) #data file with the ready to use JSON file

params = [(element.get("kb", []), element.get("release_date", [])) for element in data] #tuples pairs for parametrization
query = "INSERT INTO dbo.KB_Test (KB, Release_Date) VALUES (?, ?)" #ready to use T-SQL INSERT


inst_test = SQLConnector(output) #create a new instance
inst_test.create_connection() #create a new connection


for pairs in params:
    try:
        inst_test.execute_query(query, pairs) #execute pairs of parameters
    except Exception as e:
        logger.error(f"Failed to INSERT elements: {pairs} with the following error: {e}")
        continue

inst_test.close()




