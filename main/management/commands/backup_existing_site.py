import srsly
from tqdm import tqdm 
from pathlib import Path
from django.core.management.base import BaseCommand
import requests

pages_dir = Path.cwd() / 'backup'
if not pages_dir.exists():
    pages_dir.mkdir(parents=True, exist_ok=True)

class Command(BaseCommand):
    help = 'Request pages for old site and save to disk as html'
    
    def handle(self, *args, **options):
        item_data = srsly.read_json(Path.cwd() / 'main/assets/data/item_data.json')
        for key, item in tqdm(item_data.items()):
            if not (pages_dir / (item['deep_id'] + '.html')).exists():
                url = f"http://deep.sas.upenn.edu/{item['deep_id']}"
                resp = requests.get(url)
                (pages_dir / (item['deep_id'] + '.html')).write_bytes(resp.content)

        print("Done.")
        
        
            
            