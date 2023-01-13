from pathlib import Path

import requests
import srsly
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm
from pathlib import Path

backup_dir = Path.cwd() / 'backup'

#TODO some fields contain formatting information, ex. 5.html Additional notes.
# get_text removes all tags. they can be transferred with decode_contents() https://stackoverflow.com/questions/8112922/beautifulsoup-innerhtml
class Command(BaseCommand):
    help = 'This is a test script to assess which fields and how many records have HTML formatting in them'
    
    def handle(self, *args, **options):
        items = []
        log = """"""
        for html_doc in tqdm(backup_dir.glob('*.html')):
        #for html_doc in tqdm([(backup_dir / '5077.html')]):
            item = {}
            soup = BeautifulSoup(html_doc.read_bytes(), 'html.parser')
            try:
                in_collection = soup.find('span', text = 'In Collection:').parent.decode_contents().replace('In Collection:','').strip().encode('ISO-8859-1').decode('utf-8')
                if '<i>' in in_collection or '<b>' in in_collection:
                    print(html_doc.stem,in_collection)    
            except:
                pass
            try:
                collection_contains = soup.find('span', text = 'Collection contains:').parent.decode_contents().replace('Collection contains:','').strip().encode('ISO-8859-1').decode('utf-8')
                if '<i>' in collection_contains or '<b>' in collection_contains:
                    print(html_doc.stem,collection_contains)    
            except:
                pass
            try:
                variants = soup.find('span', text = 'Variants:').parent.decode_contents().replace('Variants:','').strip().encode('ISO-8859-1').decode('utf-8')
                if '<i>' in variants or '<b>' in variants:
                    print(html_doc.stem,variants)    
            except:
                pass
            try:
                independent_playbook = soup.find('span', text = 'Also appears as a bibliographically independent playbook in').parent.decode_contents().replace('Also appears as a bibliographically independent playbook in','').strip().encode('ISO-8859-1').decode('utf-8')
                if '<i>' in independent_playbook or '<b>' in independent_playbook:
                    print(html_doc.stem,independent_playbook)  
            except:
                pass
            try:
                also_in_collection = soup.find('span', text = 'Also appears in collection:').parent.decode_contents().replace('Also appears in collection:','').strip().encode('ISO-8859-1').decode('utf-8')
                if '<i>' in also_in_collection or '<b>' in also_in_collection:
                    print(html_doc.stem,also_in_collection)  
            except:
                pass
            try:
                title_page_title = soup.find('span', text = 'Title:').parent.decode_contents().replace('Title:','').strip().encode('ISO-8859-1').decode('utf-8')
                if '<i>' in title_page_title or '<b>' in title_page_title:
                    print(html_doc.stem,title_page_title)  
            except:
                pass