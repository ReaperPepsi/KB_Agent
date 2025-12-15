import requests
from requests.exceptions import HTTPError, Timeout
from bs4 import BeautifulSoup

# check the status 
def check_status(urls):
    if not isinstance(urls, list) or not urls:
        raise ValueError("Please provide a valid list of URL's")
    for url in urls:
        try:
            response = requests.get(url, timeout=(3.05, 5))
            response.encoding = 'UTF-8'
            response.raise_for_status()
        except Timeout as tm:
            print('The request timeout!')
        except HTTPError as http_err:
            print(f"HTTP Error occured: {http_err}")
        except Exception as ex:
            print(f"Other error occured: {ex}")
        else:
            print(f"Success!\nStatus code: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')
            container_sql_2025 = soup.find_all('table')[3]

            collumn_data = container_sql_2025.find_all("tr")
            for row in collumn_data[1:]: 
                row_data = row.find_all('td') 
                test = [data.text for data in row_data[0]]
                release_date = row_data[-1].get_text(strip=True)
                print(test[0], release_date)


URLS = ['https://sqlserverbuilds.blogspot.com']

check_status(URLS)