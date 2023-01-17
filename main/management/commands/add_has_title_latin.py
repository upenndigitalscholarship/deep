from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load Has Latin'
    
    def handle(self, *args, **options):
        txt_file = Path('backup/has_latin_title.txt').read_text()
        data = {}
        for deep_id in txt_file.split('\n'):
            item = Item.objects.get(deep_id=deep_id)
            item.title_page_has_latin = 'Yes'
            item.save() 
            
            
        