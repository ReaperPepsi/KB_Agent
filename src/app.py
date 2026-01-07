import yaml, json
from src.core.db.connectors.sql_connector import SQLConnector
from src.core.scraping.test_scrapping import check_connection, kb_scrapping, insert_data
from src.data_cleansing.data_normalizer import data_normalizer, data_cleansing, create_cleansed_json
from logs.logger import get_logger


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
container = kb_scrapping(response)
insert_data(container)


# data cleansing part
path = r"D:\DBA_python\src\core\scraping\kb_list.json"
with open(path, 'r') as f:
    data = json.load(f)


cleansed_data = data_cleansing(data)
normalized_data = data_normalizer(cleansed_data)
create_cleansed_json(normalized_data)
    

logger = get_logger(
    name=__name__,
    filename="db.log"
)

with open("src/data_cleansing/kb_list_cleansed.json") as file:
    data = json.load(file) #data file with the ready to use JSON file


parameters = []
for item in data.keys():
    for element in data.get(item):
        param = (element.get("kb", []), element.get("release_date"))
        parameters.append(param)



query = "INSERT INTO dbo.KB_Test (KB, Release_Date) VALUES (?, ?)" #ready to use T-SQL INSERT

inst_test = SQLConnector(output) #create a new instance
inst_test.create_connection() #create a new connection


for pairs in parameters:
    try:
        inst_test.execute_query(query, pairs) #execute pairs of parameters
    except Exception as e:
        logger.error(f"Failed to INSERT elements: {pairs} with the following error: {e}")
        continue

inst_test.close()