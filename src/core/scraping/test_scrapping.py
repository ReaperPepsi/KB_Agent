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
    item_container = []

    if response.status_code in range(200, 400):
        soup = BeautifulSoup(response.text, 'html.parser')
        container_sql_2025 = soup.find_all('table')[3]
        
        collumn_data = container_sql_2025.find_all("tr")
        for row in collumn_data[1:]: 
            row_data = row.find_all('td') 
            test = [data.text for data in row_data[0]]
            release_date = row_data[-1].get_text(strip=True)
            row = {"kb": test[0], "release_date": release_date}
            item_container.append(row)

    logging.info(f"KB successfully scrapped")
    return item_container


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


