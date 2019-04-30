import requests
from collections import namedtuple

Unit = namedtuple('Unit', ['code', 'name', 'benefit_rate', 'ops'])



def get_trend_candidate():
    resp = requests.get('http://lamp-lbt:8000')
    js = resp.json()
    timestamp = js.get('timestamp', 'NA')
    duration = js.get('duration', 0)
    duration = int(duration)
    stocks = js.get('data', [])
    recs = []
    for stock in stocks:
        (code, name, benefit, ops) = stock
        rec = Unit(code, name, benefit, ops)
        recs.append(rec)

    return timestamp, duration, recs

