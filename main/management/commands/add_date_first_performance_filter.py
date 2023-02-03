from django.core.management.base import BaseCommand
from tqdm import tqdm
from main.models import *


class Command(BaseCommand):
    help = 'Load date_first_performance_filter data from new database'
    
    def handle(self, *args, **options):
        titles = Title.objects.all() 
        for title in tqdm(titles, total=len(titles)): 
            year = title.date_first_performance[:4]
            if 'n/a' not in year and 'c' not in year:
                title.date_first_performance_filter = year
                title.save()
            if 'c' in year:
                title.date_first_performance_filter = title.date_first_performance[2:6]
                title.save()
            if 'n/a' in year:
                title.date_first_performance_filter = None
                title.save()
            
            

            
