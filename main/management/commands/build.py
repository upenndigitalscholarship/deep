import time
from distutils.dir_util import copy_tree
from pathlib import Path
import itertools
import srsly
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max, Min
from django.template.loader import render_to_string
from django.contrib.flatpages.models import FlatPage
from tqdm import tqdm
from django.core.management import call_command
import re
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
        author_set = []
        for edition in Edition.objects.all():
            for author in edition.authors.all():
                if author.name not in author_set:
                    if not '(?)' in author.__str__().strip():
                        authors.append({
                            'value': author.id,
                            'label': author.name.__str__().strip()
                        })
                        author_set.append(author.name)
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
        
        title_page_author = list(set(title_page_author))
        title_page_author.sort()
        title_page_author_choices = []
        for i, author in enumerate(title_page_author):
            title_page_author_choices.append({"value":i, "label":author})
        title_page_author_choices.insert(0, {"value":0,"label":"Any" })
        title_page_author_choices.insert(1, {"value":0,"label":"None" })
        title_page_author_choices.insert(2, {"value":0,"label":"---" })
        srsly.write_json(static_dir / 'data/title_page_author_filter.json', title_page_author_choices)
        
        ## Company (Title-Page Attribution) 
        db_companies = [] 
        for item in Item.objects.all():
            for company in item.title_page_company_filter.all():
                if company.name not in db_companies:
                    db_companies.append(company.name)
        db_companies.sort()
        companies = []
        for i, company in enumerate(db_companies):
            companies.append({
                'value': i,
                'label': company.strip()
            })
        srsly.write_json(static_dir / 'data/title-page-companies.json', companies)

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
        db_companies = [] 
        for item in Item.objects.all():
            for company in item.edition.title.company_first_performance_annals_filter.all():
                if company.name not in db_companies:
                    db_companies.append(company.name)
        db_companies.sort()
        companies = []
        for i, company in enumerate(db_companies):
            companies.append({
                'value': i,
                'label': company.strip()
            })
        srsly.write_json(static_dir / 'data/first-companies.json', companies)
        
        
        ## Company First Performance British Drama
        db_companies = [] 
        for item in Item.objects.all():
            for company in item.edition.title.company_first_performance_brit_filter.all():
                if company.name not in db_companies:
                    db_companies.append(company.name)
        db_companies.sort()
        companies = []
        for i, company in enumerate(db_companies):
            companies.append({
                'value': i,
                'label': company.strip()
            })
        srsly.write_json(static_dir / 'data/first-companies-brit.json', companies)
        
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

        #Printer
        
        printers_query = [';'.join(list(item.stationer_printer.all().values_list('name', flat=True))) for item in Item.objects.all() if item.stationer_printer]
        printers = []
        for p in printers_query:
            if ';' in p:
                for p_ in p.split(';'):
                    printers.append(p_)
            else:
                printers.append(p)
        printers = list(set(printers))
        printers = [p.replace('(?)','') for p in printers]
        printers.sort()
        printers_json = []
        for i, form in enumerate(printers):
            if form != "":
                printers_json.append({
                    'value': i,
                    'label': form.strip()
                })
        srsly.write_json(static_dir / 'data/printer.json', printers_json)

        #Publisher
        publisher_query = [';'.join(list(item.stationer_publisher.all().values_list('name', flat=True))) for item in Item.objects.all() if item.stationer_publisher]
        publishers = []
        for p in publisher_query:
            if ';' in p:
                for p_ in p.split(';'):
                    publishers.append(p_)
            else:
                publishers.append(p)
        publishers = list(set(publishers))
        publishers = [p.replace('(?)','') for p in publishers]
        publishers.sort()
        publishers_json = []
        for i, form in enumerate(publishers):
            if form != "":
                publishers_json.append({
                    'value': i,
                    'label': form.strip()
                })
        srsly.write_json(static_dir / 'data/publisher.json', publishers_json)

        #Bookseller
        
        bookseller_query = [';'.join(list(item.stationer_bookseller.all().values_list('name', flat=True))) for item in Item.objects.all() if item.stationer_bookseller]
        booksellers = []
        for p in bookseller_query:
            if ';' in p:
                for p_ in p.split(';'):
                    booksellers.append(p_)
            else:
                booksellers.append(p)
        booksellers = list(set(booksellers))
        booksellers = [p.replace('(?)','') for p in booksellers]
        booksellers.sort()
        booksellers_json = []
        for i, form in enumerate(booksellers):
            if form != "":
                booksellers_json.append({
                    'value': i,
                    'label': form.strip()
                })
        srsly.write_json(static_dir / 'data/bookseller.json', booksellers_json)

        #Stationer
        stationers = printers + publishers + booksellers 
        stationers = list(set(stationers))
        stationers = [s.replace('(?)','') for s in stationers]
        stationers.sort()
        stationer_json = []
        for i, form in enumerate(stationers):
            if form:
                stationer_json.append({
                    'value': i,
                    'label': form.strip()
                })
        srsly.write_json(static_dir / 'data/stationer.json', stationer_json)
        
        #Imprint Location
        locations = [i.stationer_imprint_location for i in Item.objects.all() if i.stationer_imprint_location]
        # Split those with ; in them
        locations = [x for x in (b.split(';') for b in locations)]
        locations = list(itertools.chain(*locations))     
        locations = [x.strip() for x in locations]
        locations = list(set(locations))
        locations.sort()
        # https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            return [ atoi(c) for c in re.split(r'(\d+)', text) ]

        locations.sort(key=natural_keys)
        locations_json = []
        for i, form in enumerate(locations):
                locations_json.append({
                    'value': i,
                    'label': form.strip()
                })
        print(locations_json)
        srsly.write_json(static_dir / 'data/locations.json', locations_json)

        #Book Edition 
        editions = [int(i.book_edition) for i in Edition.objects.all() if i.book_edition != 'n/a']

        editions = list(set(editions))
        editions.sort()
        editions_json = []
        for i, form in enumerate(editions):
            if form != 1 and form != 0:
                editions_json.append({
                    'value': i,
                    'label': str(form)
                })
        editions_json.insert(0, {"value":0,"label":"First" })
        editions_json.insert(1, {"value":1,"label":"Second-plus" })
        editions_json.insert(2, {"value":2,"label":"---" })
        srsly.write_json(static_dir / 'data/book_editions.json', editions_json)
        
        #Play Edition 
        editions = [int(i.play_edition) for i in Edition.objects.all() if i.play_edition != 'n/a']

        editions = list(set(editions))
        editions.sort()
        editions_json = []
        for i, form in enumerate(editions):
            if form != 1 and form != 0:
                editions_json.append({
                    'value': i,
                    'label': str(form)
                })
        editions_json.insert(0, {"value":0,"label":"First" })
        editions_json.insert(1, {"value":1,"label":"Second-plus" })
        editions_json.insert(2, {"value":2,"label":"---" })
        srsly.write_json(static_dir / 'data/play_editions.json', editions_json)

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

        download_path = (out_path / "download")
        if not download_path.exists():
            download_path.mkdir(parents=True, exist_ok=True)
        download = render_to_string('download.html')
        (download_path / 'index.html').write_text(download)

        # Flatpages 
        for flat_page in FlatPage.objects.all():
            page = render_to_string('flatpages/default.html', {"flatpage":{"content": flat_page.content}})
            flat_page_path = (out_path / f"{flat_page.url.replace('/','')}")
            if not flat_page_path.exists():
                flat_page_path.mkdir(parents=True, exist_ok=True)
            (flat_page_path / 'index.html').write_text(page)
        end = time.time()
        self.stdout.write(self.style.SUCCESS(f'Build Complete in {end-start:.2f} seconds'))
        data = srsly.read_json('main/assets/data/item_data.json')
        call_command('collectstatic','--noinput')
        self.stdout.write(self.style.SUCCESS(f'{len(data)}'))
