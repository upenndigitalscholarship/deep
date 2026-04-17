# Register your models here.
from django.apps import apps
from django.contrib import admin

from main.models import Edition, Item, Person, Title, Company, StationerImprintLocation

from django import forms


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['deep_id','greg_full','edition__title__title']
    filter_horizontal = ['stationer_imprint_location_filter']
    #raw_id_fields = ('title_page_company_filter','stationer_printer','stationer_publisher','stationer_bookseller','variant_links','in_collection','also_in_collection_link','collection_contains','independent_playbook_link')
admin.site.register(Item, ItemAdmin)

class EditionAdmin(admin.ModelAdmin):
    list_filter = ['greg_middle','title__title']
admin.site.register(Edition, EditionAdmin)

class TitleAdmin(admin.ModelAdmin):
    list_filter = ['title','greg'] 

admin.site.register(Title, TitleAdmin)

class PeopleAdmin(admin.ModelAdmin):
    list_filter = ['name']

admin.site.register(Person, PeopleAdmin)

class CompanyAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Company, CompanyAdmin)


class StationerImprintLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'supra_category', 'moeml_link']
    list_filter = ['supra_category']
    search_fields = ['name', 'moeml_link']


admin.site.register(StationerImprintLocation, StationerImprintLocationAdmin)


# models = apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
