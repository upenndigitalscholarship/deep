from django.shortcuts import render
from main.models import Item, Title
from dal import autocomplete

# Create your views here.
def index(request):
    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})

def about(request):
    return render(request, 'about.html')


class TitleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = Title.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs