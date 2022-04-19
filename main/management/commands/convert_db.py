from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from main.models import *

def company_first_performance(id:int):
    
    company_deep = CompanyDeep.objects.filter(deep_id=id, ordering=0).first()
    if company_deep: 
        company = Company.objects.get(pk=company_deep.company_id) 
        return company.name

def stationers_register(id:int):
    
    stationer_deep = SrstationerDeep.objects.filter(deep_id=id).first()
    if stationer_deep: 
        stationer = Srstationer.objects.get(pk=stationer_deep.srstationer_id) 
        return stationer.name

class Command(BaseCommand):
    help = 'Load existing DB convert to json'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)
    deeps = Deep.objects.all() 
    new_deeps = []
    for deep in deeps: 
        new_deep = {}

        # Title fields
        new_deep['deep_id'] = deep.deep_id
        new_deep['deep_id_display'] = deep.deep_id_display.to_eng_string() if deep.deep_id_display else None 
        new_deep['greg_brief'] = deep.greg_brief
        new_deep['genre'] = deep.display_genre
        new_deep['date_first_publication'] = deep.first_publish_date
        #new_deep['date_first_publication_display'] = deep.first_publish_date_display
        new_deep['company_first_performance'] = company_first_performance(deep.deep_id)
        new_deep['total_editions'] = deep.total_editions
        new_deep['stationers_register'] = stationers_register(deep.deep_id)
        #new_deep['british_drama'] = ''
        #new_deep['genre_wiggins'] = 
        print(new_deep)

    

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Database Converted'))