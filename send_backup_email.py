import pickle
from django.core.mail import send_mail
import os
import django
from sportsweb import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

with open('email_backup.pl','rb') as f:
    message = pickle.load(f)

send_mail('Picks backup',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False)

os.remove('email_backup.pl')

