# Generated by Django 2.2.1 on 2019-09-06 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0046_auto_20190906_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 6, 14, 8, 42, 730518)),
        ),
    ]
