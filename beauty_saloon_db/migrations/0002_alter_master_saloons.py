# Generated by Django 4.1.4 on 2022-12-19 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_saloon_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='saloons',
            field=models.ManyToManyField(blank=True, related_name='masters', to='beauty_saloon_db.saloon', verbose_name='Салоны'),
        ),
    ]
