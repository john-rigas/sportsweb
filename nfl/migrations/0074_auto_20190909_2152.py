# Generated by Django 2.2.1 on 2019-09-09 21:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0073_auto_20190908_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 9, 17, 52, 52, 639927)),
        ),
    ]
