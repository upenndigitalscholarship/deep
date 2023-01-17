from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load stationer_printer_filter data from old database'
    
    def handle(self, *args, **options):
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/bookseller.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, bookseller = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id].append(bookseller)
            else:
                data[deep_id] = []
                data[deep_id].append(bookseller)

        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                #print('; '.join(data[key]), item)
                if len(data[key]) == 1:
                    item.stationer_bookseller_filter = data[key][0]
                    item.save() 
                else:
                    item.stationer_bookseller_filter = ';'.join(data[key])
                    item.save() 
            except Exception as e:
                print(key, e)
            
        