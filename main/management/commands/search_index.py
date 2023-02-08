from pathlib import Path
import csv
import srsly
from django.core.management.base import BaseCommand
from lunr import lunr
from tqdm import tqdm

from main.models import *

# Generate search index for use by lunr.js https://lunr.readthedocs.io/en/latest/lunrjs-interop.html

def item_to_dict(item:Item):
    edition = item.edition
    title = item.edition.title
    
    stationer_printer = '; '.join(list(item.stationer_printer.all().values_list('name', flat=True)))
    stationer_publisher = '; '.join(list(item.stationer_publisher.all().values_list('name', flat=True)))
    stationer_bookseller = '; '.join(list(item.stationer_bookseller.all().values_list('name', flat=True)))

    title_page_company_filter = ';'.join(list(item.title_page_company_filter.all().values_list('name', flat=True)))
    company_first_performance_brit_filter = '; '.join(list(item.edition.title.company_first_performance_brit_filter.all().values_list('name', flat=True)))
    company_first_performance_annals_filter = '; '.join(list(item.edition.title.company_first_performance_annals_filter.all().values_list('name', flat=True)))
    
    item_dict = item.__dict__ 
    item_dict['title_page_company_filter'] = title_page_company_filter
    item_dict['stationer_printer_filter'] = stationer_printer
    item_dict['stationer_publisher_filter'] = stationer_publisher
    item_dict['stationer_bookseller_filter'] = stationer_bookseller

    if not item_dict.get('title_page_author_filter',None): # Replace none with 'None' (else search crashes)
        item_dict["title_page_author_filter"] = 'None'
    if not item_dict.get('author_status',None): # Replace none with 'None' (else search crashes)
        item_dict["author_status"] = 'None'
    if not item_dict.get('theater',None): 
        item_dict["theater"] = 'None'
    if not item_dict.get('title_page_genre',None): 
        item_dict["title_page_genre"] = 'None'
        
    if not item_dict.get('title_page_has_latin',None): 
        item_dict["title_page_has_latin"] = 'No'
    # if not item_dict.get('stationer_publisher_filter',None): 
    #     item_dict["stationer_publisher_filter"] = 'None'
    # if not item_dict.get('stationer_printer_filter',None): 
    #     item_dict["stationer_printer_filter"] = 'None'
    # if not item_dict.get('stationer_imprint_location',None): 
        item_dict["stationer_imprint_location"] = 'None'
    # if not item_dict.get('stationer_bookseller_filter',None): 
    #     item_dict["stationer_bookseller_filter"] = 'None'
    item_dict['variant_link'] = ''
    for link in item.variant_links.all():
        item_dict['variant_link'] += f'<a target="_blank" href="../{link.deep_id}">{link.greg_full}</a> '
    if item.in_collection:
        item_dict["in_collection"] = f'<a target="_blank" href="../{item.in_collection.deep_id}">{item.in_collection.title}</a>'
    else: 
        item_dict["in_collection"] = ""
    

    item_dict['collection_contains'] = ''
    if item.collection_contains and item.record_type == "Collection": #m2m
        for i, link in enumerate(item.collection_contains.all()):
            if i == len(item.collection_contains.all())-1:
                item_dict['collection_contains'] += f'<a target="_blank" href="../{link.deep_id}">{link.title}</a> '
            else:
                item_dict['collection_contains'] += f'<a target="_blank" href="../{link.deep_id}">{link.title}</a>; '
    if item.independent_playbook_link:
        item_dict["independent_playbook_link_id"] = item.independent_playbook_link.deep_id
    
    if item.also_in_collection:
        item_dict["also_in_collection_link"] = f'<a target="_blank" href="../{item.also_in_collection_link.deep_id}">{item.also_in_collection}</a>'
    
    if '_state' in item_dict.keys():
        del item_dict['_state']    
    
    
    edition_authors = list(edition.authors.all().values_list('id', flat=True))
    authors_display = ''.join(list(edition.authors.all().values_list('name', flat=True)))
    edition = edition.__dict__
    edition['author_id'] = edition_authors
    edition['author'] = authors_display
    if edition["blackletter"] == "":
        edition["blackletter"] = "No"
    else:
        edition["blackletter"] = "Yes" 
        
    del edition['id']
    if '_state' in edition.keys():
        del edition['_state']    
    if not edition.get('play_type_filter',None): # Replace none with 'None' (else search crashes)
        edition["play_type_filter"] = 'None'
    if not edition.get('play_type_display',None): # Replace none with 'None' (else search crashes)
        edition["play_type_display"] = 'None'

    
    title = title.__dict__
    title["company_first_performance_brit_filter"] = company_first_performance_brit_filter
    title["company_first_performance_annals_filter"] = company_first_performance_annals_filter
    
    if not title.get('company_first_performance_annals_display',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_annals_display"] = 'None'
    if not title.get('company_first_performance_annals_filter',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_annals_filter"] = 'None'
    if not title.get('brit_drama_number',None): # Replace none with 'None' (else search crashes)
        title["brit_drama_number"] = 'None'
    if not title.get('genre_annals_filter',None): # Replace none with 'None' (else search crashes)
        title["genre_annals_filter"] = 'not in Annals'        
    if not title.get('company_first_performance_brit_filter',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_brit_filter"] = 'None'
    if not title.get('company_first_performance_brit_display',None): # Replace none with 'None' (else search crashes)
        title["company_first_performance_brit_display"] = 'None'
    if not title.get('genre_brit_filter',None): # Replace none with 'None' (else search crashes)
        title["genre_brit_filter"] = 'not in BritDrama'
    if not title.get('genre_brit_display',None): # Replace none with 'None' (else search crashes)
        title["genre_brit_display"] = 'not in BritDrama'
   
    title['title_id'] = edition['title_id']
    if '_state' in title.keys():
        del title['_state']    
    

    joined =  item_dict | edition | title
    return joined

#  {
#     "id":57,
#     "edition_id":58,
#     "record_type":"Collection",
#     "collection":"c36b(iv)",
#     "year":"1632",
#     "year_int":1632,
#     "deep_id":"5088",
#     "deep_id_display":null,
#     "greg_full":"n/a",
#     "stc":"22274e.3",
#     "format":"Folio",
#     "leaves":"454",
#     "company_attribution":"n/a",
#     "company_id":1,
#     "composition_date":"n/a",
#     "date_first_publication":"1623",
#     "title_page_title":"[in single column] COMEDIES, | HISTORIES, | and TRAGEDIES.",
#     "title_page_author":"M<sup>R</sup>. WILLIAM SHAKESPEARES",
#     "title_page_author_filter":"Shakespeare, William",
#     "title_page_performance":"",
#     "title_page_latin_motto":"",
#     "title_page_imprint":"Published according to the true Originall Coppies. <i>The second Jmpression</i>. <i>LONDON</i>, Printed by <i>Tho. Cotes</i>, for <i>Robert Allot</i>, and are to be sold at his shop at the signe of the blacke Beare in Pauls Church-yard. 1632.",
#     "title_page_has_latin":"No",
#     "title_page_genre":"None",
#     "title_page_illustration":"Engraved portrait on title page, signed \"Martin Droeshout sculpsit London\"",
#     "title_page_modern_spelling":"Mr William shakespeare's comedies histories and tragedies published according to the true original copies the second impression London printed by tho. Cotes for Robert allott and are to be sold at his shop at the sign of the black bear in paul's churchyard 1632",
#     "paratext_author":null,
#     "paratext_explicit":"",
#     "paratext_errata":"",
#     "paratext_commendatory_verses":"7: by unsigned (2) [<sup>\u03c0</sup>A5r]; by \"L. Digges\"; \"I. M.\" [<sup>\u03c0</sup>A6r]; by \"Ben: Ionson\"; \"I. M. S.\"; \"Hugh Holland\"; [*2r]",
#     "paratext_to_the_reader":"\"To the Reader\" (verses) signed \"B. I.\" (Ben Jonson) [<sup>\u03c0</sup>A1v]; \"To the great variety of Readers\" signed \"John Heminge. Henry Condell.\" [<sup>\u03c0</sup>A4r]",
#     "paratext_dedication":"\"The Epistle Dedicatorie\" <i>to</i>: William Herbert, 3rd Earl of Pembroke; and Philip Herbert, 1st Earl of Montgomery (4th Earl of Pembroke); <i>from</i>: John Heminges; and Henry Condell [<sup>\u03c0</sup>A3r; misprinted A2]",
#     "paratext_argument":"",
#     "paratext_actor_list":"\"The Names of the Principall Actors in all these Playes\" [*1r]",
#     "paratext_charachter_list":"",
#     "paratext_other_paratexts":"\"A Catalogue of all the Comedies, Histories, and Tragedies contained in this Booke\" (including Troilus and Cressida) [*4v]",
#     "stationer_colophon":"Printed at <i>London</i> by <i>Thomas Cotes</i>, for <i>John Smethwick, William Aspley, Richard Hawkins, Richard Meighen</i>, and <i>Robert Allot</i>, 1632. [3d4r]",
#     "stationer_printer":"Cotes, Thomas",
#     "stationer_printer_filter":"Cotes, Thomas",
#     "stationer_publisher":"Allott, Robert",
#     "stationer_publisher_filter":"Allott, Robert",
#     "stationer_license":null,
#     "stationer_imprint_location":"A.3 (Paul's Churchyard - Northeast)",
#     "stationer_bookseller":"",
#     "stationer_bookseller_filter":"None",
#     "stationer_entries_in_register":"Nov 8, 1623: Entered to Edward Blount and Isaac Jaggard: \"M<sup>r</sup>. William Shakspeers Comedyes Histories, & Tragedyes soe manie of the said Copies as are not formerly entred to other men.\".<br />Aug 4, 1626: Transferred from the widow of Thomas Pavier to Edward Brewster and Richard Bird: \"M<sup>r</sup>. Paviers right in Shakesperes plaies or any of them\".<br />Jun 19(?), 1627: Transferred from the widow of Isaac Jaggard to Thomas Cotes and Richard Cotes: \"her p<i>ar</i>te in Shackspheere playes.\"<br />Jul 1, 1637: Transferred from the widow of Robert Allott to John Legat (2) and Andrew Crooke (1) (by order of a court): \"saluo Iure cuiuscunq<i>ue</i> ... Shakespeares workes their Part.\"",
#     "stationer_additional_notes":"The variant issues and states of this edition correspond in STC and Greg as follows: STC 22274=Greg *; STC 22274a=Greg \u2020; STC 22274b=Greg \u00a7; STC 22274c=Greg **; STC 22274d=Greg \u2020\u2020; STC 22274e=Greg \u2021; STC 22274e.3=first '1632' <i>reissue</i>; STC 22274e.5=second '1632' <i>reissue</i>.",
#     "theater_type":"None",
#     "theater":"None",
#     "variants":"There are five issues of this collection, varying in the imprint. <b>Issue 1:</b> lists Allot as publisher, and its imprint exists in four main states: STC 22274 reads \"to be fold at his shop at the signe of the Blacke Beare\" in \"Pauls Church-yard\"; STC 22274a reads \"to be fold at the signe\"; in STC 22274e.3, the original sheet <sup>\u03c0</sup>A2.5 was replaced by a cancel, which is printed on thicker paper and probably dates from 1641, after Thomas Cotes died; it corrects \"fold\" to \"sold\", lists the sign for Allot's shop as \"the blacke Beare\", and is otherwise the same as STC 22274; STC 22274e.5 also contains a cancel sheet <sup>\u03c0</sup>A2.5 similar to STC 22274e.3; it lists the sign for Allot's shop as \"the blacke Beare\" in \"<i>Pauls</i> Church yard,\" and also contains variant states with either \"according\" or \"accodring.\" <b>Issue 2:</b> STC 22274b lists Aspley as publisher at the Parrot in Paul's Churchyard. <b>Issue 3:</b> STC 22274c lists Hawkins as publisher in Chancery Lane, near Sergeant's Inn; in its two states, the imprint reads either \"shop in Chancery\" or \"shop Chancery.\" <b>Issue 4:</b> STC 22274d lists Meighen as publisher at the Middle Temple Gate in Fleet Street. <b>Issue 5:</b> STC 22274e lists Smethwick as publisher in St. Dunstan's Churchyard. See also STC ",
#     "in_collection_id":null,
#     "independent_playbook":null,
#     "independent_playbook_link_id":null,
#     "also_in_collection":null,
#     "also_in_collection_link_id":null,
#     "collection_full":"c36b(iv)",
#     "collection_middle":"c36b",
#     "collection_brief":"36",
#     "variant_edition_id":"1476",
#     "variant_newish_primary_deep_id":"1476",
#     "author_status":"Master",
#     "srstationer":null,
#     "publisher":"Allott, Robert",
#     "printer":"Cotes, Thomas",
#     "variant_link":"<a target=\"_blank\" href=\"../5089\">n/a</a> <a target=\"_blank\" href=\"../5084\">n/a</a> <a target=\"_blank\" href=\"../5086\">n/a</a> <a target=\"_blank\" href=\"../5083\">n/a</a> <a target=\"_blank\" href=\"../5082\">n/a</a> <a target=\"_blank\" href=\"../5085\">n/a</a> <a target=\"_blank\" href=\"../5087\">n/a</a> ",
#     "in_collection":"",
#     "collection_contains":"<a target=\"_blank\" href=\"../5082.29\">Timon of Athens</a>; <a target=\"_blank\" href=\"../5082.20\">1 Henry the Sixth</a>; <a target=\"_blank\" href=\"../5082.31\">Macbeth</a>; <a target=\"_blank\" href=\"../5082.21\">2 Henry the Sixth (The First Part of the Contention of the Two Famous Houses of York and Lancaster)</a>; <a target=\"_blank\" href=\"../5082.03\">The Merry Wives of Windsor</a>; <a target=\"_blank\" href=\"../5082.01\">The Tempest</a>; <a target=\"_blank\" href=\"../5082.32\">Hamlet, Prince of Denmark</a>; <a target=\"_blank\" href=\"../5082.24\">Henry the Eighth (All Is True)</a>; <a target=\"_blank\" href=\"../5082.06\">Much Ado About Nothing</a>; <a target=\"_blank\" href=\"../5082.07\">Love's Labor's Lost</a>; <a target=\"_blank\" href=\"../5082.35\">Antony and Cleopatra</a>; <a target=\"_blank\" href=\"../5082.34\">Othello, the Moor of Venice</a>; <a target=\"_blank\" href=\"../5082.02\">The Two Gentlemen of Verona</a>; <a target=\"_blank\" href=\"../5082.25\">Troilus and Cressida</a>; <a target=\"_blank\" href=\"../5082.19\">Henry the Fifth</a>; <a target=\"_blank\" href=\"../5082.18\">2 Henry the Fourth</a>; <a target=\"_blank\" href=\"../5082.33\">King Lear</a>; <a target=\"_blank\" href=\"../5082.23\">Richard the Third</a>; <a target=\"_blank\" href=\"../5082.04\">Measure for Measure</a>; <a target=\"_blank\" href=\"../5082.30\">Julius Caesar</a>; <a target=\"_blank\" href=\"../5082.28\">Romeo and Juliet</a>; <a target=\"_blank\" href=\"../5082.16\">Richard the Second</a>; <a target=\"_blank\" href=\"../5082.27\">Titus Andronicus</a>; <a target=\"_blank\" href=\"../5082.26\">Coriolanus</a>; <a target=\"_blank\" href=\"../5082.13\">Twelfth Night, or What You Will</a>; <a target=\"_blank\" href=\"../5082.17\">1 Henry the Fourth</a>; <a target=\"_blank\" href=\"../5082.36\">Cymbeline, King of Britain</a>; <a target=\"_blank\" href=\"../5082.10\">As You Like It</a>; <a target=\"_blank\" href=\"../5082.15\">King John</a>; <a target=\"_blank\" href=\"../5082.05\">The Comedy of Errors</a>; <a target=\"_blank\" href=\"../5082.09\">The Merchant of Venice (The Jew of Venice)</a>; <a target=\"_blank\" href=\"../5082.11\">The Taming of the Shrew</a>; <a target=\"_blank\" href=\"../5082.08\">A Midsummer Night's Dream</a>; <a target=\"_blank\" href=\"../5082.12\">All's Well That Ends Well</a>; <a target=\"_blank\" href=\"../5082.14\">The Winter's Tale</a>; <a target=\"_blank\" href=\"../5082.22\">3 Henry the Sixth (The True Tragedy of Richard Duke of York and the Good King Henry the Sixth)</a> ",
#     "title_id":57,
#     "greg_middle":"",
#     "book_edition":"2",
#     "play_edition":"n/a",
#     "play_type_filter":"Collection;Professional;Adult Professional",
#     "play_type_display":"Collection of Adult Professional Plays",
#     "blackletter":"No",
#     "author_id":[
#       10
#     ],
#     "author":"Shakespeare, William",
#     "authors_display":"Shakespeare, William",
#     "title":"Comedies, Histories, and Tragedies",
#     "title_alternative_keywords":"",
#     "greg":"",
#     "brit_drama_number":"None",
#     "genre_annals_display":null,
#     "genre_annals_filter":"not in Annals",
#     "genre_brit_display":"not in BritDrama",
#     "genre_brit_filter":"not in BritDrama",
#     "date_first_publication_display":"1623",
#     "date_first_performance":"n/a",
#     "date_first_performance_brit_filter":null,
#     "date_first_performance_brit_display":null,
#     "company_first_performance_annals_display":"None",
#     "company_first_performance_annals_filter":"None",
#     "company_first_performance_brit_display":"None",
#     "company_first_performance_brit_filter":"None",
#     "total_editions":"2 folios",
#     "stationers_register":null,
#     "genre_wiggins":null
#   },


class Command(BaseCommand):
    help = 'Generates a item_data for the site'
    
    def handle(self, *args, **options):
        items = [item_to_dict(item) for item in tqdm(Item.objects.all())]
        item_data = {}
        for item in items: 
            item_data[item['deep_id']] = item
        # create json item lookup for search results 
        srsly.write_json(Path('main/assets/data/item_data.json'), item_data)
        self.stdout.write(self.style.SUCCESS('Created item data'))
        # Write data to csv 
        data_file = open('main/assets/data/DEEP_data.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        count = 0
        for key_ in item_data.keys():
            if count == 0:
                header = item_data[key_].keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(item_data[key_].values())
        
        data_file.close()
        self.stdout.write(self.style.SUCCESS('Wrote data to CSV'))