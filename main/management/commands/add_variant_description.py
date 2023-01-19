from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
import numpy as np

class Command(BaseCommand):
    help = 'Load Has variant_description'
    
    def handle(self, *args, **options):
        txt_file = Path('backup/variant_description.tsv').read_text()
        for line in txt_file.split('\n'):
            deep_id, variant_description = line.split('\t')
            item = Item.objects.get(deep_id=deep_id)
            item.variants = variant_description
            item.save() 
            
            
        
