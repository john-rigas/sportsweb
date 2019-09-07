from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from nfl.models import Player, Selection, Team, Game, get_players_record, load_schedule_to_db_from_pl, load_teams_to_db, load_results_to_db_from_pl, generate_db_selections, get_current_week
from nfl.forms import SelectionFormset
import time
from django.http import HttpResponseRedirect
from sportsweb.users import create_user


def home_page(request):
    if not Team.objects.all():
        load_teams_to_db() #should elim from regular website load
        load_schedule_to_db_from_pl() # same as above
    load_results_to_db_from_pl()
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

def logout_user(request):
    logout(request)
    return redirect(f'/accounts/login/')


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
    standings = {player.name:get_players_record(player) for player in Player.objects.all()} #should cache these
    return render(request, 'nfl.html', {'player': player, 
                                        'formset': formset, 
                                        'standings': standings,
                                        'weekno': weekno,
                                        'range': range(1,18)})

def picks(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/')
    player = Player.objects.get(name = user)
    formset = SelectionFormset(request.POST)
    formset.save() # need to make sure this is safe
    return redirect(f'/{player.name}/nfl/{weekno}/')
