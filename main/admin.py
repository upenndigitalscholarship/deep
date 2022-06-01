from django.contrib import admin

# Register your models here.
from django.apps import apps
from main.models import Item, Edition 

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['edition__title__title']
    list_filter = ['edition__title__title','edition__title__genre']
admin.site.register(Item, ItemAdmin)

class EditionAdmin(admin.ModelAdmin):
    search_fields = ['title__title']
    list_filter = ['title__genre']
admin.site.register(Edition, EditionAdmin)

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass