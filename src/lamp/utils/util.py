import datetime


def ndays_before_today(n):
    now = datetime.datetime.now()
    d = now - datetime.timedelta(days=n)
    return d
