import yaml, json, re
from src.core.db.connectors.sql_connector import SQLConnector
from src.core.scraping.test_scrapping import check_connection, kb_scapping, insert_data
from src.data_cleansing.data_normalizer import data_clansing, create_cleansed_json

with open("config/config.dev.yaml", 'r') as file:
    config = yaml.full_load(file)

output = {
    "server": config['database']['server'],
    "database": config['database']['database'],
    "user": config['database']['username'],
    "password": config['database']['password']
}



# scrape WEB + display response
response = check_connection(config["sources"]["ms_kb_url"])
container = kb_scapping(response)
insert_data(container)


# data cleansing part
path = "D:\DBA_python\src\core\scraping\kb_list.json"
with open(path, 'r') as f:
    data = json.load(f)

cleansed_data = data_clansing(data)
create_cleansed_json(cleansed_data)
    

'''with open("src/data_cleansing/kb_list_cleansed.json") as file:
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

inst_test.close()'''




