import os
import django
import argparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from nfl import models

job_dict = {
    'r': models.load_results_to_db_from_pl,
    'p': models.update_player_records,
    't': models.update_team_records
}

parser = argparse.ArgumentParser(description='run cronjobs')
parser.add_argument('jobs', default = job_dict.keys())
args = parser.parse_args()

for key in args.jobs:
    job_dict[key]()