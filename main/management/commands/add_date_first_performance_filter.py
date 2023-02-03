from django.core.management.base import BaseCommand
from tqdm import tqdm
from main.models import *


class Command(BaseCommand):
    help = 'Load date_first_performance_filter data from new database'
    
    def handle(self, *args, **options):
        items = Item.obects.all() 
        for item in items: 
            year = item.edition.title.date_first_performance[:4]
            if year != 'n/a' or 'c' not in year:
                item.edition.title.date_first_performance_filter = year
                item.save()
            if 'c' in year:
                item.edition.title.date_first_performance_filter = item.edition.title.date_first_performance[2:6]
                item.save()
            
            

            