# Register your models here.
from django.apps import apps
from django.contrib import admin

from main.models import Edition, Item, Person, Title, Company

from django import forms


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['deep_id','greg_full','edition__title__title']
admin.site.register(Item, ItemAdmin)

class EditionAdmin(admin.ModelAdmin):
    list_filter = ['greg_middle','title__title']
admin.site.register(Edition, EditionAdmin)

class TitleAdmin(admin.ModelAdmin):
    list_filter = ['title','greg'] 

admin.site.register(Title, TitleAdmin)

class PeopleAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Person, PeopleAdmin)

class CompanyAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Company, CompanyAdmin)

# models = apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
