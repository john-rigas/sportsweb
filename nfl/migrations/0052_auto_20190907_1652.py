# Generated by Django 2.2.1 on 2019-09-07 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0051_auto_20190906_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 7, 12, 52, 24, 706375)),
        ),
    ]