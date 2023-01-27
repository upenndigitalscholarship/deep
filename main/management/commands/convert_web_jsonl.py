import srsly
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm
from pathlib import Path
from main.models import *


def get_authors(item:dict):
    authors = []
    names = item.get('authors_display', None)
    if names:
        names = names.split(';')
        for name in names:
            person, created = Person.objects.get_or_create(name=name.strip())
            authors.append(person)
    return authors

def get_stationer_printer(item:dict):
    stationer_printer = []
    names = item.get('stationer_printer', None)
    if names:
        names = names.split(';')
        for name in names:
            person, created = Person.objects.get_or_create(name=name.strip())
            stationer_printer.append(person)
    return stationer_printer

def get_stationer_publisher(item:dict):
    stationer_publisher = []
    names = item.get('stationer_publisher', None)
    if names:
        names = names.split(';')
        for name in names:
            person, created = Person.objects.get_or_create(name=name.strip())
            stationer_publisher.append(person)
    return stationer_publisher

def get_stationer_bookseller(item:dict):
    stationer_bookseller = []
    names = item.get('stationer_bookseller', None)
    if names:
        names = names.split(';')
        for name in names:
            person, created = Person.objects.get_or_create(name=name.strip())
            stationer_bookseller.append(person)
    return stationer_bookseller

def get_collection_links(item:dict):
    links = []
    collection_links = item.get('collection_contains_links', None)
    if collection_links:
        for collection in collection_links:
            link = Link.objects.get(deep_id=collection["href"])
            links.append(link)
    return links

def get_variant_links(item:dict):
    links = []
    variant_links = item.get('variant_links', None)
    if variant_links:
        for variant in variant_links:
            try:
                link = Link.objects.get(deep_id=variant["href"])
                links.append(link)
            except Item.DoesNotExist:
                print('[*] Item does not exist: ',variant)
    return links


def get_playtype(item:dict):
    play_type = item.get('play_type', None)
    results = []
    if play_type:
        if ';' in play_type:
            for split in play_type.split(';'):
                playtype, created = PlayType.objects.get_or_create(name=split.strip())
                results.append(playtype)
        else: 
            playtype, created = PlayType.objects.get_or_create(name=play_type.strip()) 
            results.append(playtype)
    return results
    
def handle_greg(greg:str):
    if greg == "":
        return "C"
    else:
        return greg

def django_is_worst(record_type:str):
    if record_type == 'Collection':
        return Item.COLLECTION
    if record_type == 'Play in Collection':
        return Item.PLAYINCOLLECTION
    if record_type == 'Single-Play Playbook':
        return Item.SINGLEPLAY

def lookup(item_data, deep_id_display):
    
    result = next((item for item in item_data if str(item["id"]) == deep_id_display),None)
    if not result:
        print(f'[*] No item_data for {deep_id_display}')
    else:
        return result
        #return dict(printer="",publisher="",srstationer="",author_status="",authors_display="",title_alternative_keywords="",greg_brief="",greg_full="",date_first_publication="",greg_middle="",year_display="",year=0,collection_full="",composition_date_display="",transcript_modern_spelling="",theater_type="",theater="",collection_middle="",collection_brief="",variant_edition_id="",variant_newish_primary_deep_id="")

def remove_variant_link_text(item:dict):
    variants = item.get("variants", None)
    variant_links = item.get("variant_links", None)
    if variants and variant_links:
        index = variants.find('See also Greg')
        variants = variants[:index+13]
        return variants
    else:
        return item["variants"]      

