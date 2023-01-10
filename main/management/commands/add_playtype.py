from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load company_first_performance data from old database'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/playtype.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, play_type_filter, play_type_display = row.split('\t')
            #print('[*] id:',deep_id,'[filter]', play_type_filter,'[display]',play_type_display)
            if data.get(deep_id,None):
                data[deep_id]["display"].append(play_type_display)
                data[deep_id]["filter"].append(play_type_filter)
            else:
                data[deep_id] = {"filter":[],"display":[]}
                data[deep_id]["display"].append(play_type_display)
                data[deep_id]["filter"].append(play_type_filter)
        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                edition = item.edition
                #print('; '.join(data[key]), item)
                if len(set(data[key]["display"])) == 1:
                    edition.play_type_display = data[key]["display"][0]
                    edition.play_type_filter = ';'.join(data[key]["filter"])
                    edition.save() 
                else:
                   print(key, len(set(data[key]["display"])))
            except Exception as e:
                print(key, e)
