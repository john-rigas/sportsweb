import os
import django
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from nfl import models

INITIAL_MAP = {
    'MJ':'unclemike',
    'TJ':'uncletim',
    'JP':'jenkins',
    'MA':'doc',
    'CP':'chris',
    'DT':'david',
    'JM':'johnny',
    'JR':'papou',
    'AJ':'andrew'
}

if not models.WeekRecord.objects.all():
#if True:

    with open('nfl_picks_history.pl','rb') as f:
        data = pickle.load(f)


    for year in range(2005, 2007):
        for initials in data[year].keys():
            name = INITIAL_MAP[initials[:2]]
            player = models.Player.objects.get(name = name)
            for week in range(1,22):
                if week in data[year][initials].keys():
                    models.WeekRecord.objects.create(
                        player = player,
                        year = year,
                        week_no = week,
                        wins = data[year][initials][week][0],
                        losses = data[year][initials][week][1],
                        ties = data[year][initials][week][2] if len(data[year][initials][week]) > 2 else 0
                    )
                else:
                    models.WeekRecord.objects.create(
                        player = player,
                        year = year,
                        week_no = week,
                    )

