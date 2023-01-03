from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load Author_attribution data from old database'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/author_attribution_filter.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, greg, stc, author_name, title = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id].append(author_name)
            else:
                data[deep_id] = []
                data[deep_id].append(author_name)
        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                item.title_page_author_filter = '; '.join(data[key])
                item.save() 
            except Exception as e:
                print(key, e)


            
        