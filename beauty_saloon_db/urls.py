from django.contrib import admin
from django.urls import path, include

from beauty_saloon_db.views import (
    SaloonsListView,
    SaloonDetailView,
    ServicesListView,
    DaysListView,
    DayListMastersView,
)

app_name='beauty_saloon_db'
urlpatterns = [
    path('saloon/all/', SaloonsListView.as_view()),
    path('saloon/<int:pk>/', SaloonDetailView.as_view()),
    path('service/all/', ServicesListView.as_view()),
    path('day/week/', DaysListView.as_view()),
    path('day/<int:year>/<int:month>/<int:day>/<str:saloon>/masters/',
         DayListMastersView.as_view()),
]