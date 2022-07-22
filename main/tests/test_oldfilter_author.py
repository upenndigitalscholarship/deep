import srsly
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get("http://deep.sas.upenn.edu/advancedsearch.php")

def get_authors():
    output = [] 
    select = Select(driver.find_element(By.ID, 'type0'))
    select.select_by_value('author')

    author_select = Select(driver.find_element(By.ID, 'val0'))
    for opt in author_select.options:
        id = opt.get_attribute("value")
        if id == 'Please select...':
            continue
        elif id == '':
            continue
        else:
            name = opt.text
            data = dict(id=id, name=name)
            output.append(data)
    return output 


def filter_author(id:int):
    driver.get("http://deep.sas.upenn.edu/advancedsearch.php")

    select = Select(driver.find_element(By.ID, 'type0'))
    select.select_by_value('author')

    author_select = Select(driver.find_element(By.ID, 'val0'))
    author_select.select_by_value(str(id))

    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/form/input[3]").click()

    # Results page

    results = driver.find_element(By.ID, 'searchresults')
    records = results.find_elements(By.CLASS_NAME, "record") # get all of the rows in the table
    output = []
    for record in records:
        number = record.find_element(By.CLASS_NAME, "numcol").text
        resultsyear = record.find_element(By.CLASS_NAME, "resultsyear").text
        authorname = record.find_element(By.CLASS_NAME, "authorname").text
        playname = record.find_element(By.CLASS_NAME, "playname").text
        output.append(dict(number=number, year=resultsyear, author=authorname,play=playname))
    return output 

authors = get_authors()
data = []
for author in authors:
    author_data = {}
    author_data['id'] = author['id']
    author_data['name'] = author['name']
    author_data['results'] = filter_author(author['id'])
    data.append(author_data)
srsly.write_json('oldsite_byauthorModern_results.json',data)