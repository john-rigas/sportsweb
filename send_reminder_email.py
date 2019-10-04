from django.contrib.auth.models import User
import argparse
from datetime import timedelta
from nfl import models
from sportsweb import settings
import pickle
from django.core.mail import send_mail
import os
import django
import subprocess
from utils import get_current_week
from twilio.rest import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()


parser = argparse.ArgumentParser(description='send_reminder_email')
parser.add_argument('--time', type=int)
parser.add_argument('--gamekey', type=int)
args = parser.parse_args()

with open('../../twilio/phone.pl','rb') as f:
    phone = pickle.load(f)

with open('this_weeks_reminders.pl', 'rb') as f:
    reminder_schedule = pickle.load(f)

weekno = get_current_week()
time_remaining = '3 hours' if args.time == 0 else '15 minutes'

for (gamekey, gametime), gameset in reminder_schedule.items():

    if gamekey == args.gamekey:

        for player in models.Player.objects.all():

            user = User.objects.get(username=player.name)

            if any(selection.prediction == None for selection in models.Selection.objects.filter(player=player, game__gametime=gametime)):

                message = f'Dear {player.name}, \n\nThere are games starting in {time_remaining} that you have not picked.  Please go to fredandfred.tk to make your picks.'

                # if player.name in ['andrew', 'david', 'johnny', 'unclemike', 'uncletim', 'papou', 'doc']:
                if player.name == 'johnny':
                    send_mail('You are running out of time to make your nfl picks',
                              message,
                              settings.DEFAULT_FROM_EMAIL,
                              [user.email],
                              fail_silently=False)

                # if player.name in ['chris', 'johnny']:
                if player.name == 'johnny':
                    twilioCli = Client(phone['account'], phone['token'])
                    text_message = twilioCli.messages.create(
                        body=message, from_=phone['number'], to=player.cell)
