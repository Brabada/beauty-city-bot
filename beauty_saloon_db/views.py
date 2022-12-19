from django.shortcuts import render
from django.db import models
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

import datetime

from beauty_saloon_db.serializers import (
    SaloonsListSerializer,
    SaloonDetailSerializer,
    ServiceSerializer,
    DaysListSerializer,
    DayListMastersSerializer,
)

from beauty_saloon_db.models import Saloon, Service, Day

# Create your views here.
class SaloonsListView(generics.ListAPIView):
    serializer_class = SaloonsListSerializer
    queryset = Saloon.objects.all()


class SaloonDetailView(generics.RetrieveAPIView):
    serializer_class = SaloonDetailSerializer
    queryset = Saloon.objects.all()


class ServicesListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class DaysListView(generics.ListAPIView):
    serializer_class = DaysListSerializer
    queryset = Day.objects.filter(date__gte=datetime.date.today()).exclude(
        date__gt=datetime.date.today() + datetime.timedelta(days=8)
    ).values("date").annotate(n=models.Count("pk"))


class DayListMastersView(APIView):
    def get(self, request, year, month, day, saloon):
        date = datetime.date(year, month, day)
        days = Day.objects.filter(date__exact=date, saloon__pk=saloon)
        # days = Day.objects.filter(date__exact=date,
        # saloon__name__exact=saloon) а так не выводит

        print(days)
        serializer = DayListMastersSerializer(days, many=True)
        return Response(serializer.data)

