import time 
from django.core.management.base import BaseCommand
from django.core.management import call_command
from netlify_py import NetlifyPy
from deep.secrets import NETLIFY_KEY, NETLIFY_SITE_ID
class Command(BaseCommand):
    help = 'Push site to Netlify'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        start = time.time()
        # build Lunr search index files
        call_command('search_index')
        call_command('build')

        n = NetlifyPy(access_token=NETLIFY_KEY)
        n.deploys.deploy_site(NETLIFY_SITE_ID,"site")
        
        end = time.time()
        self.stdout.write(self.style.SUCCESS(f'Deploy Complete in {end-start:.2f} seconds'))