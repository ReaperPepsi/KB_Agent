import yaml
from src.core.scraping import check_connection, kb_scrapping, insert_data

with open("config/mac_config.yaml", 'r') as file:
    config = yaml.full_load(file)


url = config['sources']['ms_kb_url']
print(url)

response = check_connection(url)

scrapped = kb_scrapping(response)
insert_data(scrapped)

