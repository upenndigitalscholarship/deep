import srsly 
from pathlib import Path
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()

def validate_item(item:dict):
    driver.get(f"http://deep.sas.upenn.edu/{item['deep_id']}")
    deep_id = driver.find_element(By.XPATH, "/html/body/div/div[2]/table/tbody/tr[2]/td/div/div[1]/div[1]/div[1]").text.replace('DEEP #: ','')
    assert deep_id == item['deep_id'], 'error: '+ item['deep_id']

    record_type = driver.find_element(By.XPATH, '/html/body/div/div[2]/table/tbody/tr[2]/td/div/div[1]/div[2]/div[1]').text.replace('RECORD TYPE: ','')
    assert item['record_type'] == record_type, 'error: '+ item['record_type'] + ':' + record_type
    return item, False
            #number = record.find_element(By.CLASS_NAME, "numcol").text

class Command(BaseCommand):
    help = 'Check all item_json records against the old site'
    
    def handle(self, *args, **options):
        item_data = srsly.read_json(Path.cwd() / 'main/assets/data/item_data.json')
        item = item_data['23']
        updated_item, changed = validate_item(item)
        #for id, item in item_data.items():
            