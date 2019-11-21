import pickle
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
import calendar
from datetime import datetime, timedelta
import pytz
from nfl.utils import get_current_week

MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}


def get_current_datetime():
    return datetime.now(pytz.timezone('US/Eastern')).replace(
        tzinfo=None,
        second=0,
        microsecond=0)


def hours_to_military_time(hour, am_pm):
    if hour == 12:
        hour = 0
    if am_pm == 'PM':
        hour += 12
    return hour


def date_and_time_to_datetime(date, time):
    month, day = date.split()
    am_pm = time[-2:]
    time_number = time[:-2]
    hour, mins = time_number.split(':')
    month_num = MONTHS[month]
    return datetime(2019,
                    month_num,
                    int(day),
                    hours_to_military_time(int(hour), am_pm),
                    int(mins))


def load_nfl_scores_page():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get('https://www.pro-football-reference.com/years/2019/games.htm')
    page_source = browser.page_source
    browser.quit()
    return page_source


def get_schedule_from_html(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    games = soup.find_all('tr')
    schedule = {week: [] for week in range(1, 18)}
    for game in games:
        week_no = game.find('th', {'data-stat': 'week_num',
                                   'scope': 'row'})
        if week_no and 'Pre' not in week_no.get_text():
            date = game.find(
                'td', {'data-stat': 'boxscore_word'}).find('a').get_text()
            time = game.find('td', {'data-stat': 'gametime'}).get_text()
            gametime = date_and_time_to_datetime(date, time)
            week_no = week_no.get_text()
            home_team = game.find(
                'td', {'data-stat': 'home_team'}).find('a').get_text()
            away_team = game.find(
                'td', {'data-stat': 'visitor_team'}).find('a').get_text()

            schedule[int(week_no)].append({
                'home_team': home_team,
                'away_team': away_team,
                'home_score': '',
                'away_score': '',
                'gametime': gametime
            })
    return schedule


def get_results_from_html(page_source):

    soup = BeautifulSoup(page_source, 'html.parser')
    games = soup.find_all('tr')
    games_to_update = {}

    for game in games:
        week_no = game.find('th', {'data-stat': 'week_num',
                                   'scope': 'row'})
        if week_no and 'Pre' not in week_no.get_text() and int(week_no.get_text()) <= get_current_week():
            date = game.find('td', {'data-stat': 'game_date'}).get_text()
            time = game.find('td', {'data-stat': 'gametime'}).get_text()
            gametime = date_and_time_to_datetime(date, time)
            week_no = int(week_no.get_text())

            if gametime + timedelta(hours=4) < get_current_datetime():
                winning_team = game.find(
                    'td', {'data-stat': 'winner'}).find('a').get_text()
                losing_team = game.find(
                    'td', {'data-stat': 'loser'}).find('a').get_text()
                if game.find('td', {'data-stat': 'pts_win'}).find('strong'):
                    winning_score = game.find(
                        'td', {'data-stat': 'pts_win'}).find('strong').get_text()
                else:
                    winning_score = game.find(
                        'td', {'data-stat': 'pts_win'}).get_text()
                losing_score = game.find(
                    'td', {'data-stat': 'pts_lose'}).get_text()

                if week_no not in games_to_update.keys():
                    games_to_update[week_no] = []

                games_to_update[week_no].append({
                    'winning_team': winning_team,
                    'losing_team': losing_team,
                    'winning_score': winning_score,
                    'losing_score': losing_score,
                    'gametime': gametime
                })

    return games_to_update


if __name__ == '__main__':
    page_source = load_nfl_scores_page()
    #schedule = get_schedule_from_html(page_source)
    # with open('saved_schedule.pl','wb') as f:
    #    pickle.dump(schedule, f)
    results = get_results_from_html(page_source)
    with open('saved_results.pl', 'wb') as f:
        pickle.dump(results, f)
