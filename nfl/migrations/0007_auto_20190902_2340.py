# Generated by Django 2.2.1 on 2019-09-02 23:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0006_auto_20190902_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 2, 19, 40, 5, 263505)),
        ),
    ]