class Command(BaseCommand):
    help = 'Load jsonl file to Django models'
    


    def handle(self, *args, **options):
        item_data = srsly.read_jsonl('main/assets/data/deeps.jsonl')
        item_data = list(item_data)
        
        #new_deep['id'] = deep.deep_id_revised
        
        for item in item_data: # This is because the old app re-formats the id, so the db and site don't match
            if '.000' in item["deep_id_display"]:
                item["deep_id_display"] = item["deep_id_display"].replace('.000','')
            if item["deep_id_display"][-2:] == '00':
                item["deep_id_display"] = item["deep_id_display"][:-2]
            elif item["deep_id_display"][-1:] == '0':
                item["deep_id_display"] = item["deep_id_display"][:-1]
        
        web_data = srsly.read_jsonl('web_item_data.jsonl')
        
        self.stdout.write(self.style.SUCCESS(f'Loaded jsonl files'))

        # Read Work-ID data, create Title and Edition objects
        work_ids = Path('backup/work_id_data.tsv').read_text()
        work_ids = work_ids.split('\n')
        for row in work_ids:
            if len(row.split('\t')) == 4:
                for deep_id, collection, greg_full, work_id in row.split('\t'):
                    try:
                        title = Title.objects.get(work_id=work_id)
                    except Title.DoesNotExist:
                        # use deep_id to fetch item data
                        db_item_data = lookup(item_data, deep_id)
                        title = Title.objects.create(
                                work_id=work_id,
                                title = db_item_data['title'],
                                title_alternative_keywords = db_item_data['title_alternative_keywords'],
                                greg = db_item_data['greg_brief'],
                                date_first_publication = db_item_data['date_first_publication'],
                                date_first_publication_display = db_item_data['date_first_publication_display'],
                                total_editions = db_item_data['total_editions'],
                            )
                            
        
        web_data = srsly.read_jsonl('web_item_data.jsonl')
        for item in tqdm(web_data):
            #There are three empty records to ignore
            if item["deep_id"] in ['47','48','1014']:
                continue 
            try:
                db_item_data = lookup(item_data, item["deep_id_display"]) 
            except KeyError:
                print('KeyError',item)
            
            if p_edition != 0:
                title = Title.objects.get(title = item['title'], edition__play_edition=db_item_data['play_edition']) 
            elif b_edition != 0:
                title = Title.objects.get(title = item['title'], edition__book_edition=db_item_data['book_edition'])   
            
            # Create Edition objects
            if title:
                if p_edition and p_edition != 0:
                    edition = Edition.objects.get(title = title, play_edition=db_item_data['play_edition'])    
                elif b_edition and b_edition != 0:
                    edition = Edition.objects.get(title = title, book_edition=db_item_data['book_edition'])  
                
                
                if edition:
                    authors = get_authors(db_item_data)
                    edition.authors.add(*authors)
                    #playtype = get_playtype(item)
                    #edition.play_type.add(*playtype)
                    edition.save()
                
                    # Create Item object
                    django_item, created = Item.objects.get_or_create(
                        edition = edition,
                        year = item['year'],
                        year_int = db_item_data['year'],
                        date_first_publication = item['date_first_publication_display'],
                        record_type=django_is_worst(item['record_type']),
                        collection = db_item_data['collection_full'],
                        deep_id = item['deep_id'],
                        greg_full = item['greg_full'], #The app transforms these, need to use web data
                        stc = item['stc'],
                        format = item['format'],
                        leaves = item['leaves'],
                        composition_date = db_item_data['composition_date_display'],
                        company_attribution = item['company_attribution'],
                        title_page_title = item["title_page_title"],
                        title_page_author = item["title_page_author"],
                        title_page_performance = item["title_page_performance"],
                        title_page_latin_motto = item["title_page_latin_motto"],
                        title_page_imprint = item["title_page_imprint"],
                        title_page_illustration = item["title_page_illustration"],
                        paratext_explicit = item["paratext_explicit"],
                        stationer_colophon = item["stationer_colophon"],
                        title_page_modern_spelling = db_item_data['transcript_modern_spelling'],
                        paratext_errata = item["paratext_errata"],
                        paratext_commendatory_verses = item["paratext_commendatory_verses"],
                        paratext_to_the_reader = item["paratext_to_the_reader"],
                        paratext_dedication = item["paratext_dedication"], 
                        paratext_argument = item["paratext_argument"],
                        paratext_actor_list = item["paratext_actor_list"],
                        paratext_charachter_list = item["paratext_charachter_list"],
                        paratext_other_paratexts = item["paratext_other_paratexts"],
                        stationer_entries_in_register = item["stationer_entries_in_register"],
                        stationer_additional_notes = item["stationer_additional_notes"],
                        theater_type = db_item_data["theater_type"],
                        theater = db_item_data["theater"],
                        collection_full= db_item_data['collection_full'],
                        collection_middle = db_item_data['collection_middle'],
                        collection_brief = db_item_data['collection_brief'],
                        variant_edition_id= db_item_data['variant_edition_id'],
                        variant_newish_primary_deep_id = db_item_data['variant_newish_primary_deep_id'],
                        author_status= db_item_data['author_status'],
                        srstationer = db_item_data['srstationer'],
                        publisher = db_item_data['publisher'],
                        printer = db_item_data['printer']
                    )
                    stationer_printer = get_stationer_printer(db_item_data)
                    django_item.stationer_printer.add(*stationer_printer)
                    
                    stationer_publisher = get_stationer_publisher(db_item_data)
                    django_item.stationer_publisher.add(*stationer_publisher)

                    stationer_bookseller = get_stationer_bookseller(db_item_data)
                    django_item.stationer_bookseller.add(*stationer_bookseller)
                    
                    django_item.company, _ = Company.objects.get_or_create(name=django_item.company_attribution)
                    django_item.save()

        
        self.stdout.write(self.style.SUCCESS('adding variants and collection links'))
        web_data = srsly.read_jsonl('web_item_data.jsonl')
        for item in tqdm(web_data):
            if item["deep_id"] in ["1014","47","48"]:
                continue
            else:
                django_item = Item.objects.get(deep_id=item["deep_id"])
                django_item.variants = remove_variant_link_text(item)
                variant_links = get_variant_links(item)
                django_item.variant_links.add(*variant_links)

                collection_links = get_collection_links(item)
                django_item.collection_contains.add(*collection_links)
                if item["in_collection"]:
                    django_item.in_collection = Link.objects.get(deep_id=item["in_collection_link_href"])
                
                if item["independent_playbook"]:
                    django_item.independent_playbook = item["independent_playbook"]
                    try:
                        django_item.independent_playbook_link = Link.objects.get(deep_id=item["independent_playbook_link_href"])
                    except Link.DoesNotExist:
                        print('broken link, ask how to handle', item["independent_playbook_link_href"])
                if item["also_in_collection"]:
                    django_item.also_in_collection = item["also_in_collection"]
                    django_item.also_in_collection_link = Link.objects.get(deep_id=item["also_in_collection_link_href"])
                django_item.stationer_bookseller_display = item['stationer_bookseller']
                django_item.stationer_publisher_display = item['stationer_publisher']
                django_item.stationer_printer_display = item['stationer_printer']
                
                django_item.save()
       

