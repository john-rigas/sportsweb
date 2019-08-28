from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.TextField()

class Game(models.Model):
    home_team = models.ForeignKey(Team, models.CASCADE, related_name = 'home_team')
    away_team = models.ForeignKey(Team, models.CASCADE, related_name = 'away_team')
    home_score = models.PositiveSmallIntegerField()
    week_no = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

class Player(models.Model):
    name = models.TextField()

class Selection(models.Model):
    game = models.ForeignKey(Game, models.CASCADE)
    player = models.ForeignKey(Player, models.CASCADE)
    prediction = models.ForeignKey(Team, models.CASCADE)