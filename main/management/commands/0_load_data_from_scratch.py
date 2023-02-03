from django.core.management import call_command
from django.core.management.base import BaseCommand
import srsly
class Command(BaseCommand):
    help = 'Rebuild the database from scratch'
    
    def handle(self, *args, **options):
        call_command('convert_web_jsonl') # Read the jsonl file exported from the old database and scraped from the website
        self.stdout.write(self.style.SUCCESS('convert_web_jsonl'))
        # The "add" commands were created as each field of the migration/scrape 
        # was evaluated. In many cases, data was not presented to the user, but is present 
        # in the SQL db through a join and needed to be added. In other cases, formatting 
        # from the db was lost in the scrape and re-added. 
        # The end result is a balance between the data in the old database, the 
        # presentation of that data by the old application (represented in the scraped pages), 
        # and user feedback. 
        call_command('add_additional_notes')
        self.stdout.write(self.style.SUCCESS('add_additional_notes'))
        call_command('add_author_status')
        self.stdout.write(self.style.SUCCESS('add_author_status'))
        call_command('add_bookseller_filter')
        self.stdout.write(self.style.SUCCESS('add_bookseller_filter'))
        call_command('add_britdrama')
        self.stdout.write(self.style.SUCCESS('add_britdrama'))
        call_command('add_company_first_performance_annals')
        self.stdout.write(self.style.SUCCESS('add_company_first_performance_annals'))
        call_command('add_title_page_company')
        self.stdout.write(self.style.SUCCESS('add_title_page_company'))
        call_command('add_date_first_performance')
        self.stdout.write(self.style.SUCCESS('add_date_first_performance'))
        call_command('add_date_first_publication')
        self.stdout.write(self.style.SUCCESS('add_date_first_publication'))
        call_command('add_genre_annals')
        self.stdout.write(self.style.SUCCESS('add_genre_annals'))
        call_command('add_genre_title_page')
        self.stdout.write(self.style.SUCCESS('add_genre_title_page'))
        call_command('add_has_title_latin')
        self.stdout.write(self.style.SUCCESS('add_has_title_latin'))
        call_command('add_imprint_location')
        self.stdout.write(self.style.SUCCESS('add_imprint_location'))
        call_command('add_playtype')
        self.stdout.write(self.style.SUCCESS('add_playtype'))
        call_command('add_previous_sr_entry_date')
        self.stdout.write(self.style.SUCCESS('add_previous_sr_entry_date'))
        call_command('add_printer_filter')
        self.stdout.write(self.style.SUCCESS('add_printer_filter'))
        call_command('add_publisher_filter')
        self.stdout.write(self.style.SUCCESS('add_publisher_filter'))
        call_command('add_title_page_author_filter')
        self.stdout.write(self.style.SUCCESS('add_title_page_author_filter'))
        call_command('add_variant_description')
        self.stdout.write(self.style.SUCCESS('add_variant_description'))
        call_command('readd_formatting_from_db')
        self.stdout.write(self.style.SUCCESS('readd_formatting_from_db'))
        call_command('add_date_first_performance_filter')
        self.stdout.write(self.style.SUCCESS('add_date_first_performance_filter'))
        # re-add sites
        call_command('loaddata','backup/sites.json')
        self.stdout.write(self.style.SUCCESS('loaddata sites'))
        # re-add pages 
        call_command('loaddata','backup/flatpages.json')
        self.stdout.write(self.style.SUCCESS('loaddata flatpages'))
        
        call_command('build')
        data = srsly.read_json('main/assets/data/item_data.json')
        data = list(data)
        self.stdout.write(self.style.SUCCESS('build complete'))
