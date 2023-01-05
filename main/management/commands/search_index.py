from pathlib import Path
import csv
import srsly
from django.core.management.base import BaseCommand
from lunr import lunr
from tqdm import tqdm

from main.models import *

# Generate search index for use by lunr.js https://lunr.readthedocs.io/en/latest/lunrjs-interop.html

def item_to_dict(item:Item):
    item_dict = item.__dict__ 
    
    if not item_dict.get('title_page_author_filter',None): # Replace none with 'None' (else search crashes)
        item_dict["title_page_author_filter"] = 'None'
    if not item_dict.get('author_status',None): # Replace none with 'None' (else search crashes)
        item_dict["author_status"] = 'None'
    
    
    item_dict['variant_link'] = ''
    for link in item.variant_links.all():
        item_dict['variant_link'] += f'<a target="_blank" href="{link.deep_id}.html">{link.greg_full}</a> '
    if item.in_collection:
        item_dict["in_collection"] = f'<a target="_blank" href="{item.in_collection.deep_id}.html">{item.in_collection.title}</a>'
    else: 
        item_dict["in_collection"] = ""
    

    item_dict['collection_contains'] = ''
    if item.collection_contains and item.record_type == "Collection": #m2m
        for i, link in enumerate(item.collection_contains.all()):
            if i == len(item.collection_contains.all())-1:
                item_dict['collection_contains'] += f'<a target="_blank" href="{link.deep_id}.html">{link.title}</a> '
            else:
                item_dict['collection_contains'] += f'<a target="_blank" href="{link.deep_id}.html">{link.title}</a>; '
    if item.independent_playbook_link:
        item_dict["independent_playbook_link_id"] = item.independent_playbook_link.deep_id
    
    if item.also_in_collection:
        item_dict["also_in_collection_link"] = f'<a target="_blank" href="{item.also_in_collection_link.deep_id}.html">{item.also_in_collection}</a>'
    
    if '_state' in item_dict.keys():
        del item_dict['_state']    
    
    edition = Edition.objects.get(id=item_dict['edition_id'])
    edition_authors = list(edition.authors.all().values_list('id', flat=True))
    authors_display = ''.join(list(edition.authors.all().values_list('name', flat=True)))
    play_type = ''.join(list(edition.play_type.all().values_list('name', flat=True)))
    edition = edition.__dict__
    edition['author_id'] = edition_authors
    edition['author'] = authors_display
    edition['play_type'] = play_type
    if edition["blackletter"] == "":
        edition["blackletter"] = "No"
    else:
        edition["blackletter"] = "Yes" 
        
    del edition['id']
    if '_state' in edition.keys():
        del edition['_state']    

    title = Title.objects.get(id=edition['title_id'])
    title = title.__dict__
    if not title.get('company_first_performance_annals_display',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_annals_display"] = 'None'
    if not title.get('company_first_performance_annals_filter',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_annals_filter"] = 'None'
    title['title_id'] = edition['title_id']
    if '_state' in title.keys():
        del title['_state']    
    

    joined =  item_dict | edition | title
    joined['lunr_id'] = item_dict['id']
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
        # Write data to csv 
        data_file = open('main/assets/data/DEEP_data.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        count = 0
        for key_ in item_data.keys():
            if count == 0:
                header = item_data[key_].keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(item_data[key_].values())
        
        data_file.close()
        self.stdout.write(self.style.SUCCESS('Wrote data to CSV'))