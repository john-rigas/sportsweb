import pickle
from django.core.mail import send_mail, EmailMessage
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from sportsweb import settings

with open('email_backup.pl','rb') as f:
    message_text = pickle.load(f)

message = EmailMessage('Picks backup',
                       message_text, 
                       settings.DEFAULT_FROM_EMAIL,
                       [settings.DEFAULT_FROM_EMAIL])

message.attach_file('db.sqlite3')
message.send(fail_silently=False)

os.remove('email_backup.pl')

