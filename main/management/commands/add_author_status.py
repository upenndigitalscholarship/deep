from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load Author_attribution data from old database'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/author_status_filter.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            status, deep_id = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id].append(status)
            else:
                data[deep_id] = []
                data[deep_id].append(status)
        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                #print('; '.join(data[key]), item)
                item.author_status = ';'.join(data[key])
                item.save() 
            except Exception as e:
                print(key, e)


            
        