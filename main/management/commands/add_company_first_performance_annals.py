from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

def create_company_first_performance(companies:str):
    results = []
    if companies:
        if ';' in companies:
            for split in companies.split(';'):
                company, created = Company.objects.get_or_create(name=split.strip())
                results.append(company)
        else: 
            company, created = Company.objects.get_or_create(name=companies.strip()) 
            results.append(company)
    return results

class Command(BaseCommand):
    help = 'Load company_first_performance data from old database'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/company_first_performance_annals.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            deep_id, company = row.split('\t')
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
                company_first_performance = create_company_first_performance(';'.join(data[key]))
                title.company_first_performance_annals_filter.add(*company_first_performance)
                title.save() 
            except Exception as e:
                print(key, e)


            
        