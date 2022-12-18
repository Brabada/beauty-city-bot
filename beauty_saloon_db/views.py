from django.shortcuts import render
from rest_framework import generics

from beauty_saloon_db.serializers import SaloonsListSerializer
from beauty_saloon_db.models import Saloon

# Create your views here.
class SaloonsListView(generics.ListAPIView):
    serializer_class = SaloonsListSerializer

    queryset = Saloon.objects.all()