# Generated by Django 2.2.1 on 2019-09-06 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0036_auto_20190906_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 6, 10, 15, 5, 291780)),
        ),
    ]