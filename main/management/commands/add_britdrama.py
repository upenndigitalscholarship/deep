import pandas as pd 
from django.core.management.base import BaseCommand
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
    help = 'Request pages for old site and save to disk as html'
    
    def handle(self, *args, **options):
        df = pd.read_csv('./backup/DEEP--BritDrama.csv')
        df1 = df.where(pd.notnull(df), None)
        # 0 Greg # Item.greg_full
        # 1 Greg (sort)
        # 2 BritDrama # Item
        # 3 Unnamed: 3
        # 4 Diplay Genre (BritDrama) Title
        # 5 Genre (BritDrama): filter terms Title
        # 6 Unnamed: 6
        # 7 Date of First Performance (BritDrama) (sort) Title
        # 8 Date of First Performance (BritDrama) (display) Title
        # 9 Unnamed: 9
        # 10 Company of First Performance (BritDrama) (display) Title
        # 11 Company of First Performance (BritDrama): filter terms Title

        for i, row in tqdm(df1.iterrows()):
            greg_num = row[0] if row[0] else ''
            greg_sort = row[1] if row[1] else ''
            brit_drama_number = row[2] if row[2] else ''
            genre_brit_display = row[4] if row[4] else ''
            genre_brit_filter= row[5] if row[5] else ''
            date_first_performance_brit_filter= row[7] if row[7] else ''
            date_first_performance_brit_display= row[8] if row[8] else ''
            company_first_performance_brit_filter= row[11] if row[11] else ''
            company_first_performance_brit_display= row[10] if row[10] else ''

            titles = Title.objects.filter(greg=greg_num)
            for title in titles:
                title.brit_drama_number = brit_drama_number
                title.genre_brit_display = genre_brit_display
                title.genre_brit_filter = genre_brit_filter
                title.date_first_performance_brit_filter = date_first_performance_brit_filter
                title.date_first_performance_brit_display = date_first_performance_brit_display
                company_first_performance = create_company_first_performance(company_first_performance_brit_filter)
                title.company_first_performance_brit_filter.add(*company_first_performance)
                title.company_first_performance_brit_display = company_first_performance_brit_display
                title.save()
                
        print("Done.")
        
