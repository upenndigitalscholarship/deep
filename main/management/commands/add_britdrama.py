import pandas as pd 
from django.core.management.base import BaseCommand
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Request pages for old site and save to disk as html'
    
    def handle(self, *args, **options):
        df = pd.read_csv('/home/apjanco/Downloads/DEEP--BritDrama.csv')
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
            greg_num = row[0] if row[0] != 'nan' else None
            greg_sort = row[1] if row[1] != 'nan' else None
            brit_drama_number = row[2] if row[2] != 'nan' else None
            genre_brit_display = row[4] if row[4] != 'nan' else None
            genre_brit_filter= row[5] if row[5] != 'nan' else None
            date_first_performance_brit_filter= row[7] if row[7] != 'nan' else None
            date_first_performance_brit_display= row[8] if row[8] != 'nan' else None
            company_first_performance_brit_filter= row[11] if row[11] != 'nan' else None
            company_first_performance_brit_display= row[10] if row[10] != 'nan' else None

            title = Title.objects.filter(greg=greg_num).first()
            if title:
                title.brit_drama_number = brit_drama_number
                title.genre_brit_display = genre_brit_display
                title.genre_brit_filter = genre_brit_filter
                title.date_first_performance_brit_filter = date_first_performance_brit_filter
                title.date_first_performance_brit_display = date_first_performance_brit_display
                title.company_first_performance_brit_filter = company_first_performance_brit_filter
                title.company_first_performance_brit_display = company_first_performance_brit_display
                title.save()
                
        print("Done.")
        
        