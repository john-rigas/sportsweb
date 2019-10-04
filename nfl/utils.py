from datetime import datetime
import pytz

people = [
    ('Uncle Mike', 'michael.rigas@zitomedia.com', 'unclemike', '+18145948337'),
    ('Jenkins', 'james.rigas@zitomedia.com', 'jenkins', '+18143315911'),
    ('Doc', 'maryannrigas@gmail.com', 'doc', '+18143315912'),
    ('Andrew', 'andrewjrigas@gmail.com', 'andrew', '+18142038320'),
    ('Chris', 'chris.rigas22@gmail.com', 'chris', '+18142033357'),
    ('Papou', 'john.rigas@zitomedia.com', 'papou', '+18142035866'),
    ('John Michael', 'jmrigas@gmail.com', 'johnny', '+18142031414'),
    ('D-Train', 'dtrain.rigas@gmail.com', 'david', '+18145948338'),
    ('Uncle Tim', 'timothy.rigas@zitomedia.com', 'uncletim', '+18146556443')
]


def get_current_datetime():
    return datetime.now(pytz.timezone('US/Eastern')).replace(
        tzinfo=None,
        second=0,
        microsecond=0)


def get_current_week():
    current_datetime = get_current_datetime()
    week_one_start = datetime(2019, 9, 3, 0, 0)
    days_since_opener = (current_datetime - week_one_start).days
    current_week = 1 + (days_since_opener // 7) if days_since_opener > 0 else 1
    return current_week
