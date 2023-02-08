from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
from rich import print

class Command(BaseCommand):
    help = 'Load bookseller data from old database'
    
    def handle(self, *args, **options):
        print("[chartreuse2] 🦆 Adding Bookseller Data from Old DB 🦆 [/chartreuse2]")
         #f"{deep_id}\t{genre_annals_filter}\t{genre_annals_display}\n"
        tsv_file = Path('backup/bookseller.tsv').read_text()
        for row in tqdm(tsv_file.split('\n')):
            deep_id, bookseller = row.split('\t')
            stationer_bookseller, created = Person.objects.get_or_create(name=bookseller.strip())
            item = Item.objects.get(deep_id=deep_id)
            item.stationer_bookseller.add(stationer_bookseller)
            item.save()
        print("[gray] 🌷 Finished 🌷 [/gray]")        