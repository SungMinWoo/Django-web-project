from django.urls import path
from .views import *

app_name = 'main_page'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('search', search_all, name='search'),
]
