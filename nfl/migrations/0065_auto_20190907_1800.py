# Generated by Django 2.2.1 on 2019-09-07 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0064_auto_20190907_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 7, 14, 0, 47, 935126)),
        ),
    ]
