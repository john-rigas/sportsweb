from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from nfl.models import Player, Selection, Team, Game, WeekRecord, TeamRecord
from nfl.utils import get_current_datetime, get_current_week
from nfl.forms import SelectionFormset
import time
from django.http import HttpResponseRedirect
from sportsweb.users import create_user, change_user_password
from collections import OrderedDict
import os.path
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from copy import deepcopy
from datetime import timedelta


def home_page(request):
    """Render the home page with a sign-in form."""

    if not Team.objects.all():
        Team.objects.load_teams_to_db()
        Game.objects.load_schedule_to_db_from_pl()
        Team.objects.add_abbreviations_to_teams()
    if not Player.objects.all():
        Player.objects.create_family_players()
    if os.path.exists('manualpicks.pl'):
        Selection.objects.update_selections_from_pl()
    if 'user' in request.session.keys():
        weekno = get_current_week()
        username = request.session['user']
        return redirect(f'/{username}/nfl/{weekno}')
    return render(request, 'home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
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


def nfl_page(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.username == user:
        return redirect('/accounts/logout')
    player = Player.objects.get(name=user)
    predictions = Selection.objects.filter(
        player=player).filter(game__week_no=weekno)
    formset = SelectionFormset(queryset=predictions)
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    weekgames = Game.objects.filter(week_no=weekno)
    weekstarted = any(_game.gametime < get_current_datetime()
                      for _game in weekgames)

    weekmenu = {}
    for wk in range(1,22):
        weekmenu[wk] = 'Week '+str(wk) if wk < 18 else 'Playoff '+str(wk-17)

    weekrecords = {_player.name: [0, 0, 0] for _player in standings}
    picks = []
    for _game in weekgames:
        next_game_picks = {}
        gamestarted = _game.gametime < get_current_datetime()
        for _player in standings:
            _selection = Selection.objects.get(player=_player, game=_game)
            if _selection.prediction is None:
                next_game_picks[_player] = ('N/A', None)
            else:
                next_game_picks[_player] = (
                    _selection.prediction.abbrv,
                    _selection.success
                )
                if _selection.success == 1:
                    weekrecords[_player.name][0] += 1
                elif _selection.success == 2:
                    weekrecords[_player.name][1] += 1
                elif _selection.success == 3:
                    weekrecords[_player.name][2] += 1

        picks.append((gamestarted, OrderedDict(sorted(next_game_picks.items(
        ), key=lambda x: -(x[0].wins + x[0].fwins))), f"{_game.away_team.abbrv} at {_game.home_team.abbrv}"))

    return render(request, 'nfl.html', {'player': player,
                                        'formset': formset,
                                        'standings': standings,
                                        'weekno': weekno,
                                        'weekmenu': weekmenu,
                                        'picks': picks,
                                        'weekgames': weekgames,
                                        'weekstarted': weekstarted,
                                        'weekrecords': weekrecords})

def nfl_standings(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect('/')
    player = Player.objects.get(name=user)
    predictions = Selection.objects.filter(
        player=player).filter(game__week_no=weekno)
    formset = SelectionFormset(queryset=predictions)
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    weekgames = Game.objects.filter(week_no=weekno)
    weekstarted = any(_game.gametime < get_current_datetime()
                      for _game in weekgames)
    cur_year = cur_year = (get_current_datetime() - timedelta(days = 100)).year

    weekmenu = {}
    for wk in range(1,22):
        weekmenu[wk] = 'Week '+str(wk) if wk < 18 else 'Playoff '+str(wk-17)

    weekrecords = {_player.name: [0, 0, 0] for _player in standings}
    picks = []
    for _game in weekgames:
        next_game_picks = {}
        gamestarted = _game.gametime < get_current_datetime()
        for _player in standings:
            _selection = Selection.objects.get(player=_player, game=_game)
            if _selection.prediction is None:
                next_game_picks[_player] = ('N/A', None)
            else:
                next_game_picks[_player] = (
                    _selection.prediction.abbrv,
                    _selection.success
                )
                if _selection.success == 1:
                    weekrecords[_player.name][0] += 1
                elif _selection.success == 2:
                    weekrecords[_player.name][1] += 1
                elif _selection.success == 3:
                    weekrecords[_player.name][2] += 1

        picks.append((gamestarted, OrderedDict(sorted(next_game_picks.items(
        ), key=lambda x: -(x[0].wins + x[0].fwins))), f"{_game.away_team.abbrv} at {_game.home_team.abbrv}"))

    return render(request, 'standings.html', {'player': player,
                                        'formset': formset,
                                        'standings': standings,
                                        'weekno': weekno,
                                        'weekmenu': weekmenu,
                                        'picks': picks,
                                        'weekgames': weekgames,
                                        'weekstarted': weekstarted,
                                        'weekrecords': weekrecords,
                                        'year':cur_year})

def nfl_results(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect('/')
    player = Player.objects.get(name=user)
    predictions = Selection.objects.filter(
        player=player).filter(game__week_no=weekno)
    formset = SelectionFormset(queryset=predictions)
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    weekgames = Game.objects.filter(week_no=weekno)
    weekstarted = any(_game.gametime < get_current_datetime()
                      for _game in weekgames)
    weekmenu = {}
    for wk in range(1,22):
        weekmenu[wk] = 'Week '+str(wk) if wk < 18 else 'Playoff '+str(wk-17)

    weekrecords = {_player.name: [0, 0, 0] for _player in standings}
    picks = []
    for _game in weekgames:
        next_game_picks = {}
        gamestarted = _game.gametime < get_current_datetime()
        for _player in standings:
            _selection = Selection.objects.get(player=_player, game=_game)
            if _selection.prediction is None:
                next_game_picks[_player] = ('N/A', None)
            else:
                next_game_picks[_player] = (
                    _selection.prediction.abbrv,
                    _selection.success
                )
                if _selection.success == 1:
                    weekrecords[_player.name][0] += 1
                elif _selection.success == 2:
                    weekrecords[_player.name][1] += 1
                elif _selection.success == 3:
                    weekrecords[_player.name][2] += 1

        picks.append((gamestarted, OrderedDict(sorted(next_game_picks.items(
        ), key=lambda x: -(x[0].wins + x[0].fwins))), f"{_game.away_team.abbrv} at {_game.home_team.abbrv}"))

    return render(request, 'results.html', {'player': player,
                                        'formset': formset,
                                        'standings': standings,
                                        'weekno': weekno,
                                        'weekmenu': weekmenu,
                                        'picks': picks,
                                        'weekgames': weekgames,
                                        'weekstarted': weekstarted,
                                        'weekrecords': weekrecords})

def nfl_history(request, user):
    weekno = get_current_week()
    current_player = Player.objects.get(name=user)
    if not request.user.is_authenticated:
        return redirect('/')
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'history.html', {
        'standings':standings,
        'year_range':range(2019,2006,-1),
        'weekno': weekno,
        'player': current_player
        })

def nfl_history_regular(request, user):
    weekno = get_current_week()
    current_player = Player.objects.get(name=user)
    if not request.user.is_authenticated:
        return redirect('/')
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'regularhistory.html', {
        'standings':standings,
        'year_range':range(2019,2006,-1),
        'weekno': weekno,
        'player': current_player
        })

def nfl_history_playoffs(request, user):
    weekno = get_current_week()
    current_player = Player.objects.get(name=user)
    if not request.user.is_authenticated:
        return redirect('/')
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'playoffhistory.html', {
        'standings':standings,
        'year_range':range(2019,2006,-1),
        'weekno': weekno,
        'player': current_player
        })

def nfl_history_regular_year(request, user, year):
    weekno = get_current_week()
    weekyear = [(wk, year) for wk in range(17,0,-1)]
    current_player = Player.objects.get(name=user)
    if not request.user.is_authenticated:
        return redirect('/')
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'regularhistoryyear.html', {
        'standings':standings,
        'year_range':range(2019,2006,-1),
        'weekyear': weekyear,
        'player': current_player,
        'year':year,
        'weekno':weekno
        })

