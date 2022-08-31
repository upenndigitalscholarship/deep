import srsly
from bs4 import BeautifulSoup
from tqdm import tqdm 
from pathlib import Path
from django.core.management.base import BaseCommand
import requests

backup_dir = Path.cwd() / 'backup'
site_dir = Path.cwd() / 'site'

class Command(BaseCommand):
    help = 'Confirm that data in new item pages is identical to previous site (files in backup)'
    
    def handle(self, *args, **options):
        
        for old_html in tqdm(backup_dir.glob('*.html')):
            new_html = site_dir / old_html.name
            old_soup = BeautifulSoup(old_html.read_bytes(), 'html.parser')
            new_soup = BeautifulSoup(new_html.read_bytes(), 'html.parser')
            
            old_year = old_soup.find("td", {"class": "resultsyear"}).getText()
            new_year = new_soup.find("h4", {"id": "year"}).getText()
            assert old_year == new_year, f'[*] Error in year, old: {old_year}, new: {new_year}'

            old_title = old_soup.find("td", {"class": "playname"}).getText()
            new_title = new_soup.find("h4", {"id": "title"}).getText()
            assert old_title == new_title, f'[*] Error in title, old: {old_title}, new: {new_title}'

            old_author = old_soup.find("td", {"class": "authorname"}).getText()
            new_author = new_soup.find("h4", {"id": "authors"}).getText()
            assert old_author == new_author, f'[*] Error in author, old: {old_author}, new: {new_author}'

            old_deep_id = old_soup.find('span', text = 'DEEP #:').parent.get_text().replace('DEEP #:','').strip()
            new_deep_id = new_soup.find("span", {"id": "deep_id"}).getText()
            assert old_deep_id == new_deep_id, f'[*] Error in deep_id, old: {old_deep_id}, new: {new_deep_id}'

            old_in_collection = old_soup.find('span', text = 'In Collection:')
            if old_in_collection:
                link = old_soup.find('span', text = 'In Collection:').parent.find('a')
                Old_in_collection_text = link.get_text() 
                Old_in_collection_href = link['href'].replace("javascript:showRecord('",'').replace("')", '')
                #<span id="in_collection"> <a href="5022.html">1 & 2 The Troublesome Reign of King John</a></span>
                new_in_collection = new_soup.find("span", {"id": "in_collection"})
                if new_in_collection:
                    print(new_in_collection)
                    new_in_collection_text = new_in_collection.find('a').get_text()
                    new_in_collection_href = new_in_collection.find('a').href
                else:
                    print(f'[*] Error {old_deep_id}, "in collection present on old site, but not new')
                assert Old_in_collection_text == new_in_collection_text, f'[*] Error in collection, old: {Old_in_collection_text}, new: {new_in_collection_text}'
                assert Old_in_collection_href == new_in_collection_href, f'[*] Error in collection, old: {Old_in_collection_href}, new: {new_in_collection_href}'
