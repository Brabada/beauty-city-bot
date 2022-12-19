# Generated by Django 4.1.4 on 2022-12-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_saloon_db', '0002_alter_master_saloons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saloon',
            name='latitude',
            field=models.FloatField(blank=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='saloon',
            name='longitude',
            field=models.FloatField(blank=True, verbose_name='Долгота'),
        ),
    ]
