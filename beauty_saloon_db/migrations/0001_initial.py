# Generated by Django 4.1.4 on 2022-12-14 16:55

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО клиента')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, region='RU', verbose_name='Телефонный номер клиента')),
                ('telegram_id', models.CharField(blank=True, max_length=100, verbose_name='ID клиента в Telegram')),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата')),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО мастера')),
            ],
        ),
        migrations.CreateModel(
            name='Saloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название салона')),
                ('address', models.CharField(max_length=400, verbose_name='Адрес')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('latitude', models.FloatField(verbose_name='Широта')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Название услуги')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Стоимость услуги')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_time', models.TimeField(verbose_name='Начало сеанса')),
                ('finishing_time', models.TimeField(verbose_name='Конец сеанса')),
                ('busy', models.BooleanField(verbose_name='Занято ли время')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_times', to='beauty_saloon_db.day', verbose_name='День')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(db_index=True, verbose_name='Дата и время визита')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='beauty_saloon_db.client', verbose_name='Клиент')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visits', to='beauty_saloon_db.master', verbose_name='Закреплённый мастер')),
                ('saloon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visits', to='beauty_saloon_db.saloon', verbose_name='Салон красоты')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visits', to='beauty_saloon_db.service', verbose_name='Услуга')),
            ],
        ),
        migrations.AddField(
            model_name='master',
            name='saloons',
            field=models.ManyToManyField(blank=True, null=True, related_name='masters', to='beauty_saloon_db.saloon', verbose_name='Салоны'),
        ),
        migrations.AddField(
            model_name='master',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='masters', to='beauty_saloon_db.service', verbose_name='Услуги'),
        ),
        migrations.AddField(
            model_name='day',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='days', to='beauty_saloon_db.master', verbose_name='Назначенный мастер'),
        ),
        migrations.AddField(
            model_name='day',
            name='saloon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='days', to='beauty_saloon_db.saloon', verbose_name='Салон'),
        ),
    ]
