"""deep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views

admin.site.site_header = 'DEEP'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('download.html', views.download, name='download'),
    path('sources.html', views.sources, name='sources'),
    path('about.html', views.about, name='about'),
    path('title_autocomplete/', views.TitleAutocomplete.as_view(), name='title_autocomplete'),
    path('person_autocomplete/', views.PersonAutocomplete.as_view(), name='person_autocomplete'),
    path('theater_autocomplete/', views.TheaterAutocomplete.as_view(), name='theater_autocomplete'),
    path('<deep_id>.html', views.item_page, name='item_page'),
]
