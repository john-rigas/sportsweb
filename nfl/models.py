from django.db import models
from django.db.models import Q
import pickle
import time
from datetime import date, datetime
from django.utils import timezone
import pytz

# Create your models here.
def load_teams_to_db():
    with open('team_set.pl','rb') as f:
        teams = pickle.load(f)
    for team in teams:
        Team.objects.create(name = team)

def load_schedule_to_db_from_pl():
    with open('saved_schedule.pl','rb') as f:
        schedule = pickle.load(f)
    for i in range(1,18):
        for game in schedule[i]:
            home_team_obj = Team.objects.get(name = game['home_team'])
            away_team_obj = Team.objects.get(name = game['away_team'])
            Game.objects.create(
                home_team = home_team_obj,
                away_team = away_team_obj,
                home_score = 0 if game['home_score'] == '' else int(game['home_score']),
                away_score = 0 if game['away_score'] == '' else int(game['away_score']),
                week_no = i,
                gametime = game['gametime']
            )

def load_results_to_db_from_pl():
    with open('saved_results.pl','rb') as f:
        results = pickle.load(f)
    for week in results.keys():
        for game_result in results[week]:
            game_to_update = Game.objects.filter(week_no = week).filter(
                                              Q(home_team__name = game_result['winning_team']) |
                                              Q(away_team__name = game_result['winning_team']))[0]

            if game_result['winning_team'] == game_to_update.home_team.name:
                game_to_update.home_score = game_result['winning_score']
                game_to_update.away_score = game_result['losing_score']
            else:
                game_to_update.home_score = game_result['losing_score']
                game_to_update.away_score = game_result['winning_score']               

            game_to_update.save()

def generate_db_selections(player):
    for game in Game.objects.all():
        Selection.objects.create(game = game, player = player)

def get_current_datetime():
    return datetime.now(pytz.timezone('US/Eastern')).replace(
                                                        tzinfo=None,
                                                        second=0,
                                                        microsecond=0)

def get_current_week():
    current_datetime = get_current_datetime()
    week_one_start = datetime(2019, 9, 3, 0, 0)
    days_since_opener = (current_datetime - week_one_start).days
    current_week = 1 + (days_since_opener // 7) if days_since_opener > 0 else 1
    return current_week


def update_player_records():
    for player in Player.objects.all():
        player.wins = 0
        player.losses = 0
        player.ties = 0
        for game in Game.objects.all():
            winner = get_game_winner(game)

            selection = Selection.objects.get(player = player, game = game)
            if winner == None:
                pass
            elif winner == selection.prediction:
                player.wins += 1
            elif winner == 'TIE':
                player.ties += 1
            else:
                player.losses += 1
        player.save()

def update_team_records():
    for team in Team.objects.all():
        team.wins = 0
        team.losses = 0
        team.ties = 0
        for game in Game.objects.filter(Q(home_team = team) | Q(away_team = team)):
            winner = get_game_winner(game)
            if winner == None:
                pass
            elif winner == team:
                team.wins += 1
            elif winner == 'TIE':
                team.ties += 1
            else:
                team.losses += 1
        team.save()


def get_game_winner(game):
    if game.gametime > get_current_datetime():
        winner = None
    elif game.home_score > game.away_score:
        winner = game.home_team
    elif game.away_score > game.home_score:
        winner = game.away_team
    else:
        winner = 'TIE'
    return winner



class Team(models.Model):
    name = models.TextField()
    wins = models.PositiveSmallIntegerField(default = 0)
    losses = models.PositiveSmallIntegerField(default = 0)
    ties = models.PositiveSmallIntegerField(default = 0)

    def __str__(self):
        if self.ties == 0:
            string_rep = f"{self.name} {self.wins}-{self.losses}"
        else:
            string_rep = f"{self.name} {self.wins}-{self.losses}-{self.ties}"
        return string_rep

class Game(models.Model):
    home_team = models.ForeignKey(Team, models.CASCADE, related_name = 'home_team')
    away_team = models.ForeignKey(Team, models.CASCADE, related_name = 'away_team')
    home_score = models.PositiveSmallIntegerField(default = 0)
    away_score = models.PositiveSmallIntegerField(default = 0)
    week_no = models.PositiveSmallIntegerField(default = 1)
    gametime = models.DateTimeField(
        default = datetime.now(pytz.timezone('US/Eastern')).replace(tzinfo=None)) 

    def __str__(self):
        return str(self.gametime.strftime("%b %d %Y %H:%M")) + ' ' + self.away_team.name + ' at ' + self.home_team.name

class Player(models.Model):
    name = models.TextField()
    wins = models.PositiveSmallIntegerField(default = 0)
    losses = models.PositiveSmallIntegerField(default = 0)
    ties = models.PositiveSmallIntegerField(default = 0)

    def __str__(self):
        return self.name

class Selection(models.Model):
    game = models.ForeignKey(Game, models.CASCADE, null = False, blank=False)
    player = models.ForeignKey(Player, models.CASCADE)
    prediction = models.ForeignKey(Team, 
                                   models.CASCADE, 
                                   null=True)
