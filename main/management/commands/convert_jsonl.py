from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from main.models import *
from tqdm import tqdm
import srsly 

authors_json_file = srsly.read_json('main/assets/data/authors.json')
authors_json = {}
for author in authors_json_file['results']:
    authors_json[author['id']] = author['text']

def get_authors(item:dict):
    authors = []
    if item.get('authors', None): 
        for i in item['authors']:
            name = authors_json[i]
            if name:
                person, created = Person.objects.get_or_create(name=name)
                authors.append(person)

    else: 
        names = item.get('authors_display', None)
        if names:
            names = names.split(';')
            for name in names:
                person, created = Person.objects.get_or_create(name=name)
                authors.append(person)
    return authors

class Command(BaseCommand):
    help = 'Load jsonl file to Django models'

    def add_arguments(self, parser):
        parser.add_argument('jsonl_path', nargs='+', type=str)

    def handle(self, *args, **options):
        data = srsly.read_jsonl(options['jsonl_path'][0])
        self.stdout.write(self.style.SUCCESS(f'Loaded jsonl file'))

        # Create Title objects
        for item in tqdm(data): 
            # Title fields
            title, created = Title.objects.get_or_create(
                deep_id=item['id'],
                title = item['title'],
                greg = item['greg_brief'],
                genre = item['genre'],
                date_first_publication = item['date_first_publication'],
                date_first_publication_display = item['date_first_publication_display'],
                company_first_performance = item['company_first_performance'],
                total_editions = item['total_editions'],
            )
            #if created:
            #    self.stdout.write(self.style.SUCCESS(f'Added new Title: {title.title}'))
    
            # Create Edition objects
            if title:
                edition, created = Edition.objects.get_or_create(
                    title = title,
                    greg_middle = item['greg_middle'],
                    book_edition = item['book_edition'], 
                    play_edition = item['play_edition'],
                    play_type = item['play_type'],
                    blackletter = item['blackletter'],
                )
                #if created:
                #    self.stdout.write(self.style.SUCCESS(f'Added new Edition: {edition.title}'))
                
                if edition:
                    authors = get_authors(item)
                    edition.authors.add(*authors)
                    edition.save()
                
                    # Create Item object
                    item, created = Item.objects.get_or_create(
                        edition = edition,
                        year = item['year_display'],
                        date_first_publication = item['date_first_publication'],
                        record_type=item['record_type'],
                        collection = item['collection_full'],
                        deep_id_display = item['deep_id_display'],
                        greg_full = item['greg_full'],
                        stc = item['stc'],
                        format = item['format'],
                        leaves = item['leaves'],
                        composition_date = item['composition_date_display'],
                        company_attribution = item['company_attribution'],
                        title_page_title = item["title_page_title"],
                        title_page_author = item["title_page_author"],
                        title_page_performance = item["title_page_performance"],
                        title_page_latin_motto = item["title-page_latin_motto"],
                        title_page_imprint = item["title_page_imprint"],
                        title_page_illustration = item["title_page_illustration"],
                        title_page_explicit = item["title_page_explicit"],
                        title_page_colophon = item["title_page_colophon"],
                        paratext_errata = item["paratext_errata"],
                        paratext_commendatory_verses = item["paratext_commendatory_verses"],
                        paratext_to_the_reader = item["paratext_to_the_reader"],
                        paratext_dedication = item["paratext_dedication"], 
                        paratext_argument = item["paratext_argument"],
                        paratext_actor_list = item["paratext_actor_list"],
                        paratext_charachter_list = item["paratext_charachter_list"],
                        paratext_other_paratexts = item["paratext_other_paratexts"],
                        stationer_printer = item["stationer_printer"],
                        stationer_publisher = item["stationer_publisher"],
                        stationer_bookseller = item["stationer_bookseller"],
                        stationer_entries_in_register = item["stationer_entries_in_register"],
                        stationer_additional_notes = item["stationer_additional_notes"],

                    )
                    item.company, _ = Company.objects.get_or_create(name=item.company_attribution)
                    item.save()
