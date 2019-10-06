import os
import django
import pickle
from django.db.models import Q
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from nfl import models
from nfl import utils

if not models.TeamRecord.objects.all():
    for player in models.Player.objects.all():
        for team in models.Team.objects.all():
            selections = models.Selection.objects.filter(player=player).filter(Q(game__home_team=team) | Q(game__away_team=team))
            wins = 0
            losses = 0
            ties = 0
            for selection in selections:
                if selection.game.gametime + timedelta(days=1) < utils.get_current_datetime():
                    if selection.success == 1:
                        wins += 1
                    elif selection.success == 2:
                        losses += 1
                    elif selection.success == 3:
                        ties += 1
            models.TeamRecord.objects.create(
                timeframe = 'Y',
                player = player,
                team = team,
                wins = wins,
                losses = losses,
                ties = ties,
            )
            models.TeamRecord.objects.create(
                timeframe = 'C',
                player = player,
                team = team,
                wins = 0,
                losses = 0,
                ties = 0,
            )