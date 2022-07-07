import srsly
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from main.models import *
from tqdm import tqdm
deep_fields = [
    'deep_id',
    'nid',
    'deep_id_display_old',
    'deep_id_display',
    'deep_id_revised',
    'deep_id_notused',
    'title',
    'year',
    'year_display',
    'composition_date',
    'composition_date_display',
    'first_publish_date',
    'first_publish_date_display',
    'record_type_id',
    'theater_type_id',
    'greg_full',
    'greg_brief',
    'greg_middle',
    'greg_word',
    'not_in_greg',
    'stc_or_wing',
    'stc_or_wing2',
    'collection_brief',
    'collection_middle',
    'collection_full',
    'collection_word',
    'play_edition_number',
    'book_edition_number',
    'variant_description',
    'edition',
    'total_editions',
    'sheets_delete',
    'sheets',
    'collation',
    'dedication_to',
    'commendatory_verses_by',
    'to_the_reader',
    'argument',
    'char_list',
    'actor_list',
    'illustrationontporfrontis',
    'blackletter',
    'latin',
    'addition_and_correction_attributions',
    'other_paratexts',
    'previous_sr_entry_date',
    'additional_notes',
    'transcript_title',
    'transcript_author',
    'transcript_performance',
    'transcript_latin',
    'transcript_imprint',
    'transcript_explicit',
    'transcript_colophon',
    'transcript_dedication',
    'transcript_commendatory_verses',
    'transcript_to_the_reader',
    'transcript_printed_license',
    'transcript_general_title',
    'transcript_woodcut',
    'transcript_woodcut_frontispiece',
    'transcript_engraved_title',
    'transcript_engraved_portrait',
    'transcript_engraved_frontispiece',
    'biandic',
    'transcript_character_list',
    'transcript_actor_list',
    'transcript_argument',
    'transcript_modern_spelling',
    'transcript_old_spelling',
    'display_play_type',
    'format',
    'display_authors',
    'display_genre',
    'display_booksellers',
    'display_printers',
    'display_publishers',
    'display_companies',
    'display_auspices',
    'title_alternative_keywords',
     'errata'
 ]


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

def get_authors(id:int):
    """Given a DEEP id, returns a sorted list of Author ids"""
    attributions_deep = AuthorAttributionDeep.objects.filter(deep_id=id)
    authors = []
    for a in attributions_deep: 
        attribution = AuthorAttribution.objects.get(pk=a.author_attribution_id)
        try:
            author = Author.objects.get(name=attribution.name)
            order = a.ordering
            authors.append((order, author.author_id))
        except Author.DoesNotExist:
            pass
    # Sort by order
    authors = sorted(authors, key = lambda x: x[0])
    return [a[1] for a in authors ]

def get_authors_from_display(deep:Deep):
    """ex 'Beaumont, Francis; Fletcher, John' """
    author_list = []
    authors = deep.display_authors
    if authors:
        if ";" in authors:
            authors = authors.split(';')
        else:
            authors = [authors]
        for author in authors:
            author = author.strip()
            
            a, created = Author.objects.get_or_create(name=author)
            if created:
                print(f'created record for {author}')
            author_list.append(a.author_id)
            
    return author_list 

def get_record_type(id:int):
    types = ['','Single-Play Playbook', 'Collection', 'Play in Collection']
    return types[id]

def get_stc_or_wing(deep): 
    if deep.stc_or_wing2 and deep.stc_or_wing2 != '':
        return f"{deep.stc_or_wing}; {deep.stc_or_wing2}"
    elif deep.stc_or_wing:
        return f"{deep.stc_or_wing}"
    else:
        return ""

def get_theater_type(id):
    lookup = {0:'', 1:"Indoor",2:"Outdoor",3:"Both Indoor and Outdoor",4:"None"}
    return lookup[id]

