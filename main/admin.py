# Register your models here.
from django.apps import apps
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from main.models import Edition, Item, Person, Title

from django import forms


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['deep_id','greg_full','edition__title__title']
admin.site.register(Item, ItemAdmin)

class EditionAdmin(admin.ModelAdmin):
    list_filter = ['title__deep_id','greg_middle','title__title']
admin.site.register(Edition, EditionAdmin)

class TitleAdmin(admin.ModelAdmin):
    list_filter = ['deep_id','title','greg'] 

admin.site.register(Title, TitleAdmin)

class PeopleAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Person, PeopleAdmin)

# models = apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