def nfl_history_playoffs_year(request, user, year):
    weekno = get_current_week()
    weekyear = [(wk, year) for wk in range(21,17,-1)]
    current_player = Player.objects.get(name=user)
    if not request.user.is_authenticated:
        return redirect('/')
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'playoffhistoryyear.html', {
        'standings':standings,
        'week_range':range(17,0,-1),
        'weekyear': weekyear,
        'player': current_player,
        'year': year,
        'weekno': weekno
        })

def nfl_history_year(request, user, year):
    weekno = get_current_week()
    weekyear = [(wk, year) for wk in range(21,0,-1)]
    current_player = Player.objects.get(name=user)
    if not request.user.is_authenticated:
        return redirect('/')
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'yearhistory.html', {
        'standings':standings,
        'week_range':range(17,0,-1),
        'player': current_player,
        'weekyear': weekyear,
        'year':year,
        'weekno':weekno
        })


def nfl_players(request, user):
    weekno = get_current_week()
    current_player = Player.objects.get(name=user)
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')
    return render(request, 'players.html', {
        'standings': standings,
        'player': current_player,
        'weekno': weekno
    })

def nfl_player(request, user, player):
    weekno = get_current_week()
    current_player = Player.objects.get(name=user)
    info_player = Player.objects.get(name=player)
    standings = Player.objects.extra(
        select={'total_wins': "wins + fwins"}).order_by('-total_wins')

    teams = Team.objects.all()
    records = {}
    for team in teams:
        year_record = TeamRecord.objects.get(timeframe = 'Y', player = info_player, team = team)
        year_rate = f"{year_record.wins/(year_record.wins+year_record.losses):.3f}" if year_record.losses else "1.000"
        career_record = TeamRecord.objects.get(timeframe = 'C', player = info_player, team = team)
        career_rate = f"{(year_record.wins+career_record.wins)/(year_record.wins+career_record.wins+year_record.losses+career_record.losses):.3f}" if year_record.losses+career_record.losses else "1.000"
        records[team.name] = (year_record.wins, year_record.losses, year_record.ties, year_rate,
                             year_record.wins+career_record.wins, year_record.losses+career_record.losses, year_record.ties+career_record.ties, career_rate)
    return render(request, 'player.html', {
        'standings': standings,
        'player': current_player,
        'weekno': weekno,
        'records': records,
        'info_player': info_player
    })


