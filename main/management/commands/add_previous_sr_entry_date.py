from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load previous_sr_entry_date data from old database'
    
    def handle(self, *args, **options):
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/previous_sr_entry_date.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            
            deep_id, previous_sr_entry_date = row.split('\t')
            
            if data.get(deep_id,None):
                data[deep_id].append(previous_sr_entry_date)
            else:
                data[deep_id] = []
                data[deep_id].append(previous_sr_entry_date)

        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
               
                #print('; '.join(data[key]), item)
                if len(set(data[key])) == 1:
                    item.stationer_entries_in_register = data[key][0]
                    
                    #print(data[key]["display"][0], ';'.join(data[key]["filter"]))
                    item.save() 
                else:
                   item.stationer_entries_in_register = '; '.join(data[key])
                   item.save()
            except Exception as e:
                print(key, e)
            
        