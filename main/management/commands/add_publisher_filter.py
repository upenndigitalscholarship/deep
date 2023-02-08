from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
from rich import print

class Command(BaseCommand):
    help = 'Load Publisher data from old database'
    
    def handle(self, *args, **options):
        print("[chartreuse2] 🐹 Adding Publisher Data from Old DB 🐹 [/chartreuse2]")
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/publisher.tsv').read_text()
        for row in tqdm(tsv_file.split('\n')):
            deep_id, publisher = row.split('\t')
            stationer_publisher, created = Person.objects.get_or_create(name=publisher.strip())
            item = Item.objects.get(deep_id=deep_id)
            item.stationer_publisher.add(stationer_publisher)
            item.save()
        print("[gray] 🐺 Finished 🐺 [/gray]")