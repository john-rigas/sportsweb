import pickle
from django.core.mail import send_mail
import os
import django
import subprocess
from sportsweb import settings
from nfl import models
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

reminder_schedule = {}

gamekey = 0
for game in models.Game.objects.filter(week_no = models.get_current_week()):
    if not game.gametime in reminder_schedule.keys():
        reminder_schedule[(gamekey, game.gametime)] = []
        gamekey += 1
    reminder_schedule[game.gametime].append(game)

with open('this_weeks_reminders.pl','wb') as f:
    pickle.dump(reminder_schedule, f)

for (gamekey, gametime), game_set in reminder_schedule.items():
    sendtime1 = gametime - timedelta(days=1)
    sendtime2 = gametime - timedelta(minutes=15)
    subprocess.run(f'echo "{sendtime1.minute} {sendtime1.hour} {sendtime1.day} {sendtime1.month} * cd ~/sites/fredandfred.tk && ./virtualenv/bin/python send_reminder_email.py --time 0 --gamekey {gamekey}" >> /tmp/crondump')
    subprocess.run(f'echo "{sendtime2.minute} {sendtime2.hour} {sendtime2.day} {sendtime2.month} * cd ~/sites/fredandfred.tk && ./virtualenv/bin/python send_reminder_email.py --time 1 --gamekey {gamekey}" >> /tmp/crondump')