# Generated by Django 2.2.1 on 2019-09-05 23:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0031_auto_20190905_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 5, 19, 1, 13, 585697)),
        ),
    ]
