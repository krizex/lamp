import requests
from collections import namedtuple
from lamp.utils.util import parallel_apply, constructor_of
from lamp.app.controllers.base import ObjectBaseUnit


class TrendCandidate(ObjectBaseUnit):
    def __init__(self, name, code, benefit, ops):
        super(TrendCandidate, self).__init__(name, code, 0)
        self.benefit_rate = benefit
        self.ops = ops

    @property
    def last_n_days_date(self):
        ret = self.get_last_n_days_date(22)
        return ret

    @property
    def last_n_days_price(self):
        return self.get_last_n_days_price(22)


def get_trend_candidate():
    resp = requests.get('http://lamp-lbt:8000')
    js = resp.json()
    timestamp = js.get('timestamp', 'NA')
    duration = js.get('duration', 0)
    duration = int(duration)
    stocks = js.get('data', [])
    recs = []

    def build(x):
        (code, name, benefit, ops) = x
        return TrendCandidate(code, name, benefit, ops)

    recs = parallel_apply(stocks, build)
    recs.sort(key=lambda s: s.benefit_rate, reverse=True)

    return timestamp, duration, recs

