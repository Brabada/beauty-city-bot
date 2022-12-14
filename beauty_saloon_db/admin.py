from django.contrib import admin

from .models import Client, Visit, Master, Service, Saloon, Day, WorkingTime
# Register your models here.

admin.site.register(Client)
admin.site.register(Visit)
admin.site.register(Master)
admin.site.register(Service)
admin.site.register(Saloon)
admin.site.register(Day)
admin.site.register(WorkingTime)
