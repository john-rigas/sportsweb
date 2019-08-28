from django.shortcuts import render, redirect
from nfl.models import Player


def home_page(request):
    return render(request, 'home.html')

def new_user(request):
    player = Player.objects.create()
    return redirect(f'/{player.id}/nfl')

def nfl_page(request, player_id):
    player = Player.objects.get(id=player_id)
    return render(request, 'nfl.html', {'player': player})

def picks(request):
    return render(request, 'nfl.html')