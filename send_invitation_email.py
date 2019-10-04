import pickle
from django.core.mail import send_mail
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsweb.settings")
django.setup()

from sportsweb import settings
from django.contrib.auth.models import User
from nfl import models

for user in User.objects.all():
    
    message_text = f'{user.username}, \n\nTo submit your NFL picks, please go to fredandfred.tk - your username is {user.username} and your password is {user.username}.  Make sure to hit the submit button when you are done.  If you have any trouble, let me know or just send me your picks.\n\nThanks, \nJohnny' 

    send_mail('NFL picks',
                message_text,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False)