import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()
from sportsweb import settings
from nfl import models, utils

for person in utils.people:
    player = models.Player.objects.get(name=person[2])
    player.cell = person[3]
    player.save()
