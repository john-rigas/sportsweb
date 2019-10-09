from django import template
from nfl.models import WeekRecord, Player, Selection
from django.db.models import Sum
from nfl.utils import get_current_datetime
from datetime import timedelta

register = template.Library()

@register.filter
def week_or_playoff(weekno):
    if weekno <= 17:
        wk_string = f"Week {weekno}"
    else:
        wk_string = f"Playoff {weekno - 17}"
    return wk_string

@register.filter
def calc_yearrecord(playername, year):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_year_record(player, year)
    return _format_record(wins, losses, ties)

@register.filter
def calc_yearrecord_reg(playername, year):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_year_record(player, year, "regular")
    return _format_record(wins, losses, ties)

@register.filter
def calc_yearrecord_playoff(playername, year):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_year_record(player, year, "playoffs")
    return _format_record(wins, losses, ties)

@register.filter
def calc_weekrecord(playername, week_year):
    week, year = week_year
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_week_record(player, year, week)
    return _format_record(wins, losses, ties)

@register.filter
def calc_totalrecord(playername, portion="full"):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_total_record(player, portion)
    return _format_record(wins, losses, ties, show_ties = False)

@register.filter
def calc_careerpercent(playername, portion="full"):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_total_record(player, portion)
    return f"{wins/(wins+losses):.3f}"[1:]

@register.filter
def calc_yearpercent(playername, year):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_year_record(player, year)
    if losses:
        rate_string = f"{wins/(wins+losses):.3f}"[1:]
    else:
        rate_string = ""
    return rate_string

@register.filter
def calc_yearpercent_reg(playername, year):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_year_record(player, year, "regular")
    if losses:
        rate_string = f"{wins/(wins+losses):.3f}"[1:]
    else:
        rate_string = ""
    return rate_string

@register.filter
def calc_yearpercent_playoff(playername, year):
    player = Player.objects.get(name=playername)
    wins, losses, ties = _sum_year_record(player, year, "playoffs")
    if losses:
        rate_string = f"{wins/(wins+losses):.3f}"[1:]
    else:
        rate_string = ""
    return rate_string

@register.filter
def calc_championships(standings, portion="full"):
    cur_year = (get_current_datetime() - timedelta(days = 100)).year
    championships = [0 for player in standings]
    all_ties = False
    for year in range(2005, cur_year):
        year_ties = False
        best = None
        for idx,player in enumerate(standings):
            wins, losses, ties = _sum_year_record(player, year, portion)
            if losses != 0:
                if not best:
                    best = (wins, losses, ties)
                    leaders = [idx]
                else:
                    if best[0]/(best[0]+best[1]) <= wins/(wins+losses):
                        if best[0]/(best[0]+best[1]) == wins/(wins+losses):
                            leaders.append(idx)
                        else: 
                            leaders = [idx]
                        best = (wins, losses, ties)

        if len(leaders) > 1:
            year_ties = True
            all_ties = True

        for leader in leaders:
            if year_ties:
                championships[leader] += 1/len(leaders)
            else:
                championships[leader] += 1

    if all_ties:
        championships = [f"{champ:.2f}" for champ in championships]

    return championships

    return 0

def _calc_previous_year_record(player, year, portion="full"):
    if portion == "full":
        wins = WeekRecord.objects.filter(player=player, year=year).aggregate(Sum('wins'))['wins__sum']
        losses = WeekRecord.objects.filter(player=player, year=year).aggregate(Sum('losses'))['losses__sum']
        ties = WeekRecord.objects.filter(player=player, year=year).aggregate(Sum('ties'))['ties__sum']
    elif portion == "regular":
        wins = WeekRecord.objects.filter(player=player, year=year, week_no__lte=17).aggregate(Sum('wins'))['wins__sum']
        losses = WeekRecord.objects.filter(player=player, year=year, week_no__lte=17).aggregate(Sum('losses'))['losses__sum']
        ties = WeekRecord.objects.filter(player=player, year=year, week_no__lte=17).aggregate(Sum('ties'))['ties__sum']
    elif portion == "playoffs":
        wins = WeekRecord.objects.filter(player=player, year=year, week_no__gte=18).aggregate(Sum('wins'))['wins__sum']
        losses = WeekRecord.objects.filter(player=player, year=year, week_no__gte=18).aggregate(Sum('losses'))['losses__sum']
        ties = WeekRecord.objects.filter(player=player, year=year, week_no__gte=18).aggregate(Sum('ties'))['ties__sum']
    return wins, losses, ties

def _calc_current_year_record(player, year, portion="full"): # need to implement correctly
    if portion == "full":
        wins = player.wins + player.fwins
        losses = player.losses + player.flosses
        ties = player.ties + player.fties
    elif portion == "regular":
        wins = player.wins + player.fwins
        losses = player.losses + player.flosses
        ties = player.ties + player.fties
    elif portion == "playoffs":
        wins = 0
        losses = 0
        ties = 0
    return wins, losses, ties

def _replace_none_record(wins, losses, ties):
    ties = ties if ties else 0
    wins = wins if wins else 0
    losses = losses if losses else 0
    return wins, losses, ties

def _format_record(wins, losses, ties, show_ties = True):
    if ties and show_ties:
        rec_string = f"{wins}-{losses}-{ties}"
    else:
        rec_string = f"{wins}-{losses}"
    return rec_string

def _sum_total_record(player, portion="full"):
    cur_year = (get_current_datetime() - timedelta(days = 100)).year
    wins, losses, ties = _calc_current_year_record(player, cur_year, portion)
    total_wins, total_losses, total_ties = _replace_none_record(wins, losses, ties)
    for year in range(cur_year - 1, 2004, -1):
        wins, losses, ties = _calc_previous_year_record(player, year, portion)
        wins, losses, ties = _replace_none_record(wins, losses, ties)
        total_wins += wins
        total_losses += losses
        total_ties += ties
    return total_wins, total_losses, total_ties

def _sum_year_record(player, year, portion="full"):
    cur_year = (get_current_datetime() - timedelta(days = 100)).year
    if cur_year > year:
        wins, losses, ties = _calc_previous_year_record(player, year, portion)
    elif cur_year == year:
        wins, losses, ties = _calc_current_year_record(player, year, portion)
    wins, losses, ties = _replace_none_record(wins, losses, ties)
    return wins, losses, ties

def _sum_week_record(player, year, week):
    cur_year = (get_current_datetime() - timedelta(days = 100)).year
    if WeekRecord.objects.filter(player=player, year=year, week_no=week):
        if cur_year > year:
            wins = WeekRecord.objects.get(player=player, year=year, week_no=week).wins
            losses = WeekRecord.objects.get(player=player, year=year, week_no=week).losses
            ties = WeekRecord.objects.get(player=player, year=year, week_no=week).ties
        elif cur_year == year:
            wins = 0
            losses = 0
            ties = 0
            selections = Selection.objects.filter(player=player, game__week_no = week)
            for selection in selections:
                if selection.success == 1 or selection.success == 5:
                    wins += 1
                elif selection.success == 2 or selection.success == 6:
                    losses += 1
                elif selection.success == 3 or selection.success == 7:
                    ties += 1       
        wins, losses, ties = _replace_none_record(wins, losses, ties)
    else:
        wins, losses, ties = (0,0,0)
    return wins, losses, ties
