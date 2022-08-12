from django.shortcuts import render
from django.db.models import Max, Min
from main.models import Item, Title, Person, Theater
from dal import autocomplete

# Create your views here.
def index(request):
    context = {}
    context['min_year'] = Item.objects.aggregate(Min('year_int'))['year_int__min']
    context['max_year'] = Item.objects.aggregate(Max('year_int'))['year_int__max']
    return render(request, 'index.html', context)

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