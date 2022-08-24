import time 
import srsly 
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max, Min
from django.template.loader import render_to_string
from django.core.management import call_command
from main.models import Item, Person, PlayType, Title, Edition
from distutils.dir_util import copy_tree
from pathlib import Path
from tqdm import tqdm
from main.management.commands.search_index import item_to_dict

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

        #Authors 
        authors = [] 
        for author in Person.objects.all():
            if not '(?)' in author.__str__().strip():
                authors.append({
                    'value': author.id,
                    'label': author.__str__().strip()
                })
        srsly.write_json(static_dir / 'data/authors.json', authors)
        
        ## Companies
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

        # Author status 
        db_author_status = [] 
        for item in Item.objects.all():
            if item and item.author_status and item.author_status not in db_author_status:
                db_author_status.append(item.author_status)
        author_statuses = []
        for i, auth_stat in enumerate(db_author_status):
            author_statuses.append({
                'value': i,
                'label': auth_stat.strip()
            })
        srsly.write_json(static_dir / 'data/author_status.json', author_statuses)

        ## Company First Performance
        # very few records have a company of first performance, to limit the list to just companies that 
        # appear a company of first performance in the data, this field needs its own set of valid choices
        first_companies = [company[0] for company in Title.objects.values_list('company_first_performance').distinct() if company[0] is not None]
        first_companies_json = []
        for i, company in enumerate(first_companies):
            first_companies_json.append({
                'value': i,
                'label': company.strip()
            })
        srsly.write_json(static_dir / 'data/first-companies.json', first_companies_json)

        ## Play Types
        playtypes = []
        playquery = PlayType.objects.all().distinct()
        
        for i, pt in enumerate(playquery):
            if not '(?)' in pt.name:
                playtypes.append({"value":i, "label":pt.name})
        srsly.write_json(static_dir / 'data/playtype.json', playtypes)
        
        ## Genre 
        genres = []
        genre_query = set([t.genre for t in Title.objects.all()])
        
        for i, g in enumerate(genre_query):
            genres.append({"value":i, "label":g})
        srsly.write_json(static_dir / 'data/genre.json', genres)

        ## Theaters 
        theater_json = []
        theater_types = list(set([item.theater_type for item in Item.objects.all()]))
        theaters = list(set([item.theater for item in Item.objects.all()]))
        theaters = theater_types + theaters
        tts = []
        for t in theaters:
            if ";" in t:
                for tt in t.split(";"):
                    tts.append(tt)
            else:
                tts.append(t)
        theaters = set(tts)
        #TODO in progress, also theater type
        for i, t in enumerate(theaters):
            if t != "":
                theater_json.append({"value":i, "label":t})
        srsly.write_json(static_dir / 'data/theater.json', theater_json)

        ## Formats
        formats = set([i.format for i in Item.objects.all() if i.format])
        formats_json = []
        for i, form in enumerate(formats):
            formats_json.append({
                'value': i,
                'label': form.strip()
            })
        srsly.write_json(static_dir / 'data/formats.json', formats_json)

        #Blackletter 
        
        blackletters = set([i.blackletter for i in Edition.objects.all() if i.blackletter])
        bl_json = []
        for i, bl in enumerate(blackletters):
            bl_json.append({
                'value': i,
                'label': bl.strip()
            })
        srsly.write_json(static_dir / 'data/blackletter.json', bl_json)

        #copy all static files
        site_static = (out_path / 'assets')
        if not site_static.exists():
            site_static.mkdir(parents=True, exist_ok=True)
        copy_tree(static_dir, str(site_static))
        
        context = {}
        context['min_year'] = Item.objects.aggregate(Min('year_int'))['year_int__min']
        context['max_year'] = Item.objects.aggregate(Max('year_int'))['year_int__max']
        context['build'] = True
        index = render_to_string('index.html',context)
        (out_path / 'index.html').write_text(index)     

        # Item pages
        self.stdout.write(self.style.SUCCESS('Creating item pages'))
        for item in tqdm(Item.objects.all()):
            page = render_to_string('item_page.html', {"data":item_to_dict(item)})
            (out_path / f'{item.deep_id}.html').write_text(page)     

        about = render_to_string('about.html')
        (out_path / 'about.html').write_text(about)     

        browse = render_to_string('browse.html')
        (out_path / 'browse.html').write_text(browse)    
        end = time.time()
        self.stdout.write(self.style.SUCCESS(f'Build Complete in {end-start:.2f} seconds'))