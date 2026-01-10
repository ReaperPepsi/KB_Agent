import requests, json
from requests.exceptions import HTTPError, Timeout
from bs4 import BeautifulSoup

from logs.logger import get_logger

logger = get_logger(
    name=__name__,
    filename="web_scrapping.log"
)


def check_connection(url):
    if not url:
        logger.error("Empty URL provided")
        raise ValueError("Please provide a valid URL")
    else:
        logger.info(f"Starting request to URL: {url}")
        try:
            response = requests.get(url, timeout=(3.05, 5))
            response.encoding = 'UTF-8'
            response.raise_for_status()
        except Timeout as tm:
            logger.error("Timeout occurred!")
            print('The request timeout!')
        except HTTPError as http_err:
            logger.error(f"HTTP Error occured: {http_err}")
            print("HTTP Error!")
        except Exception as ex:
            logger.error(f"Other error occured: {ex}")
            print("Error!")
        else:
            logger.info(f"{response} successfully created for URL: {url}!")
            return response




# check the status 
def kb_scrapping(response):
    json_raw = {}
    if response.status_code in range(200, 400):
        soup = BeautifulSoup(response.text, 'html.parser')
        container_sql_2025 = soup.find_all('table')[3] # -> SQL 2025
        container_sql_2022 = soup.find_all('table')[4] # -> SQL 2022
        container_sql_2019 = soup.find_all('table')[5] # -> SQL 2019
        container_sql_2017 = soup.find_all('table')[6] # -> SQL 2017
        container_sql_2016 = soup.find_all('table')[7] # -> SQL 2016
        container_sql_2014 = soup.find_all('table')[8] # -> SQL 2014
        
        collumn_data_2025 = container_sql_2025.find_all("tr")
        collumn_data_2022 = container_sql_2022.find_all("tr")
        collumn_data_2019 = container_sql_2019.find_all("tr")
        collumn_data_2017 = container_sql_2017.find_all("tr")
        collumn_data_2016 = container_sql_2016.find_all("tr")
        collumn_data_2014 = container_sql_2014.find_all("tr")

        data_list = [
    ("SQL_2025", collumn_data_2025),
    ("SQL_2022", collumn_data_2022),
    ("SQL_2019", collumn_data_2019),
    ("SQL_2017", collumn_data_2017),
    ("SQL_2016", collumn_data_2016),
    ("SQL_2014", collumn_data_2014)
]

    for version, rows in data_list:
        item_container = []
        for row in rows[1:]: 
            row_data = row.find_all('td') 
            kb = [data.text for data in row_data[0]]
            release_date = row_data[-1].get_text(strip=True)
            row = {"kb": kb[0], "release_date": release_date}
            item_container.append(row)
            json_raw[version] =  item_container


    logger.info(f"KB successfully scrapped")
    return json_raw


def insert_data(kb_list):
    path = "D:\DBA_python\src\core\scraping\kb_list.json"

    if not kb_list:
        logger.error(f"Empty list of scrapped KB's")
        raise ValueError("Please provide a valid list of KB")
    else:
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(kb_list, file)
        logger.info(f"{len(kb_list)} items written to JSON")

    with open(path, 'r') as f:
        data = json.load(f)

    return data




