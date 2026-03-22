import re,json, os, logging
from logs.logger import get_logger

logger = get_logger(
    name=__name__,
    filename="data_cleansing.log"
)


def data_cleansing(scrappend_json_raw:dict) -> list:
    cleansed_list = []
    error = 0
    pattern_date =  r"\d{4}-\d{2}-\d{2}"
    pattern_kb = r"\d{2}.\d{1}.\d{4}.\d{1}"

    logger.info(f"Starting cleansing Data")
    for item in scrappend_json_raw.values():
        intermediar_list = []
        for values in item:
            match_date = re.findall(pattern_date, values.get("release_date", []))
            match_kb   = re.findall(pattern_kb, values.get("kb", []))
            if match_date and match_kb:
                valid_date = ''.join(match_date)
                valid_kb = ''.join(match_kb)
                intermediar_list.append({"kb": valid_kb, "release_date": valid_date})

            else:
                error += 1
                logger.info(f"Can not perform data cleansing on {values}")
                
        cleansed_list.append(intermediar_list)
    
    logger.info(f"Data clansing process terminated with {error} errors!")
    return cleansed_list



def data_normalizer(kb_list: list) -> json:   
    if not kb_list:
        logger.error(f"Empty kb list provided!")
        errors += 1
        raise ValueError("Please provide a non empty list")
    else:
        final_json = {}
        versions = ["SQL_2025", "SQL_2022", "SQL_2019", "SQL_2017", "SQL_2016", "SQL_2014"]

        
        for version, kb_list in zip(versions, kb_list):
            final_json[version] = kb_list

    return final_json



def create_cleansed_json(cleansed_data):
    path = "/Users/reaper_pepsi/KB_Agent/src/data_cleansing/kb_list_cleansed.json"
    if not cleansed_data:
        logger.error(f"Empty list of data")
        raise ValueError("Please provide a valid list of data")
    else:
        logger.info(f"Starting creating normalized JSON")
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(cleansed_data, file)
        logger.info(f"{len(cleansed_data)} items written to JSON")

        with open(path, encoding="UTF-8") as file:
            json_cleansed = json.load(file) #data file with the ready to use JSON file
    
    logger.info(f"Normalized JSON created!")
    return json_cleansed

