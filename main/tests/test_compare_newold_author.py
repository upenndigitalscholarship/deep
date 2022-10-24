from pathlib import Path

import srsly

old_data = srsly.read_json('oldsite_byauthorModern_results.json')
new_data = srsly.read_json('newsite_byauthor_results.json')

error_log = """"""

def authors_match():
    for i in range(500):
        try:
            old_match = next(item for item in old_data if item["id"] == str(i))    
            new_match = next(item for item in new_data if item["id"] == i)  
            print(i, new_match['name'], old_match['name'])
            assert new_match['name'] == old_match['name']
        except Exception as e:
            print(i, e)

#Path('error.log').write_text(error_log)
authors_match()

def results_match(): 
    pass