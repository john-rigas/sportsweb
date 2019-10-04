import os
import django
import argparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from nfl import models

job_dict = {
    'r': models.Game.objects.load_results_to_db_from_pl,
    's': models.Selection.objects.update_selection_statuses,
    'p': models.Player.objects.update_player_records,
    't': models.Team.objects.update_team_records
}

parser = argparse.ArgumentParser(description='run cronjobs')
parser.add_argument('--jobs', nargs='?', default=job_dict.keys())
args = parser.parse_args()

for key in args.jobs:
    job_dict[key]()
