# Generated by Django 2.2.1 on 2019-10-05 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0086_auto_20191004_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', models.TextField(choices=[('C', 'Career'), ('Y', 'Year')])),
                ('wins', models.PositiveSmallIntegerField(default=0)),
                ('losses', models.PositiveSmallIntegerField(default=0)),
                ('ties', models.PositiveSmallIntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nfl.Player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nfl.Team')),
            ],
        ),
    ]
