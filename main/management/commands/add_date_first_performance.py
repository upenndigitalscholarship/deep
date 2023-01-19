from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np
import srsly 

class Command(BaseCommand):
    help = 'Load title.date_first_performance from web data'
    
    def handle(self, *args, **options):
        web_data = srsly.read_jsonl('web_item_data.jsonl')
        for item in web_data:
            deep = Item.objects.get(deep_id=item['deep_id'])
            title = deep.edition.title
            title.date_first_performance = item['date_first_performance']
            title.save()
            #print(item['deep_id'], item['date_first_performance'])
