import json
from typing import List

import srsly
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get("https://deep2.netlify.app/")

def get_authors():
    driver.get("https://deep2.netlify.app/assets/data/authors.json") 
    return json.loads(driver.find_element(By.TAG_NAME, "body").text)

def match_old_authors(authors:List[dict]):
    result = True
    data = srsly.read_json('oldsite_byauthorModern_results.json')
    for old_author in data: 
        id = old_author['id']
        name = old_author['name']
        # get author record from authors.json
        for item in authors:
            if item["value"] == id:
                if item['label'] == name:
                    continue
                else:
                    result = False
                    print('[error-1], mismatch old:' + id + name + 'new:' + str(item))
    return result

def filter_author(id:int, name:str):
    driver.get("https://deep2.netlify.app/")

    open_advanced = driver.find_element(By.XPATH, "/html/body/main/section/div/div/div[1]/div/div/p/a")
    open_advanced.click() 

    select = Select(driver.find_element(By.ID, 'searchSelect'))
    select.select_by_value('author')

    #click on choices
    driver.find_element(By.CLASS_NAME,'choices').click()
    
    # click on choice
    choices = driver.find_elements(By.CLASS_NAME, "choices__item")
    for choice in choices:
        try: # Ignore stale element exception
            if choice.text == name: 
                choice.click()
        except Exception as e:
            continue
    
    # Results page

    results = driver.find_element(By.XPATH, '/html/body/main/section/div/div/div[2]/div/table')
    records = results.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
    output = []
    for record in records:
        try: #author no results
            resultsyear = record.find_element(By.CLASS_NAME, "year").text
            authorname = record.find_element(By.CLASS_NAME, "authors_display").text
            playname = record.find_element(By.CLASS_NAME, "title").text
            output.append(dict(year=resultsyear, author=authorname,play=playname))
        except Exception as e:
            continue
    return output 

authors = get_authors()
#test author ids against old site
assert match_old_authors(authors)
data = []
for author in authors:
    author_data = {}
    author_data['id'] = author['value']
    author_data['name'] = author['label']
    author_data['results'] = filter_author(author['value'], author['label'])
    data.append(author_data)
srsly.write_json('newsite_byauthor_results.json',data)