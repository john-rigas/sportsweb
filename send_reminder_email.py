import pickle
from django.core.mail import send_mail
import os
import django
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from sportsweb import settings
from nfl import models
from datetime import timedelta
import argparse
from django.contrib.auth.models import User

parser = argparse.ArgumentParser(description='send_reminder_email')
parser.add_argument('--time', type = int)
parser.add_argument('--gamekey', type = int)
args = parser.parse_args()

with open('this_weeks_reminders.pl','rb') as f:
    reminder_schedule = pickle.load(f)

weekno = models.get_current_week()
time_remaining = '3 hours' if args.time == 0 else '15 minutes'

for (gamekey, gametime), gameset in reminder_schedule.items():

    if gamekey == args.gamekey:

        for player in models.Player.objects.all():
            user = User.objects.get(username = player.name)

            if any(selection.prediction == None for selection in models.Selection.objects.filter(player = player, game__week_no = weekno)):
                
                message = f'There are games starting in {time_remaining} that you have not picked.  Please go to fredandfred.tk to make your picks.'

                send_mail('You are running out of time to make your nfl picks',
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          ['fredandfredandfredandfred@gmail.com'], # SHOULD BE: user.email
                          fail_silently=False)