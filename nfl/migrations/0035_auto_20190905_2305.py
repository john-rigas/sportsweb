# Generated by Django 2.2.1 on 2019-09-05 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0034_auto_20190905_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 5, 19, 5, 47, 998693)),
        ),
    ]
