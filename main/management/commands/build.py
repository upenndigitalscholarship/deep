import time 
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from main.models import Title
from distutils.dir_util import copy_tree
from pathlib import Path

class Command(BaseCommand):
    help = 'Builds a static version of the site'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        start_time = time.time()
        out_path = Path('site')
        if not out_path.exists():
            out_path.mkdir(parents=True, exist_ok=True)

        #copy all static files
        static_dir = Path('main/assets')

        site_static = (out_path / 'assets')
        if not site_static.exists():
            site_static.mkdir(parents=True, exist_ok=True)
        copy_tree(static_dir, str(site_static))
        
        index = render_to_string('index.html')
        (out_path / 'index.html').write_text(index)     

        about = render_to_string('about.html')
        (out_path / 'about.html').write_text(about)     

        self.stdout.write(self.style.SUCCESS('Build Complete'))