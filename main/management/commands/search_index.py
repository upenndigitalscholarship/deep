import srsly
from pathlib import Path
from lunr import lunr
from tqdm import tqdm
from main.models import * 
from django.core.management.base import BaseCommand

# Generate search index for use by lunr.js https://lunr.readthedocs.io/en/latest/lunrjs-interop.html

def item_to_dict(item:Item):
    item = item.__dict__ 
    
    edition = Edition.objects.get(id=item['edition_id'])
    edition = edition.__dict__
    del edition['id']

    title = Title.objects.get(id=edition['title_id'])
    title = title.__dict__

    return item | edition | title
    

class Command(BaseCommand):
    help = 'Generates a Lunr index for the site'
    
    def handle(self, *args, **options):
        items = [item_to_dict(item) for item in tqdm(Item.objects.all())]

        idx = lunr(ref="id", fields=['record_type', 'collection', 'year', 'deep_id_display', 'greg_full', 'stc', 'format', 'leaves', 'company_attribution', 'company_id', 'composition_date', 'date_first_publication', 'book_edition', 'play_edition', 'play_type', 'blackletter', 'deep_id', 'title', 'greg', 'genre', 'date_first_publication_display', 'date_first_performance', 'company_first_performance', 'total_editions', 'stationers_register', 'british_drama', 'genre_wiggins'], documents=items)
        serialized_idx = idx.serialize()
        index_path = Path.cwd() / 'main' / 'assets' / 'lunr' 
        if not index_path.exists():
            index_path.mkdir(parents=True, exist_ok=True)
        srsly.write_json(index_path / 'search.json', serialized_idx)

        self.stdout.write(self.style.SUCCESS('Search index created'))