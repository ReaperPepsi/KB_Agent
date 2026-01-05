import re,json
from logs.logger import get_logger

data_normalizer_logger = get_logger('data_cleansing', 'data_cleansing.log')


def data_clansing(kb_list: dict):
    pattern_date =  r"\d{4}-\d{2}-\d{2}"
    pattern_kb = r"\d{2}.\d{1}.\d{4}.\d{1}"
    errors = 0
    json_cleansed = []
    if not kb_list:
        data_normalizer_logger.error(f"Empty kb list provided!")
        raise ValueError("Please provide a non empty list")
    else:
        data_normalizer_logger.info(f"Starting cleansing Data")
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
                    data_normalizer_logger.info(f"Can not perform data cleansing on {values}")
                    errors += 1
            json_cleansed.append(intermediar_list)

    versions = ["SQL_2025", "SQL_2022", "SQL_2019", "SQL_2017", "SQL_2016", "SQL_2014"]
    final_json = {}

    for version, kb_list in zip(versions, json_cleansed):
        final_json[version] = kb_list

    data_normalizer_logger.info(f"Data clansing process terminated with {errors} errors!")
    return final_json



def create_cleansed_json(cleansed_data):
    path = "D:\DBA_python\src\data_cleansing\kb_list_cleansed.json"
    if not cleansed_data:
        data_normalizer_logger.error(f"Empty list of data")
        raise ValueError("Please provide a valid list of data")
    else:
        data_normalizer_logger.info(f"Starting creating normalized JSON")
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(cleansed_data, file)
        data_normalizer_logger.info(f"{len(cleansed_data)} items written to JSON")
    
    data_normalizer_logger.info(f"Normalized JSON created!")
    return f"{len(cleansed_data)} items inserted in JSON file"