class Command(BaseCommand):
    help = 'Load existing DB convert to json'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)
    deeps = Deep.objects.all() 
    new_deeps = []
    for deep in tqdm(deeps): 
        new_deep = {}

        # Title fields
        new_deep['id'] = deep.deep_id_revised
        new_deep['deep_id'] = deep.deep_id
        new_deep['deep_id_display'] = deep.deep_id_display.to_eng_string() if deep.deep_id_display else None 
        new_deep['title'] = deep.title
        new_deep['greg_brief'] = deep.greg_brief
        new_deep['genre'] = deep.display_genre
        new_deep['date_first_publication'] = deep.first_publish_date
        new_deep['date_first_publication_display'] = deep.first_publish_date_display
        new_deep['company_first_performance'] = company_first_performance(deep.deep_id)
        new_deep['company_attribution'] = deep.display_auspices
        new_deep['total_editions'] = deep.total_editions
        new_deep['stationers_register'] = stationers_register(deep.deep_id)
        new_deep['variant_description'] = deep.variant_description
        #new_deep['british_drama'] = ''
        #new_deep['genre_wiggins'] = 

        # Edition fields
        new_deep['authors'] = get_authors_from_display(deep)
        new_deep['authors_display'] = deep.display_authors
        new_deep['greg_middle'] = deep.greg_middle
        new_deep['book_edition'] = deep.book_edition_number
        new_deep['play_edition'] = deep.play_edition_number
        new_deep['play_type'] = deep.display_play_type
        new_deep['blackletter'] = deep.blackletter

        # Item fields 
        new_deep["record_type"] = get_record_type(deep.record_type_id)
        new_deep['year'] = deep.year
        new_deep['year_display'] = deep.year_display
        new_deep['greg_full'] = deep.greg_full
        new_deep['greg_display'] = deep.greg_word
        new_deep['stc'] = get_stc_or_wing(deep)
        new_deep['format'] = deep.format
        new_deep['leaves'] = deep.sheets
        new_deep['company_attribution'] = deep.display_companies
        new_deep['date_first_publication'] = deep.first_publish_date_display
        new_deep['composition_date'] = deep.composition_date
        new_deep['composition_date_display'] = deep.composition_date_display

        new_deep['theater_type'] = get_theater_type(deep.theater_type_id)
        #TitlePage fields
        new_deep['title_page_title'] = deep.transcript_title
        new_deep['title_page_author'] = deep.transcript_author
        new_deep['title_page_performance'] = deep.transcript_performance
        new_deep['title-page_latin_motto'] = deep.transcript_latin
        new_deep['title_page_imprint'] = deep.transcript_imprint
        new_deep['title_page_illustration'] = deep.illustrationontporfrontis
        new_deep['title_page_explicit'] = deep.transcript_explicit
        new_deep['title_page_colophon'] = deep.transcript_colophon
        

        new_deep['paratext_errata'] = deep.errata
        new_deep['paratext_commendatory_verses'] = deep.transcript_commendatory_verses
        new_deep['paratext_to_the_reader'] = deep.transcript_to_the_reader
        new_deep['paratext_dedication'] = deep.transcript_dedication
        new_deep['paratext_argument'] = deep.transcript_argument
        new_deep['paratext_actor_list'] = deep.transcript_actor_list
        new_deep['paratext_charachter_list'] = deep.transcript_character_list
        new_deep['paratext_other_paratexts'] = deep.other_paratexts

        new_deep['stationer_printer'] = deep.display_printers
        new_deep['stationer_publisher'] = deep.display_publishers
        new_deep['stationer_bookseller'] = deep.display_booksellers
        new_deep['stationer_entries_in_register'] = deep.previous_sr_entry_date
        new_deep['stationer_additional_notes'] = deep.additional_notes

        new_deep['latin'] = True if deep.latin == "Yes" else False
        new_deep['dedication_to'] = True if deep.dedication_to == "Yes" else False
        new_deep['argument'] = True if deep.argument == "Yes" else False
        new_deep['addition_and_correction_attributions'] = True if deep.addition_and_correction_attributions == "Yes" else False
        new_deep['actor_list'] = True if deep.actor_list == "Yes" else False
        new_deep['charlist'] = True if deep.char_list == "Yes" else False
        new_deep['to_the_reader'] = True if deep.to_the_reader == "Yes" else False
        new_deep['commendatory_verses_by'] = True if deep.commendatory_verses_by == "Yes" else False
        new_deep['BIandIC'] = deep.biandic # What is this?
        new_deep['nid'] = deep.nid # Is what?
        new_deep['title_alternative_keywords'] = deep.title_alternative_keywords
        new_deep['transcript_modern_spelling'] = deep.transcript_modern_spelling
        new_deep['transcript_engraved_frontispiece'] = deep.transcript_engraved_frontispiece
        new_deep['transcript_engraved_title'] = deep.transcript_engraved_title
        new_deep['transcript_printed_license'] = deep.transcript_printed_license

        # What purpose do these serve?
        new_deep['collection_full'] = deep.collection_full
        new_deep['collection_middle'] = deep.collection_middle
        new_deep['collection_brief'] = deep.collection_brief
        
        new_deeps.append(new_deep)
    srsly.write_jsonl('deeps.jsonl',new_deeps)

    authors = []
    for author in Author.objects.all():
        authors.append({ "value":author.author_id,"label":author.name})
    srsly.write_json('authors.json',authors)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Database Converted'))