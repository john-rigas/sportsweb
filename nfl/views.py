from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from nfl.models import Player, Selection, Team, Game, add_to_email_backup, add_abbreviations_to_teams, create_family_players, update_selections_from_pl, load_schedule_to_db_from_pl, load_teams_to_db, execute_regular_update, generate_db_selections, get_current_week
from nfl.forms import SelectionFormset
import time
from django.http import HttpResponseRedirect
from sportsweb.users import create_user, change_user_password
from collections import OrderedDict
import os.path


def home_page(request):
    if not Team.objects.all():
        load_teams_to_db() #should elim from regular website load
        load_schedule_to_db_from_pl() # same as above
        add_abbreviations_to_teams()
    if not Player.objects.all():
        create_family_players()
    if os.path.exists('manualpicks.pl'):
        update_selections_from_pl()
    #execute_regular_update() #same
    if 'user' in request.session.keys():
        weekno = get_current_week()
        username = request.session['user']
        return redirect(f'/{username}/nfl/{weekno}')
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None and user.is_active:
            login(request, user)
            weekno = get_current_week()
            request.session['user'] = user.username
            return redirect(f'/{username}/nfl/{weekno}')
        else:
            return redirect('/')
    else:
        return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')


def new_user(request):
    weekno = get_current_week()
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    if username not in [player.name for player in Player.objects.all()]:
        player = Player.objects.create(name = username)
        generate_db_selections(player) #same as above
        user = create_user(username, email, password)
    if user is not None and user.is_active:    
        login(request, user)
        request.session['user'] = user.username
        return redirect(f'/{username}/nfl/{weekno}')
    else:
        return redirect('/')


def nfl_page(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/')
    player = Player.objects.get(name = user)
    predictions = Selection.objects.filter(player = player).filter(game__week_no = weekno)   
    formset = SelectionFormset(queryset = predictions)
    standings = Player.objects.all().order_by('-wins')
    weekgames = Game.objects.filter(week_no = weekno)
    picks = [{_player.name:(Selection.objects.get(player=_player, game=_game).prediction.abbrv
                           if Selection.objects.get(player=_player, game=_game).prediction is not None
                           else 'N/A') 
                           for _player in standings} for _game in weekgames]
    return render(request, 'nfl.html', {'player': player, 
                                        'formset': formset, 
                                        'standings': standings,
                                        'weekno': weekno,
                                        'range': range(1,18),
                                        'picks': picks,
                                        'weekgames': weekgames})

def picks(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/')
    player = Player.objects.get(name = user)
    formset = SelectionFormset(request.POST)
    add_to_email_backup(player, Selection.objects.filter(player = player, game__week_no = weekno))
    if formset.is_valid():
        formset.save() # need to make sure this is safe
    return redirect(f'/{player.name}/nfl/{weekno}/')

def change_password(request, user):
    change_user_password(user, request.POST['newpassword'])
    logout(request)
    return redirect('/')
