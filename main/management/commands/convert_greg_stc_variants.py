import requests
import srsly
from django.core.management.base import BaseCommand
from tqdm import tqdm
from main.models import Item


class Command(BaseCommand):
    help = "Change the variants that end in Greg to DEEP #"
    
    def handle(self, *args, **options):
        for item in tqdm(Item.objects.all()): 
            if item.variants[-4:] == 'Greg':
                item.variants = item.variants[:-4] + "DEEP #"
                item.save() 
