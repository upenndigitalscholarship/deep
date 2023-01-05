from dal import autocomplete
from django.db.models import Max, Min
from django.shortcuts import render,redirect
from django.core.management import call_command

from main.management.commands.search_index import item_to_dict
from main.models import Edition, Item, Person, Theater, Title


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

def build(request):
    call_command('build')
    return redirect('admin:index')

def browse(request):
    return render(request, 'browse.html')

def about(request):
    return render(request, 'about.html')

def download(request):
    return render(request, 'download.html')

def sources(request):
    return render(request, 'sources.html')

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