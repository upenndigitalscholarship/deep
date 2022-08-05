from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from main.models import *
from tqdm import tqdm
import srsly 


def get_authors(item:dict):
    authors = []
    names = item.get('authors_display', None)
    if names:
        names = names.split(';')
        for name in names:
            person, created = Person.objects.get_or_create(name=name.strip())
            authors.append(person)
    return authors


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
                authors_display = item['authors_display'],
                title = item['title'],
                title_alternative_keywords = item['title_alternative_keywords'],
                greg = handle_greg(item['greg_brief']),
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
                    greg_middle = handle_greg(item['greg_middle']),
                    book_edition = item['book_edition'], 
                    play_edition = item['play_edition'],
                    blackletter = item['blackletter'],
                )
                #if created:
                #    self.stdout.write(self.style.SUCCESS(f'Added new Edition: {edition.title}'))
                
                if edition:
                    authors = get_authors(item)
                    edition.authors.add(*authors)
                    playtype = get_playtype(item)
                    edition.play_type.add(*playtype)
                    edition.save()
                
                    # Create Item object
                    item, created = Item.objects.get_or_create(
                        edition = edition,
                        year = item['year_display'],
                        year_int = item['year'],
                        date_first_publication = item['date_first_publication'],
                        record_type=django_is_worst(item['record_type']),
                        collection = item['collection_full'],
                        deep_id_display = item['deep_id_display'],
                        greg_full = handle_greg(item['greg_full']),
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
                        title_page_modern_spelling = item['transcript_modern_spelling'],
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
                        theater_type = item["theater_type"],
                        theater = item["theater"],

                    )
                    item.company, _ = Company.objects.get_or_create(name=item.company_attribution)
                    item.save()