def picks(request, user, weekno):
    if not request.user.is_authenticated:
        return redirect('/')
    player = Player.objects.get(name=user)
    formset = SelectionFormset(request.POST)
    if formset.is_valid():
        total_submitted = sum(1 for form in formset if form.cleaned_data.get('prediction') != None)
        total = len(formset)
        messages.success(request, f'Success: You have completed {total_submitted} of {total} picks')
        formset.save()  # need to make sure this is safe
    Selection.objects.add_to_email_backup(player, Selection.objects.filter(
        player=player, game__week_no=weekno))
    return redirect(f'/{player.name}/nfl/{weekno}/#picks')


def password(request, user):
    return render(request, 'password.html', {'username': user})


def change_password(request, user):
    pass_one = request.POST['password']
    pass_two = request.POST['confirmpass']
    if pass_one == pass_two:
        change_user_password(user, pass_one)
        return redirect('/accounts/logout')
    else:
        return render(request, 'password.html', {'username': user})


def user_password(request):
    username = request.POST['username']
    if username in [user.username for user in User.objects.all()]:
        return redirect(f'/{username}/password/')
    else:
        return redirect('/')


# def new_user(request):
#     weekno = get_current_week()
#     username = request.POST['username']
#     password = request.POST['password']
#     email = request.POST['email']
#     if username not in [player.name for player in Player.objects.all()]:
#         player = Player.objects.create(name=username)
#         Selection.objects.generate_db_selections(player)
#         user = create_user(username, email, password)
#     if user is not None and user.is_active:
#         login(request, user)
#         request.session['user'] = user.username
#         return redirect(f'/{username}/nfl/{weekno}')
#     else:
#         return redirect('/')
