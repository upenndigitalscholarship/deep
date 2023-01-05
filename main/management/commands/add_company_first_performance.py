from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load company_first_performance data from old database'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/company_first_performance.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            company, deep_id = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id].append(company)
            else:
                data[deep_id] = []
                data[deep_id].append(company)
        for key in data.keys():
            try:
                item = Item.objects.get(deep_id=key)
                title = item.edition.title
                #print('; '.join(data[key]), item)
                title.company_first_performance_annals_display = '; '.join(data[key])
                title.company_first_performance_annals_filter = ';'.join(data[key])
                title.save() 
            except Exception as e:
                print(key, e)


            
        