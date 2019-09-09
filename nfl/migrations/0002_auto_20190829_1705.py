# Generated by Django 2.2.1 on 2019-08-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='away_score',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_score',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='week_no',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='game',
            name='year',
            field=models.PositiveSmallIntegerField(default=2019),
        ),
    ]
