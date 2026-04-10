import yaml, json
from src.core.scraping.test_scrapping import check_connection, kb_scrapping, insert_data
from src.data_cleansing.data_normalizer import data_normalizer, data_cleansing, create_cleansed_json
from src.core.db.connectors.Postgres_connector import SQLConnector
from logs.logger import get_logger


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
    
    query = "INSERT INTO public.KB_Scraped (KB, Release_Date) VALUES (%s, %s) ON CONFLICT (kb) DO NOTHING;" #ready to use T-SQL INSERT
    inst_test = SQLConnector() #create a new instance -> needs REFACTOR FOR POSTGRES
    inst_test.open_connection() #create a new connection

    for pairs in parameteres:
        try:
            inst_test.execute_query(query, pairs) #execute pairs of parameters
        except Exception as e:
            logger.error(f"Failed to INSERT elements: {pairs} with the following error: {e}")
            continue

    inst_test.close_connection()



def main():
    scrapped_data = web_scrapping_insert_json(url="https://sqlserverbuilds.blogspot.com/")
    cleansed_json = prepare_data_for_db(scrapped_data)
    sql_parameters = get_insert_parameter(cleansed_json)
    insert_data_sql(sql_parameters)


if __name__ == "__main__":
    main()
