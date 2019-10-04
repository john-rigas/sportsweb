from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def create_user(username, email, password):
    new_user = User.objects.create_user(username, email, password)
    new_user.save()
    return new_user


def change_user_password(username, new_password):
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
