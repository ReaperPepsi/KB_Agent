import json
kb_ready = "D:\DBA_python\src\data_cleansing\kb_list_cleansed.json"

with open(kb_ready, 'r', encoding='UTF-8') as file:
    data = json.load(file)

query_test_insert_with_params = ['''INSERT INTO dbo.KB_Test ([KB], [Release_Date]) VALUES (?, ?)''', (f'{data[0].get("kb", [])}', f'{data[0].get("release_date", [])}')]


