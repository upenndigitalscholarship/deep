from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load Genreharbage data from old database'
    
    def handle(self, *args, **options):
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/genre_title_page.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, genre_title_page_filter = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id].append(genre_title_page_filter)
                
            else:
                data[deep_id] = []
                data[deep_id].append(genre_title_page_filter)

        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                
                if len(set(data[key])) == 1:
                    item.title_page_genre = data[key][0]
                    
                    item.save() 
                else:
                    item.title_page_genre = '; '.join(data[key])
            except Exception as e:
                print(key, e)
            
        