import yaml
from src.core.scraping import check_connection, kb_scrapping, insert_data
from src.data_cleansing.data_normalizer import data_cleansing, data_normalizer, create_cleansed_json

with open("config/mac_config.yaml", 'r') as file:
    config = yaml.full_load(file)


url = config['sources']['ms_kb_url']
print(url)

response = check_connection(url)

scrapped = kb_scrapping(response)
raw_json = insert_data(scrapped)


# test data cleansing
cleansed_data = data_cleansing(raw_json)
normalized_data = data_normalizer(cleansed_data)
create_cleansed_json(normalized_data)

