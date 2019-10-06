from django.db import models
from django.db.models import Q
import pickle
import time
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.conf import settings
import pytz
from sportsweb.users import create_user
import os
from nfl import utils


class TeamManager(models.Manager):
    def load_teams_to_db(self):
        with open('team_set.pl', 'rb') as f:
            teams = pickle.load(f)
        for team in teams:
            self.model.objects.create(name=team)

    def add_abbreviations_to_teams(self):
        with open('team_abbreviations.pl', 'rb') as f:
            abbreviations = pickle.load(f)
        for team in self.model.objects.all():
            team.abbrv = abbreviations[team.name]
            team.save()

    def update_team_records(self):
        for team in self.model.objects.all():
            team.wins = 0
            team.losses = 0
            team.ties = 0
            for game in Game.objects.filter(Q(home_team=team) | Q(away_team=team)):
                winner = game.get_game_winner()
                if winner == None:
                    pass
                elif winner == team:
                    team.wins += 1
                elif winner == 'TIE':
                    team.ties += 1
                else:
                    team.losses += 1
            team.save()


class Team(models.Model):
    name = models.TextField()
    abbrv = models.TextField(default='')
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    ties = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if self.ties == 0:
            string_rep = f"{self.name} {self.wins}-{self.losses}"
        else:
            string_rep = f"{self.name} {self.wins}-{self.losses}-{self.ties}"
        return string_rep
    objects = TeamManager()


class GameManager(models.Manager):
    def load_schedule_to_db_from_pl(self):
        with open('saved_schedule.pl', 'rb') as f:
            schedule = pickle.load(f)
        for i in range(1, 18):
            for game in schedule[i]:
                home_team_obj = Team.objects.get(name=game['home_team'])
                away_team_obj = Team.objects.get(name=game['away_team'])
                self.model.objects.create(
                    home_team=home_team_obj,
                    away_team=away_team_obj,
                    home_score=0 if game['home_score'] == '' else int(
                        game['home_score']),
                    away_score=0 if game['away_score'] == '' else int(
                        game['away_score']),
                    week_no=i,
                    gametime=game['gametime']
                )

    def load_results_to_db_from_pl(self):
        with open('saved_results.pl', 'rb') as f:
            results = pickle.load(f)
        for week in results.keys():
            for game_result in results[week]:
                if game_result['winning_score']:
                    game_to_update = self.model.objects.filter(week_no=week).filter(
                        Q(home_team__name=game_result['winning_team']) |
                        Q(away_team__name=game_result['winning_team']))[0]

                    if game_result['winning_team'] == game_to_update.home_team.name:
                        game_to_update.home_score = int(
                            game_result['winning_score'])
                        game_to_update.away_score = int(
                            game_result['losing_score'])
                    else:
                        game_to_update.home_score = int(
                            game_result['losing_score'])
                        game_to_update.away_score = int(
                            game_result['winning_score'])

                    game_to_update.save()


