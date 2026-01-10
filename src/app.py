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

logger = get_logger(
name=__name__,
filename="db.log")

# Web scrapping + JSON Insert function
def web_scrapping_insert_json(url):

    get_response = check_connection(url)
    container = kb_scrapping(get_response)
    data_to_insert = insert_data(container)

    return data_to_insert


# Data normalization + JSON Insert
def prepare_data_for_db(json_row):

    cleansed_data = data_cleansing(json_row)
    normalized_data = data_normalizer(cleansed_data)
    json_cleansed = create_cleansed_json(normalized_data)

    return json_cleansed


def get_insert_parameter(normalized_data):
    parameter_list = []
    for item in normalized_data.keys():
        for element in normalized_data.get(item):
            param = (element.get("kb", []), element.get("release_date"))
            parameter_list.append(param)

    return parameter_list


def insert_data_sql(parameteres):
    query = "INSERT INTO dbo.KB_Test (KB, Release_Date) VALUES (?, ?)" #ready to use T-SQL INSERT
    inst_test = SQLConnector(output) #create a new instance
    inst_test.create_connection() #create a new connection

    for pairs in parameteres:
        try:
            inst_test.execute_query(query, pairs) #execute pairs of parameters
        except Exception as e:
            logger.error(f"Failed to INSERT elements: {pairs} with the following error: {e}")
            continue

    inst_test.close()

    return None


scrapped_data = web_scrapping_insert_json(url="https://sqlserverbuilds.blogspot.com/")
cleansed_json = prepare_data_for_db(scrapped_data)
sql_parameters = get_insert_parameter(cleansed_json)

insert_data(sql_parameters)