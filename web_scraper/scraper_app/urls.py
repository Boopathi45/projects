from django.contrib import admin
from django.urls import path
from .import views

app_name = 'scraper_app'
urlpatterns = [
    path('',views.intro, name='intro_page'),
    path('lists',views.scrape, name='scrape'),
    path('delete',views.delete, name='delete'),
    path('del_config',views.del_config, name='del_config')
]
