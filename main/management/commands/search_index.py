import srsly
from pathlib import Path
from lunr import lunr
from tqdm import tqdm
from main.models import * 
from django.core.management.base import BaseCommand

# Generate search index for use by lunr.js https://lunr.readthedocs.io/en/latest/lunrjs-interop.html

def item_to_dict(item:Item):
    item = item.__dict__ 
    if '_state' in item.keys():
        del item['_state']    
    edition = Edition.objects.get(id=item['edition_id'])
    edition_authors = list(edition.authors.all().values_list('id', flat=True))
    authors_display = ''.join(list(edition.authors.all().values_list('name', flat=True)))
    play_type = ''.join(list(edition.play_type.all().values_list('name', flat=True)))
    edition = edition.__dict__
    edition['author_id'] = edition_authors
    edition['author'] = authors_display
    edition['play_type'] = play_type
    del edition['id']
    if '_state' in edition.keys():
        del edition['_state']    

    title = Title.objects.get(id=edition['title_id'])
    title = title.__dict__
    title['title_id'] = edition['title_id']
    if '_state' in title.keys():
        del title['_state']    
    

    joined =  item | edition | title
    joined['lunr_id'] = item['id']
    return joined

# {'id': 1,
#  'edition_id': 1,
#  'record_type': 'Single-Play Playbook',
#  'collection': None,
#  'year': '[1515?]',
#  'deep_id_display': '1.000',
#  'greg_full': '3a',
#  'stc': '14039',
#  'format': 'Quarto',
#  'leaves': '18',
#  'company_attribution': '',
#  'company_id': None,
#  'composition_date': '1513 [c.1513-1516]',
#  'date_first_publication': '[1515?]',
#  'title_id': 1,
#  'greg_middle': '3a',
#  'book_edition': '1',
#  'play_edition': '1',
#  'play_type': 'Interlude',
#  'blackletter': 'Yes',
#  'person_id': [1],
#  'deep_id': '1',
#  'title': 'Hycke Scorner',
#  'greg': '3',
#  'genre': 'Moral Interlude',
#  'date_first_publication_display': '[1515?]',
#  'date_first_performance': None,
#  'company_first_performance': None,
#  'total_editions': '3 quartos',
#  'stationers_register': None,
#  'british_drama': None,
#  'genre_wiggins': None,
#  'lunr_id': 1}


class Command(BaseCommand):
    help = 'Generates a Lunr index for the site'
    
    def handle(self, *args, **options):
        items = [item_to_dict(item) for item in tqdm(Item.objects.all())]
        item_data = {}
        for item in items: 
            item_data[item['id']] = item
        # create json item lookup for search results 
        srsly.write_json(Path('main/assets/data/item_data.json'), item_data)
        self.stdout.write(self.style.SUCCESS('Created item data'))

        idx = lunr(ref="lunr_id", fields=['id','title_id','record_type', 'author_id','collection', 'year', 'deep_id_display', 'greg_full', 'stc', 'format', 'leaves', 'company_attribution', 'company_id', 'composition_date', 'date_first_publication', 'book_edition', 'play_edition', 'play_type', 'blackletter', 'deep_id', 'title', 'title_alternative_keywords', 'greg', 'genre', 'date_first_publication_display', 'date_first_performance', 'company_first_performance', 'total_editions', 'stationers_register', 'british_drama', 'genre_wiggins', 'title_page_modern_spelling'], documents=items)
        serialized_idx = idx.serialize()
        index_path = Path.cwd() / 'main' / 'assets' / 'lunr' 
        if not index_path.exists():
            index_path.mkdir(parents=True, exist_ok=True)
        srsly.write_json(index_path / 'search.json', serialized_idx)

        self.stdout.write(self.style.SUCCESS('Search index created'))