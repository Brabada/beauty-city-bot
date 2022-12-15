from django.contrib import admin
from django.urls import path, include

from beauty_saloon_db.views import SaloonsListView

app_name='beauty_saloon_db'
urlpatterns = [
    path('saloon/all/', SaloonsListView.as_view())
]