class Game(models.Model):
    home_team = models.ForeignKey(
        Team, models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(
        Team, models.CASCADE, related_name='away_team')
    home_score = models.PositiveSmallIntegerField(default=0)
    away_score = models.PositiveSmallIntegerField(default=0)
    week_no = models.PositiveSmallIntegerField(default=1)
    gametime = models.DateTimeField(default=datetime(2019, 9, 2, 0, 0))
    objects = GameManager()

    def __str__(self):
        return str(self.gametime.strftime("%b %d %Y  -  %H:%M")) + ' - ' + self.away_team.name + ' at ' + self.home_team.name

    def get_game_winner(self):
        if not self.home_score and not self.away_score:
            winner = None
        elif self.home_score > self.away_score:
            winner = self.home_team
        elif self.away_score > self.home_score:
            winner = self.away_team
        else:
            winner = 'TIE'
        return winner


class PlayerManager(models.Manager):
    def create_family_players(self):
        for person in utils.people:
            player = self.model.objects.create(name=person[2], cell=person[3])
            Selection.objects.generate_db_selections(player)  # same as above
            create_user(person[2], person[1], person[2])

    def update_player_records(self):
        leader = None
        for player in Player.objects.all():
            player.wins = 0
            player.losses = 0
            player.ties = 0
            player.gb = 0
            player.fwins = 0
            player.flosses = 0
            player.fties = 0
            for selection in Selection.objects.filter(player=player):
                if selection.success == 0:
                    pass
                elif selection.success == 1:
                    player.wins += 1
                elif selection.success == 2:
                    player.losses += 1
                elif selection.success == 3:
                    player.ties += 1
                elif selection.success == 5:
                    player.fwins += 1
                elif selection.success == 6:
                    player.flosses += 1
                elif selection.success == 7:
                    player.fties += 1
                else:
                    pass

            if leader is None:
                leader = player
            else:
                if (player.wins + player.fwins - player.losses - player.flosses) > (leader.wins + leader.fwins - leader.losses - leader.flosses):
                    leader = player
            player.save()

        for player in Player.objects.all():
            player.gb = (leader.wins + leader.fwins + player.losses + player.flosses -
                         leader.losses - leader.flosses - player.wins - player.fwins)/2
            player.save()


class Player(models.Model):
    name = models.TextField()
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    ties = models.PositiveSmallIntegerField(default=0)
    fwins = models.PositiveSmallIntegerField(default=0)
    flosses = models.PositiveSmallIntegerField(default=0)
    fties = models.PositiveSmallIntegerField(default=0)
    gb = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    cell = models.TextField(default='+18142031414')
    objects = PlayerManager()

    def __str__(self):
        return self.name


class SelectionManager(models.Manager):
    def generate_db_selections(self, player):
        for game in Game.objects.all():
            self.model.objects.create(game=game, player=player)

    def add_to_email_backup(self, player, picks):
        message = player.name + '\n' + \
            '\n'.join(str(pick.game) + ': ' + str(pick.prediction)
                      for pick in picks) + '\n'
        if os.path.exists('email_backup.pl'):
            with open('email_backup.pl', 'rb') as f:
                message = message + pickle.load(f)

        with open('email_backup.pl', 'wb') as f:
            pickle.dump(message, f)

    def update_selections_from_pl(self):
        with open('manualpicks.pl', 'rb') as f:
            picks = pickle.load(f)
        for username, home_team, away_team, prediction in picks:
            self.update_selection_manually(
                username, home_team, away_team, prediction)
        os.remove('manualpicks.pl')

    def update_selection_manually(self, username, home_team_name, away_team_name, team_predicted_name):
        player = Player.objects.get(name=username)
        game = Game.objects.get(home_team__name=home_team_name,
                                away_team__name=away_team_name)
        selection = self.model.objects.get(player=player, game=game)
        team_predicted = Team.objects.get(name=team_predicted_name)
        selection.prediction = team_predicted
        selection.save()

    def update_selection_statuses(self):
        for game in Game.objects.all():
            winner = game.get_game_winner()
            for player in Player.objects.all():
                selection = self.model.objects.get(player=player, game=game)
                if winner == None:
                    pass
                elif winner == selection.prediction:
                    selection.success = 1
                elif selection.prediction == None:
                    selection.success = 4
                elif winner == 'TIE':
                    selection.success = 3
                else:
                    selection.success = 2
                selection.save()
        missed_games = self.model.objects.build_missed_games_dict()
        for week_no in range(1, 18):
            for player in Player.objects.all():
                if player.name in missed_games.keys() and week_no in missed_games[player.name].keys():
                    worst_record = self.model.objects.get_worst_record_for_game_set(
                        missed_games[player.name][week_no])
                    for game in missed_games[player.name][week_no]:
                        selection = self.model.objects.get(
                            player=player, game=game)
                        if worst_record[0] > 0:
                            worst_record[0] -= 1
                            selection.success = 5
                        elif worst_record[1] > 0:
                            worst_record[1] -= 1
                            selection.success = 6
                        elif worst_record[2] > 0:
                            worst_record[2] -= 1
                            selection.success = 7
                        selection.save()

    def build_missed_games_dict(self):
        missed_games = {}
        for selection in self.model.objects.all():
            if selection.game.gametime + timedelta(hours = 15) < utils.get_current_datetime():
                if selection.prediction == None:
                    if selection.player.name not in missed_games.keys():
                        missed_games[selection.player.name] = {}
                    if selection.game.week_no not in missed_games[selection.player.name].keys():
                        missed_games[selection.player.name][selection.game.week_no] = [
                        ]
                    missed_games[selection.player.name][selection.game.week_no].append(
                        selection.game)
        return missed_games

    def get_worst_record_for_game_set(self, game_list):
        worst = False
        for player in Player.objects.all():
            record = [0, 0, 0]
            for game in game_list:
                selection = self.model.objects.get(game=game, player=player)
                if selection.success == 1:
                    record[0] += 1
                elif selection.success == 2:
                    record[1] += 1
                elif selection.success == 3:
                    record[2] += 1
            if sum(record) == len(game_list):
                if not worst:
                    worst = record
                if record[0] / (record[0] + record[1]) < worst[0] / (worst[0] + worst[1]):
                    worst = record
        return worst if worst else [0, 0, 0]


class Selection(models.Model):
    game = models.ForeignKey(Game, models.CASCADE, null=False, blank=False)
    player = models.ForeignKey(Player, models.CASCADE)
    prediction = models.ForeignKey(Team, models.CASCADE, null=True, blank=True)
    success = models.PositiveSmallIntegerField(
        default=0)  # 0:NA, 1:W, 2:L, 3:T 4:forgot 5:fwin 6:floss 7: ftie
    objects = SelectionManager()

class WeekRecord(models.Model):
    player = models.ForeignKey(Player, models.CASCADE)
    year = models.PositiveIntegerField(default = 2019)
    wins = models.PositiveSmallIntegerField(default = 0)
    losses = models.PositiveSmallIntegerField(default = 0)
    ties = models.PositiveSmallIntegerField(default = 0)
    week_no = models.PositiveSmallIntegerField()

class TeamRecord(models.Model):
    timeframe = models.TextField(choices = [('C','Career'),('Y','Year')])
    player = models.ForeignKey(Player, models.CASCADE)
    team = models.ForeignKey(Team, models.CASCADE)
    wins = models.PositiveSmallIntegerField(default = 0)
    losses = models.PositiveSmallIntegerField(default = 0)
    ties = models.PositiveSmallIntegerField(default = 0)



