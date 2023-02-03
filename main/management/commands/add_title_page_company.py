from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np


def create_title_page_company(company:str):
    results = []
    if company:
        if ';' in company:
            for split in company.split(';'):
                company_obj, created = Company.objects.get_or_create(name=split.strip())
                results.append(company_obj)
        else: 
            company_obj, created = Company.objects.get_or_create(name=company.strip()) 
            results.append(company_obj)
    return results

class Command(BaseCommand):
    help = 'Load company_first_performance data from old database. Comes from the old Company/CompanyDeep tables'
    
    def handle(self, *args, **options):
        tsv_file = Path('backup/title_page_company.tsv').read_text()
        data = {}
        for row in tsv_file.split('\n'):
            company, deep_id = row.split('\t')
            if data.get(deep_id,None):
                data[deep_id].append(company)
            else:
                data[deep_id] = []
                data[deep_id].append(company)
        for key in data.keys():
            
            item = Item.objects.get(deep_id=key)
            #print('; '.join(data[key]), item)
            item.title_page_company_display = '; '.join(data[key])                
            item.save() 

        #TODO this is not working, I have no idea why.
        for key in data.keys():
            item = Item.objects.get(deep_id=key)
            if item:
                title_page_company = create_title_page_company(';'.join(data[key]))
                for company in title_page_company:
                    item.title_page_company_filter.add(company) 
                item.save() 
            

            
        