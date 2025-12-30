import re, os, logging, json


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "data_cleansing.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def data_clansing(kb_list: dict):
    pattern_date =  r"\d{4}-\d{2}-\d{2}"
    pattern_kb = r"\d{2}.\d{1}.\d{4}.\d{1}"
    errors = 0
    json_cleansed = []
    if not kb_list:
        #logging.error(f"Empty kb list provided!")
        raise ValueError("Please provide a non empty list")
    else:
        #logging.info(f"Starting cleansing Data")
        for item in kb_list.values():
            intermediar_list = []
            for values in item:
                match_date = re.findall(pattern_date, values.get("release_date", []))
                match_kb   = re.findall(pattern_kb, values.get("kb", []))
                if match_date and match_kb:
                    valid_date = ''.join(match_date)
                    valid_kb = ''.join(match_kb)
                    intermediar_list.append({"kb": valid_kb, "release_date": valid_date})
                    
                else:
                    #logging.error(f"Can not perform data cleansing on {item}")
                    errors += 1
            json_cleansed.append(intermediar_list)

    versions = ["SQL_2025", "SQL_2022"]
    final_json = {}

    for version, kb_list in zip(versions, json_cleansed):
        final_json[version] = kb_list

    #logging.info(f"Data clansing process terminated with {errors} errors!")
    return final_json



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


