# Generated by Django 2.2.1 on 2019-09-06 18:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0044_auto_20190906_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 6, 14, 2, 16, 206044)),
        ),
    ]