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
        new_deep['date_first_publication_display'] = deep.first_publish_date_display
        new_deep['company_first_performance'] = company_first_performance(deep.deep_id)
        new_deep['total_editions'] = deep.total_editions
        new_deep['stationers_register'] = stationers_register(deep.deep_id)
        #new_deep['british_drama'] = ''
        #new_deep['genre_wiggins'] = 
        print(new_deep)

    # nid = models.IntegerField(blank=True, null=True)
    # deep_id_display_old = models.CharField(max_length=32, blank=True, null=True)
    # deep_id_display = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    # deep_id_revised = models.CharField(max_length=8, blank=True, null=True)
    # deep_id_notused = models.IntegerField(blank=True, null=True)
    # title = models.CharField(max_length=225)
    # year = models.PositiveIntegerField(blank=True, null=True)
    # year_display = models.CharField(max_length=32)
    # composition_date = models.PositiveIntegerField(blank=True, null=True)
    # composition_date_display = models.CharField(max_length=255)
    # first_publish_date = models.PositiveIntegerField(blank=True, null=True)
    # first_publish_date_display = models.CharField(max_length=255)
    # record_type_id = models.IntegerField()
    # theater_type_id = models.IntegerField()
    # greg_full = models.CharField(max_length=128)
    # greg_brief = models.CharField(max_length=32)
    # greg_middle = models.CharField(max_length=32)
    # greg_word = models.CharField(max_length=150)
    # not_in_greg = models.IntegerField()
    # stc_or_wing = models.CharField(max_length=100)
    # stc_or_wing2 = models.CharField(max_length=100, blank=True, null=True)
    # collection_brief = models.CharField(max_length=32, blank=True, null=True)
    # collection_middle = models.CharField(max_length=32, blank=True, null=True)
    # collection_full = models.CharField(max_length=128, blank=True, null=True)
    # collection_word = models.CharField(max_length=150, blank=True, null=True)
    # play_edition_number = models.IntegerField()
    # book_edition_number = models.IntegerField(blank=True, null=True)
    # variant_description = models.TextField()
    # edition = models.CharField(max_length=32)
    # total_editions = models.TextField()
    # sheets_delete = models.CharField(max_length=32)
    # sheets = models.CharField(max_length=32)
    # collation = models.CharField(max_length=100, blank=True, null=True)
    # dedication_to = models.TextField()
    # commendatory_verses_by = models.TextField()
    # to_the_reader = models.CharField(max_length=255)
    # argument = models.CharField(max_length=255)
    # char_list = models.CharField(max_length=255)
    # actor_list = models.CharField(max_length=255)
    # illustrationontporfrontis = models.TextField()
    # blackletter = models.CharField(max_length=255)
    # latin = models.CharField(max_length=255)
    # addition_and_correction_attributions = models.CharField(max_length=255)
    # other_paratexts = models.TextField(blank=True, null=True)
    # previous_sr_entry_date = models.TextField()
    # additional_notes = models.TextField()
    # transcript_title = models.TextField()
    # transcript_author = models.TextField()
    # transcript_performance = models.TextField()
    # transcript_latin = models.TextField()
    # transcript_imprint = models.TextField()
    # transcript_explicit = models.TextField()
    # transcript_colophon = models.TextField()
    # transcript_dedication = models.TextField()
    # transcript_commendatory_verses = models.TextField()
    # transcript_to_the_reader = models.TextField()
    # transcript_printed_license = models.TextField()
    # transcript_general_title = models.TextField()
    # transcript_woodcut = models.TextField()
    # transcript_woodcut_frontispiece = models.TextField()
    # transcript_engraved_title = models.TextField()
    # transcript_engraved_portrait = models.TextField()
    # transcript_engraved_frontispiece = models.TextField()
    # biandic = models.IntegerField(db_column='BIandIC', blank=True, null=True)  # Field name made lowercase.
    # transcript_character_list = models.TextField(blank=True, null=True)
    # transcript_actor_list = models.TextField(blank=True, null=True)
    # transcript_argument = models.TextField(blank=True, null=True)
    # transcript_modern_spelling = models.TextField()
    # transcript_old_spelling = models.TextField()
    # display_play_type = models.CharField(max_length=200, blank=True, null=True)
    # format = models.CharField(max_length=100, blank=True, null=True)
    # display_authors = models.CharField(max_length=200, blank=True, null=True)
    # display_genre = models.CharField(max_length=200, blank=True, null=True)
    # display_booksellers = models.CharField(max_length=200, blank=True, null=True)
    # display_printers = models.CharField(max_length=200, blank=True, null=True)
    # display_publishers = models.CharField(max_length=200, blank=True, null=True)
    # display_companies = models.CharField(max_length=200, blank=True, null=True)
    # display_auspices = models.CharField(max_length=200, blank=True, null=True)
    # title_alternative_keywords = models.TextField(blank=True, null=True)
    # errata = models.CharField(max_length=200, blank=True, null=True)
    #        print(serializers.serialize('json', [deep]))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Database Converted'))