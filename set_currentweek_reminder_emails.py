import pickle
from django.core.mail import send_mail
import os
import django
import subprocess
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from sportsweb import settings
from nfl import models, utils

reminder_schedule = {}

gamekey = 0
for game in models.Game.objects.filter(week_no = utils.get_current_week()):
    if all(game.gametime != t for k,t in reminder_schedule.keys()):
        reminder_schedule[(gamekey, game.gametime)] = []
        gamekey += 1
    reminder_schedule[(gamekey - 1, game.gametime)].append(game)

with open('this_weeks_reminders.pl','wb') as f: 
    pickle.dump(reminder_schedule, f)

if os.path.exists('/tmp/remindercrondump'):
    subprocess.run('rm /tmp/remindercrondump', shell=True)

subprocess.run('crontab -l > /tmp/remindercrondump', shell=True)

for (gamekey, gametime), game_set in reminder_schedule.items():
    sendtime1 = gametime - timedelta(hours=3)
    sendtime2 = gametime - timedelta(minutes=15)
    #if (gametime.weekday() > 0 and gametime.weekday() < 6) or gametime.hour == 13:     
    subprocess.run(f'echo "{sendtime1.minute} {sendtime1.hour} {sendtime1.day} {sendtime1.month} * cd ~/sites/fredandfred.tk && ./virtualenv/bin/python send_reminder_email.py --time 0 --gamekey {gamekey}" >> /tmp/remindercrondump', shell=True)
    subprocess.run(f'echo "{sendtime2.minute} {sendtime2.hour} {sendtime2.day} {sendtime2.month} * cd ~/sites/fredandfred.tk && ./virtualenv/bin/python send_reminder_email.py --time 1 --gamekey {gamekey}" >> /tmp/remindercrondump', shell=True)
    subprocess.run('crontab /tmp/remindercrondump', shell=True)