from django.shortcuts import render
from main.models import Item, Title, Person, Theater
from dal import autocomplete

# Create your views here.
def index(request):
    return render(request, 'index.html')

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