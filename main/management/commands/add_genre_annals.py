from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load Genreharbage data from old database'
    
    def handle(self, *args, **options):
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/genre_annals.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, genre_annals_filter, genre_annals_display = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id]["display"].append(genre_annals_display)
                data[deep_id]["filter"].append(genre_annals_filter)
            else:
                data[deep_id] = {"filter":[],"display":[]}
                data[deep_id]["display"].append(genre_annals_display)
                data[deep_id]["filter"].append(genre_annals_filter)

        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                title = item.edition.title
                #print('; '.join(data[key]), item)
                if len(set(data[key]["display"])) == 1:
                    title.genre_annals_display = data[key]["display"][0]
                    title.genre_annals_filter = ';'.join(data[key]["filter"])
                    #print(data[key]["display"][0], ';'.join(data[key]["filter"]))
                    title.save() 
                else:
                   print(key, len(set(data[key]["display"])))
            except Exception as e:
                print(key, e)
            
        