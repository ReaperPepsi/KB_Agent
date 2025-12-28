import json
from src.data_cleansing.data_normalizer import test_list

kb_ready = "D:\DBA_python\src\data_cleansing\kb_list_cleansed.json"

with open(kb_ready, 'r', encoding='UTF-8') as file:
    data = json.load(file)



def create_insert_command(json_data):
    queries = []
    if not json_data:
        raise ValueError("Please provide an existing JSON file")
    
    for element in json_data:
        query = f' """INSERT INTO dbo.TestKB (KB, Release_Date) VALUES(?, ?)""", ({str(element.get('kb'))}, {str(element.get('release_date'))})'
        queries.append(query)

    print(queries)

