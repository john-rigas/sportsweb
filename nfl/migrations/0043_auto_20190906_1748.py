# Generated by Django 2.2.1 on 2019-09-06 17:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0042_auto_20190906_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 6, 13, 48, 6, 756626)),
        ),
    ]
