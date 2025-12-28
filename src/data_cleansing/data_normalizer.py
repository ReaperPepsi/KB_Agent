import re, os, logging, json


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "data_cleansing.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def data_clansing(kb_list):
    pattern =  r"\d{4}-\d{2}-\d{2}"
    errors = 0
    final_list = []
    if not kb_list:
        logging.error(f"Empty kb list provided!")
        raise ValueError("Please provide a non empty list")
    else:
        logging.info(f"Starting cleansing Data")
        for item in kb_list:
            match = re.findall(pattern, item.get("release_date", []))
            if match:
                valid_output = ''.join(match)
                final_list.append({"kb": item.get("kb", []), "release_date": valid_output})
            else:
                logging.error(f"Can not perform data cleansing on {item}")
                errors += 1
    logging.info(f"Data clansing process terminated with {errors} errors!")
    return final_list



def create_cleansed_json(cleansed_data):
    path = "D:\DBA_python\src\data_cleansing\kb_list_cleansed.json"

    if not cleansed_data:
        logging.error(f"Empty list of data")
        raise ValueError("Please provide a valid list of data")
    else:
        logging.info(f"Starting creating normalized JSON")
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(cleansed_data, file)
        logging.info(f"{len(cleansed_data)} items written to JSON")
    
    logging.info(f"Normalized JSON created!")
    return f"{len(cleansed_data)} items inserted in JSON file"


test_list = [{"kb": "17.0.1000.7", "release_date": "2025-11-18*new"}, {"kb": "17.0.925.4", "release_date": "2025-09-16"}, {"kb": "17.0.900.7", "release_date": "2025-08-21"}, {"kb": "17.0.800.3", "release_date": "2025-06-16"}, {"kb": "17.0.700.9", "release_date": "2025-05-19"}, {"kb": "17.0.600.9", "release_date": "2025-04-10"}, {"kb": "17.0.17.0", "release_date": "2024-11-19"}, {"kb": "17.0.17.0", "release_date": ""}]