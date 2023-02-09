from django.core.management.base import BaseCommand
from pathlib import Path
from tqdm import tqdm
from main.models import *
from rich import print

class Command(BaseCommand):
    help = 'Load stationer_printer data from old database'
    
    def handle(self, *args, **options):
        print("[chartreuse2] 🐸 Adding Printer Data from Old DB 🐸 [/chartreuse2]")
        tsv_file = Path('backup/printer.tsv').read_text()
        for row in tqdm(tsv_file.split('\n')):
            deep_id, printer = row.split('\t')
            stationer_printer, created = Person.objects.get_or_create(name=printer.strip())
            item = Item.objects.get(deep_id=deep_id)
            item.stationer_printer.add(stationer_printer)
            item.save()
        print("[green] 🦩 Finished 🦩 [/green]")
            