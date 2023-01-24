from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load date_first_publication data from old database'
    
    def handle(self, *args, **options):
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/date_first_publication.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, date_first_publication, date_first_publication_display = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id]["display"].append(date_first_publication_display)
                data[deep_id]["filter"].append(date_first_publication)
            else:
                data[deep_id] = {"filter":[],"display":[]}
                data[deep_id]["display"].append(date_first_publication_display)
                data[deep_id]["filter"].append(date_first_publication)

        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                title = item.edition.title
                #print('; '.join(data[key]), item)
                if len(set(data[key]["display"])) == 1:
                    title.date_first_publication_display = data[key]["display"][0]
                    title.date_first_publication = ';'.join(data[key]["filter"])
                    #print(data[key]["display"][0], ';'.join(data[key]["filter"]))
                    title.save() 
                else:
                   print(key, len(set(data[key]["display"])))
            except Exception as e:
                print(key, e)
            
        