import pickle
from django.core.mail import send_mail
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from sportsweb import settings

