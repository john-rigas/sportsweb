# Generated by Django 2.2.1 on 2019-09-01 15:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0004_auto_20190901_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gametime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
