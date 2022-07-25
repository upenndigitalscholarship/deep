import time 
import srsly 
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.core.management import call_command
from main.models import Item, Person, PlayType
from distutils.dir_util import copy_tree
from pathlib import Path

class Command(BaseCommand):
    help = 'Builds a static version of the site'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        start = time.time()
        # build Lunr search index files
        call_command('search_index')

        
        out_path = Path('site')
        if not out_path.exists():
            out_path.mkdir(parents=True, exist_ok=True)

        

        
        static_dir = Path('main/assets')
        # create json data files 
        #       {
        #   "results": [
        #     {
        #       "id":0,
        #       "text":"The Jovial Crew, or The Devil Turned Ranter"
        #     },...]
        # }
        items = {} 
        items['results'] = []
        for item in Item.objects.all():
            items['results'].append({
                'id': item.id,
                'text': item.__str__()
            })
        srsly.write_json(static_dir / 'data/items.json', items)

        authors = [] 
        for author in Person.objects.all():
            if not '(?)' in author.__str__().strip():
                authors.append({
                    'value': author.id,
                    'label': author.__str__().strip()
                })
        srsly.write_json(static_dir / 'data/authors.json', authors)

        db_companies = [] 
        for item in Item.objects.all():
            if item and item.company.name and item.company.name not in db_companies:
                db_companies.append(item.company.name)
        companies = []
        for i, company in enumerate(db_companies):
            companies.append({
                'value': i,
                'label': company.strip()
            })
        srsly.write_json(static_dir / 'data/companies.json', companies)

        ## Play Types
        playtypes = []
        playquery = PlayType.objects.all().distinct()
        
        for i, pt in enumerate(playquery):
            if not '(?)' in pt.name:
                playtypes.append({"value":i, "label":pt.name})
        srsly.write_json(static_dir / 'data/playtypes.json', playtypes)
        
        #copy all static files
        site_static = (out_path / 'assets')
        if not site_static.exists():
            site_static.mkdir(parents=True, exist_ok=True)
        copy_tree(static_dir, str(site_static))
        
        index = render_to_string('index.html',{"build":True})
        (out_path / 'index.html').write_text(index)     

        about = render_to_string('about.html')
        (out_path / 'about.html').write_text(about)     

        browse = render_to_string('browse.html')
        (out_path / 'browse.html').write_text(browse)    
        end = time.time()
        self.stdout.write(self.style.SUCCESS(f'Build Complete in {end-start:.2f} seconds'))