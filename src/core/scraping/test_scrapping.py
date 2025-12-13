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
            soup = BeautifulSoup(response.text, 'html.parser')
            h1_tags = soup.find_all('p')
            print(f"Success!\nStatus code: {response.status_code}\nContent: {response.text}")
            for h1 in h1_tags:
                print(f"{h1}")

URLS = ['https://example.com']

check_status(URLS)