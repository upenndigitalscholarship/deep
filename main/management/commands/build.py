import time
from distutils.dir_util import copy_tree
from pathlib import Path

import srsly
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max, Min
from django.template.loader import render_to_string
from tqdm import tqdm

from main.management.commands.search_index import item_to_dict
from main.models import Edition, Item, Person, Title


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
        # 43 For this search, place "Anonymous" at the top, with a blank line after, and then the alphabetized list of names
        authors = [] 
        for author in Person.objects.all().order_by('name'):
            if not '(?)' in author.__str__().strip():
                authors.append({
                    'value': author.id,
                    'label': author.__str__().strip()
                })
        anonymous_index = next((index for (index, d) in enumerate(authors) if d["label"] == "Anonymous"), None)
        authors.insert(0, authors.pop(anonymous_index))
        authors.insert(1, {"value":0,"label":"---" })
        srsly.write_json(static_dir / 'data/authors.json', authors)
        
        # Author Title-Page Attribution
        title_page_author_filter = [a[0] for a in Item.objects.values_list('title_page_author_filter').distinct() if a[0]]
        title_page_author = []
        for t in title_page_author_filter:
             if ';' in t:
                 for s in t.split(';'):
                     if s not in title_page_author:
                         title_page_author.append(s.strip())
        title_page_author.sort()
        title_page_author = list(set(title_page_author))
        title_page_author_choices = []
        for i, author in enumerate(title_page_author):
            title_page_author_choices.append({"value":i, "label":author})
        title_page_author_choices.insert(0, {"value":0,"label":"Any" })
        title_page_author_choices.insert(1, {"value":0,"label":"None" })
        title_page_author_choices.insert(2, {"value":0,"label":"---" })
        srsly.write_json(static_dir / 'data/title_page_author_filter.json', title_page_author_choices)
        ## Companies
        db_companies = [] 
        for item in Item.objects.all().order_by('edition__title'):
            if item and item.company.name and item.company.name not in db_companies:
                db_companies.append(item.company.name)
        companies = []
        for i, company in enumerate(db_companies):
            companies.append({
                'value': i,
                'label': company.strip()
            })
        srsly.write_json(static_dir / 'data/companies.json', companies)

        # Genre BritDrama 
        genre_BritDrama = [a[0] for a in Title.objects.values_list('genre_brit_filter').distinct() if a[0]]
        genres = []
        for g in genre_BritDrama:
            if ';' in g:
                for l in g.split(';'):
                    genres.append(l.strip())
            else:
                genres.append(g)
        genres = list(set(genres))
        genres.sort()
        genre_out = []
        for i, genre in enumerate(genres):
            genre_out.append({
                'value': i,
                'label': genre.title().strip()
            })
        srsly.write_json(static_dir / 'data/genres_bd.json', genre_out)
        
        #Genre Playbook  --- Genre (Title-Page Attribution)
        genre_BritDrama = [a[0] for a in Item.objects.values_list('title_page_genre').distinct() if a[0]]
        genres = []
        for g in genre_BritDrama:
            if ';' in g:
                for l in g.split(';'):
                    genres.append(l.strip())
            else:
                genres.append(g)
        genres = list(set(genres))
        genres.sort()
        genre_out = []
        for i, genre in enumerate(genres):
            genre_out.append({
                'value': i,
                'label': genre.strip()
            })
        genre_out.insert(0, {"value":0,"label":"Any" })
        genre_out.insert(1, {"value":0,"label":"None" })
        genre_out.insert(2, {"value":0,"label":"---" })
        srsly.write_json(static_dir / 'data/genre_playbook.json', genre_out)
        
        # Author status 
        # It is not clear where this data comes from, so I am manually 
        # replacing author_status.json with values from the current site
        db_author_status = [] 
        for item in Item.objects.all().order_by('edition__title'):
            if item and item.author_status and item.author_status not in db_author_status:
                db_author_status.append(item.author_status)
        author_status_filter = []
        for g in db_author_status:
            if ';' in g:
                for l in g.split(';'):
                    author_status_filter.append(l.strip())
            else:
                author_status_filter.append(g)
        author_status_filter = list(set(author_status_filter))
        author_status_filter.sort()

        author_statuses = []
        for i, auth_stat in enumerate(author_status_filter):
            author_statuses.append({
                'value': i,
                'label': auth_stat.strip()
            })
        author_statuses.insert(0, {"value":0,"label":"Any" })
        author_statuses.insert(1, {"value":0,"label":"None" })
        author_statuses.insert(2, {"value":0,"label":"---" })

        srsly.write_json(static_dir / 'data/author_status.json', author_statuses)

        ## Company First Performance Annals
        # very few records have a company of first performance, to limit the list to just companies that 
        # appear a company of first performance in the data, this field needs its own set of valid choices
        first_companies = [company[0] for company in Title.objects.order_by('title').values_list('company_first_performance_annals_filter').distinct() if company[0] is not None and company[0] != 'n/a' or 'Unknown' ]
        first_companies = list(set(first_companies)) #also sorts alphabetically, who knew!?
        first_companies_distinct = []
        for g in first_companies:
            if not g:
                g = "None"
            if ';' in g:
                for l in g.split(';'):
                    first_companies_distinct.append(l.strip())
            else:
                first_companies_distinct.append(g)
        first_companies_distinct = list(set(first_companies_distinct))
        first_companies_distinct.sort()
        first_companies_json = []
        for i, company in enumerate(first_companies_distinct):
            if not company == 'None':
                first_companies_json.append({
                    'value': i,
                    'label': company.strip()
                })
        first_companies_json.insert(0, {"value":0,"label":"Any" })
        first_companies_json.insert(1, {"value":0,"label":"None" })
        first_companies_json.insert(2, {"value":0,"label":"---" })
        srsly.write_json(static_dir / 'data/first-companies.json', first_companies_json)

        ## Company First Performance British Drama
        first_companies = [company[0] for company in Title.objects.order_by('title').values_list('company_first_performance_brit_filter').distinct() if company[0] is not None and company[0] != 'n/a' or 'Unknown' ]
        first_companies = list(set(first_companies)) #also sorts alphabetically, who knew!?
        first_companies_distinct = []
        for g in first_companies:
            if not g:
                g = "None"
            if ';' in g:
                for l in g.split(';'):
                    first_companies_distinct.append(l.strip())
            else:
                first_companies_distinct.append(g)
        first_companies_distinct = list(set(first_companies_distinct))
        first_companies_distinct.sort()
        first_companies_json = []
        for i, company in enumerate(first_companies_distinct):
            if not company == 'None':
                first_companies_json.append({
                    'value': i,
                    'label': company.strip()
                })
        first_companies_json.insert(0, {"value":0,"label":"Any" })
        first_companies_json.insert(1, {"value":0,"label":"None" })
        first_companies_json.insert(2, {"value":0,"label":"---" })
        srsly.write_json(static_dir / 'data/first-companies-brit.json', first_companies_json)

        ## Play Type Filter
        playtypes = []
        playquery = Edition.objects.values_list('play_type_filter')
        for p in playquery:
            if p[0] and ';' in p[0]:
                for t in p[0].split(';'):
                    if t not in playtypes:
                        playtypes.append(t)
            else:
                if p[0] and p[0] not in playtypes:
                    playtypes.append(p[0])
        playtypes.remove('Professional')
        playtypes.remove('Nonprofessional')
        playtypes.sort()
        playtypes_json = []
        for i, pt in enumerate(playtypes):
            playtypes_json.append({"value":i, "label":pt})
        playtypes_json.insert(0, {"value":0,"label":"Professional" })
        playtypes_json.insert(1, {"value":1,"label":"Nonprofessional" })
        playtypes_json.insert(2, {"value":2,"label":"---" })
        srsly.write_json(static_dir / 'data/playtype.json', playtypes_json)
        
        ## Genre (Annals)
        # Temp disable to match old site's terms
        # genres = []
        # genre_query = list(set([t.genre_annals_filter for t in Title.objects.all().order_by('title')]))
        # genre_query.sort()

        # for i, g in enumerate(genre_query):
        #     genres.append({"value":i, "label":g})
        # srsly.write_json(static_dir / 'data/genre.json', genres)

        ## Theaters 
        # Changed to manual given client requirements
        # theater_json = []
        # theater_types = list(set([item.theater_type for item in Item.objects.all()]))
        # theater_types.sort()
        # count = 0
        # for i, t in enumerate(theater_types):
        #     if t != "" and t != "None":
        #         theater_json.append({"value":i, "label":t})
        #         count += 1 
        
        # theaters = list(set([item.theater for item in Item.objects.all()]))
        
        # theater_parts = []
        # for t in theaters:
        #     if ';' in t:
        #         for s in t.split(';'):
        #             if s not in theater_parts:
        #                 theater_parts.append(s)
        # theaters = theater_parts + theater_types
        # theaters.remove('')

        # theaters.sort()
        
        # for i, t in enumerate(theaters):
        #     if t != "":
        #         theater_json.append({"value":i, "label":t})
        #         count += 1
        # srsly.write_json(static_dir / 'data/theater.json', theater_json)

        ## Formats
        formats = list(set([i.format for i in Item.objects.all() if i.format]))
        formats.sort()
        formats_json = []
        for i, form in enumerate(formats):
            formats_json.append({
                'value': i,
                'label': form.strip()
            })
        srsly.write_json(static_dir / 'data/formats.json', formats_json)

        #Blackletter 
        #Removed dynamic generation of values, given that yes and no are only requested options.

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
            page_path = (out_path / f'{item.deep_id}')
            if not page_path.exists():
                page_path.mkdir(parents=True, exist_ok=True)

            (page_path / 'index.html').write_text(page)     

        about = render_to_string('about.html')
        (out_path / 'about.html').write_text(about)     

        download = render_to_string('download.html')
        (out_path / 'download.html').write_text(download)  
        
        sources = render_to_string('sources.html')
        (out_path / 'sources.html').write_text(sources)  
        
        browse = render_to_string('browse.html')
        (out_path / 'browse.html').write_text(browse)    
        end = time.time()
        self.stdout.write(self.style.SUCCESS(f'Build Complete in {end-start:.2f} seconds'))
