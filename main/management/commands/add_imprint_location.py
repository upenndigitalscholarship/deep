from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load company_first_performance data from old database'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/imprint_location.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, imprint_location = row.split('\t')
            #print('[*] id:',deep_id,'[filter]', play_type_filter,'[display]',play_type_display)
            if data.get(deep_id,None):
                data[deep_id].append(imprint_location)
                
            else:
                data[deep_id] = []
                data[deep_id].append(imprint_location)
        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                
                #print('; '.join(data[key]), item)
                if len(set(data[key])) == 1:
                    item.stationer_imprint_location = data[key][0]
                    item.save() 
                else:
                    item.stationer_imprint_location = '; '.join(data[key])
            except Exception as e:
                print(key, e)
