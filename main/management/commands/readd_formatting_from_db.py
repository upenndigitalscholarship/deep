from django.core.management import call_command
from django.core.management.base import BaseCommand
from main.models import Item, Edition, Title 
import srsly 

class Command(BaseCommand):
    help = '# For 18 fields that contain formatting, but have lost it during make_items_from_html, re-add the formatting from deeps.jsonl'
    
    def handle(self, *args, **options):
        deeps = srsly.read_jsonl('main/assets/data/deeps.jsonl')
        for deep in deeps:
            item = Item.objects.get(deep_id=deep["id"])
            if item:
                if deep.get('title_page_title',None):
                    item.title_page_title = deep['title_page_title']
                    item.save()
                if deep.get('title_page_author',None):
                    item.title_page_author = deep['title_page_author']
                    item.save()
                if deep.get('title_page_performance',None):
                    item.title_page_performance = deep['title_page_performance']
                    item.save()
                if deep.get('title-page_latin_motto',None):
                    item.title_page_latin_motto = deep['title-page_latin_motto']
                    item.save()
                if deep.get('title_page_imprint',None):
                    item.title_page_imprint = deep['title_page_imprint']
                    item.save()
                if deep.get('title_page_illustration',None):
                    item.title_page_illustration = deep['title_page_illustration']
                    item.save()
                if deep.get('title_page_explicit',None):
                    item.paratext_explicit = deep['title_page_explicit']
                    item.save()
                if deep.get('title_page_colophon',None):
                    item.stationer_colophon = deep['title_page_colophon']
                    item.save()
                if deep.get('paratext_commendatory_verses',None):
                    item.paratext_commendatory_verses = deep['paratext_commendatory_verses']
                    item.save()
                if deep.get('paratext_to_the_reader',None):
                    item.paratext_to_the_reader = deep['paratext_to_the_reader']
                    item.save()
                if deep.get('paratext_dedication',None):
                    item.paratext_dedication = deep['paratext_dedication']
                    item.save()
                if deep.get('paratext_argument',None):
                    item.paratext_argument = deep['paratext_argument']
                    item.save()
                if deep.get('paratext_actor_list',None):
                    item.paratext_actor_list = deep['paratext_actor_list']
                    item.save()
                if deep.get('paratext_charachter_list',None):
                    item.paratext_charachter_list = deep['paratext_charachter_list']
                    item.save()
                if deep.get('transcript_printed_license',None):
                    item.stationer_license = deep['transcript_printed_license']
                    item.save()

        # new_deep['transcript_modern_spelling'] = deep.transcript_modern_spelling
        # new_deep['transcript_engraved_frontispiece'] = deep.transcript_engraved_frontispiece
        # new_deep['transcript_engraved_title'] = deep.transcript_engraved_title
        #Imprint location is also a thing! ImprintlocationDeep and Imprintlocation in old-db