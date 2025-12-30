import requests, json,logging, os
from requests.exceptions import HTTPError, Timeout
from bs4 import BeautifulSoup


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "web_scrapping.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)



def check_connection(url):
    if not url:
        logging.error("Empty URL provided")
        raise ValueError("Please provide a valid URL")
    else:
        logging.info(f"Starting request to URL: {url}")
        try:
            response = requests.get(url, timeout=(3.05, 5))
            response.encoding = 'UTF-8'
            response.raise_for_status()
        except Timeout as tm:
            logging.error("Timeout occurred!")
            print('The request timeout!')
        except HTTPError as http_err:
            logging.error(f"HTTP Error occured: {http_err}")
            print("HTTP Error!")
        except Exception as ex:
            logging.error(f"Other error occured: {ex}")
            print("Error!")
        else:
            logging.info(f"{response} successfully created for URL: {url}!")
            return response
    


# check the status 
def kb_scapping(response):
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
    ("SQL_2022", collumn_data_2022)
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


    logging.info(f"KB successfully scrapped")
    return json_raw


def insert_data(kb_list):
    path = "D:\DBA_python\src\core\scraping\kb_list.json"

    if not kb_list:
        logging.error(f"Empty list of scrapped KB's")
        raise ValueError("Please provide a valid list of KB")
    else:
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(kb_list, file)
        logging.info(f"{len(kb_list)} items written to JSON")
    
    return f"{len(kb_list)} items inserted in JSON file"




