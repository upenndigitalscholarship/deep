from django.shortcuts import render
from django.db.models import Max, Min
from main.models import Item, Title, Person, Theater, Edition
from dal import autocomplete

def item_to_dict(item:Item):
    item_dict = item.__dict__ 
    
    item_dict['variant_link'] = ''
    for link in item.variant_links.all():
        item_dict['variant_link'] += f'<a href="{link.deep_id}.html">{link.greg_full}</a> '
    
    item_dict["collection_contains_links"] = []
    for link in item.collection_contains.all():
        item_dict['collection_contains_links'].append(dict(text=link.edition.title.title,href=link.deep_id))

    if '_state' in item_dict.keys():
        del item_dict['_state']    
    
    edition = Edition.objects.get(id=item_dict['edition_id'])
    edition_authors = list(edition.authors.all().values_list('id', flat=True))
    authors_display = ''.join(list(edition.authors.all().values_list('name', flat=True)))
    play_type = ''.join(list(edition.play_type.all().values_list('name', flat=True)))
    edition = edition.__dict__
    edition['author_id'] = edition_authors
    edition['author'] = authors_display
    edition['play_type'] = play_type
    del edition['id']
    if '_state' in edition.keys():
        del edition['_state']    

    title = Title.objects.get(id=edition['title_id'])
    title = title.__dict__
    title['title_id'] = edition['title_id']
    if '_state' in title.keys():
        del title['_state']    
    

    joined =  item_dict | edition | title
    joined['lunr_id'] = item_dict['id']
    return joined


# Create your views here.
def index(request):
    context = {}
    context['min_year'] = Item.objects.aggregate(Min('year_int'))['year_int__min']
    context['max_year'] = Item.objects.aggregate(Max('year_int'))['year_int__max']
    return render(request, 'index.html', context)

def item_page(request, deep_id):
    context = {}
    context['data'] = item_to_dict(Item.objects.get(deep_id=deep_id))
    return render(request, 'item_page.html', context)

def browse(request):
    return render(request, 'browse.html')

def about(request):
    return render(request, 'about.html')



class TitleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(edition__title__title__istartswith=self.q)

        return qs

class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TheaterAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = Theater.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs