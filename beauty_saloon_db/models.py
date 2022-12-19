from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Client(models.Model):
    name = models.CharField('ФИО клиента', max_length=200)
    phone_number = PhoneNumberField('Телефонный номер клиента',
                                    region='RU',
                                    blank=True,
                                    max_length=20)
    telegram_id = models.CharField('ID клиента в Telegram',
                                   max_length=100,
                                   blank=True)

    def __str__(self):
        return f"{self.name} {self.phone_number}"


class Saloon(models.Model):
    name = models.CharField('Название салона', max_length=200)
    address = models.CharField('Адрес', max_length=400)
    longitude = models.FloatField('Долгота')
    latitude = models.FloatField('Широта')

    def __str__(self):
        return f"{self.name} {self.address}"


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=300)
    price = models.DecimalField('Стоимость услуги',
                                max_digits=10,
                                decimal_places=2,
                                blank=True,
                                null=True)

    def __str__(self):
        return f"{self.name} {self.price}"


class Master(models.Model):
    name = models.CharField('ФИО мастера', max_length=200)
    services = models.ManyToManyField(Service,
                                      blank=True,
                                      related_name='masters',
                                      verbose_name='Услуги')
    saloons = models.ManyToManyField(Saloon,
                                     blank=True,
                                     null=True,
                                     related_name='masters',
                                     verbose_name='Салоны')

    def __str__(self):
        return f"{self.name}"


class Visit(models.Model):
    service = models.ForeignKey(Service,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='visits',
                                verbose_name='Услуга')
    master = models.ForeignKey(Master,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='visits',
                               verbose_name='Закреплённый мастер')
    start_datetime = models.DateTimeField('Дата и время визита',
                                          db_index=True)
    saloon = models.ForeignKey(Saloon,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='visits',
                               verbose_name='Салон красоты')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='visits',
                               verbose_name='Клиент')

    def __str__(self):
        return f"{self.start_datetime} - {self.client.name} / Мастер " \
               f"{self.master.name} в {self.saloon.name}"


class Day(models.Model):
    date = models.DateField('Дата', null=True, blank=True)
    saloon = models.ForeignKey(Saloon,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='days',
                               verbose_name='Салон')
    master = models.ForeignKey(Master,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='days',
                               verbose_name='Назначенный мастер')

    def __str__(self):
        return f"{self.date} {self.saloon.name} {self.master.name}"


class WorkingTime(models.Model):
    starting_time = models.TimeField('Начало сеанса')
    finishing_time = models.TimeField('Конец сеанса')
    busy = models.BooleanField('Занято ли время')
    day = models.ForeignKey(Day,
                            on_delete=models.CASCADE,
                            related_name='working_times',
                            verbose_name='День')

    def __str__(self):
        return f"{self.day.date} {self.starting_time} " \
               f"{self.day.master.name}/Занято:{self.busy}"
