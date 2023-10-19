from pathlib import Path
import csv
import srsly
from django.core.management.base import BaseCommand
from lunr import lunr
from tqdm import tqdm

from main.models import *

# Generate search index for use by lunr.js https://lunr.readthedocs.io/en/latest/lunrjs-interop.html

def item_to_dict(item:Item):
    edition = item.edition
    title = item.edition.title
    
    stationer_printer = '; '.join(list(item.stationer_printer.all().values_list('name', flat=True)))
    stationer_publisher = '; '.join(list(item.stationer_publisher.all().values_list('name', flat=True)))
    stationer_bookseller = '; '.join(list(item.stationer_bookseller.all().values_list('name', flat=True)))
    title_page_author_filter = ';'.join(list(item.edition.authors.all().values_list('name', flat=True)))

    title_page_company_filter = ';'.join(list(item.title_page_company_filter.all().values_list('name', flat=True)))
    company_first_performance_brit_filter = '; '.join(list(item.edition.title.company_first_performance_brit_filter.all().values_list('name', flat=True)))
    company_first_performance_annals_filter = '; '.join(list(item.edition.title.company_first_performance_annals_filter.all().values_list('name', flat=True)))

    item_dict = item.__dict__ 
    item_dict['title_page_author_filter'] = title_page_author_filter
    item_dict['title_page_company_filter'] = title_page_company_filter
    item_dict['stationer_printer_filter'] = stationer_printer
    item_dict['stationer_publisher_filter'] = stationer_publisher
    item_dict['stationer_bookseller_filter'] = stationer_bookseller
    

    #172, issue with paratext None
    if not item_dict.get('paratext_author',None):
        item_dict["paratext_author"] = ''
    if not item_dict.get('paratext_explicit',None):
        item_dict["paratext_explicit"] = ''
    if not item_dict.get('paratext_errata',None):
        item_dict["paratext_errata"] = ''
    if not item_dict.get('paratext_commendatory_verses',None):
        item_dict["paratext_commendatory_verses"] = ''
    if not item_dict.get('paratext_to_the_reader',None):
        item_dict["paratext_to_the_reader"] = ''       
    if not item_dict.get('paratext_dedication',None):
        item_dict["paratext_dedication"] = ''
    if not item_dict.get('paratext_argument',None):
        item_dict["paratext_argument"] = ''
    if not item_dict.get('paratext_actor_list',None):
        item_dict["paratext_actor_list"] = ''  
    if not item_dict.get('paratext_charachter_list',None):
        item_dict["paratext_charachter_list"] = ''
    if not item_dict.get('paratext_other_paratexts',None):
        item_dict["paratext_other_paratexts"] = ''
     
    if not item_dict.get('title_page_author_filter',None): # Replace none with 'None' (else search crashes)
        item_dict["title_page_author_filter"] = 'None'
    if not item_dict.get('author_status',None): # Replace none with 'None' (else search crashes)
        item_dict["author_status"] = 'None'
    if not item_dict.get('theater',None): 
        item_dict["theater"] = 'None'
    if not item_dict.get('theater_type',None): 
        item_dict["theater_type"] = 'None'
    if not item_dict.get('title_page_genre',None): 
        item_dict["title_page_genre"] = 'None'
    if not item_dict.get('title_page_modern_spelling',None): 
        item_dict["title_page_modern_spelling"] = ''
    if not item_dict.get('title_page_latin_motto',None): 
        item_dict["title_page_latin_motto"] = ''
    if not item_dict.get('title_page_illustration',None): 
        item_dict["title_page_illustration"] = ""
    if not item_dict.get('title_page_author',None): 
        item_dict["title_page_author"] = 'None'
    if not item_dict.get("title_page_performance",None):
        item_dict["title_page_performance"] = ""
    if not item_dict.get('title_page_has_latin',None): 
        item_dict["title_page_has_latin"] = 'No'
    if not item_dict.get('title_page_company_display', None):
        item_dict['title_page_company_display'] = "n/a"
    if not item_dict.get('date_first_performance_brit_display', None):
        item_dict['date_first_performance_brit_display'] = "n/a"
    # genre_annals_display
    if not item_dict.get('genre_annals_display', None):
        item_dict['genre_annals_display'] = "not in Annals"
    # brit_drama_number
    if not item_dict.get('brit_drama_number', None):
        item_dict['brit_drama_number'] = "not in BritDrama"
    # if not item_dict.get('stationer_publisher_filter',None): 
    #     item_dict["stationer_publisher_filter"] = 'None'
    # if not item_dict.get('stationer_printer_filter',None): 
    #     item_dict["stationer_printer_filter"] = 'None'
    if not item_dict.get('stationer_imprint_location',None): 
        item_dict["stationer_imprint_location"] = 'None'
    # if not item_dict.get('stationer_bookseller_filter',None): 
    #     item_dict["stationer_bookseller_filter"] = 'None'
    item_dict['variant_link'] = ''
    for i, link in enumerate(item.variant_links.all().order_by('deep_id')):
        if i == len(item.variant_links.all())-1:
            item_dict['variant_link'] += f'<a target="_blank" href="../{link.deep_id}">{link.deep_id}</a> '
        else:
            item_dict['variant_link'] += f'<a target="_blank" href="../{link.deep_id}">{link.deep_id}</a>; '

    if item.in_collection:
        item_dict["in_collection"] = f'<a target="_blank" href="../{item.in_collection.deep_id}">{item.in_collection.title}</a>'
    else: 
        item_dict["in_collection"] = ""
    

    item_dict['collection_contains'] = ''
    if item.collection_contains and item.record_type == "Collection": #m2m
        for i, link in enumerate(item.collection_contains.all().order_by('deep_id')):
            if i == len(item.collection_contains.all())-1:
                item_dict['collection_contains'] += f'<a target="_blank" href="../{link.deep_id}">{link.title}</a> '
            else:
                item_dict['collection_contains'] += f'<a target="_blank" href="../{link.deep_id}">{link.title}</a>; '
    if item.independent_playbook_link:
        item_dict["independent_playbook_link_id"] = item.independent_playbook_link.deep_id
    
    if item.also_in_collection:
        item_dict["also_in_collection_link"] = f'<a target="_blank" href="../{item.also_in_collection_link.deep_id}">{item.also_in_collection}</a>'
    
    if '_state' in item_dict.keys():
        del item_dict['_state']    
    
    
    edition_authors = list(edition.authors.all().values_list('id', flat=True))
    authors_display = ''.join(list(edition.authors.all().values_list('name', flat=True)))
    edition = edition.__dict__
    edition['author_id'] = edition_authors
    edition['author'] = authors_display
    #{'', None, 'Yes', 'Yes, Partly'}    
    if edition["blackletter"] == "":
        edition["blackletter"] = "No"
    if edition["blackletter"] == None:
        edition["blackletter"] = "No"
    
        
    if edition['book_edition'] == '0':
        edition['book_edition'] = 'n/a'
    if edition['play_edition'] == '0':
        edition['play_edition'] = 'n/a'

    del edition['id']
    if '_state' in edition.keys():
        del edition['_state']    
    if not edition.get('play_type_filter',None): # Replace none with 'None' (else search crashes)
        edition["play_type_filter"] = 'None'
    if not edition.get('play_type_display',None): # Replace none with 'None' (else search crashes)
        edition["play_type_display"] = 'None'

    
    title = title.__dict__
    title["company_first_performance_brit_filter"] = company_first_performance_brit_filter
    title["company_first_performance_annals_filter"] = company_first_performance_annals_filter
    
    if not title.get('company_first_performance_annals_display',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_annals_display"] = 'n/a'
    if not title.get('company_first_performance_annals_filter',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_annals_filter"] = 'None'
    if not title.get('brit_drama_number',None): # Replace none with 'None' (else search crashes)
        title["brit_drama_number"] = 'None'
    if not title.get('genre_annals_filter',None): # Replace none with 'None' (else search crashes)
        title["genre_annals_filter"] = 'not in Annals'        
    if not title.get('company_first_performance_brit_filter',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_brit_filter"] = 'None'
    if not title.get('company_first_performance_brit_display',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_brit_display"] = 'n/a'
    if not title.get('genre_brit_filter',None): # Replace none with 'None' (else search crashes)
        title["genre_brit_filter"] = 'not in BritDrama'
    if not title.get('genre_brit_display',None): # Replace none with 'None' (else search crashes)
        title["genre_brit_display"] = 'not in BritDrama'
    if not title.get('title_alternative_keywords', None):
        title['title_alternative_keywords'] = ""
    title['title_id'] = edition['title_id']
    if '_state' in title.keys():
        del title['_state']    
    

    joined =  item_dict | edition | title
    return joined



class Command(BaseCommand):
    help = 'Generates a item_data for the site'
    
    def handle(self, *args, **options):
        items = [item_to_dict(item) for item in tqdm(Item.objects.all())]
        item_data = {}
        for item in items: 
            item_data[item['deep_id']] = item
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
