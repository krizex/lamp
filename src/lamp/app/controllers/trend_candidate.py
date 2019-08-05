import requests
from collections import namedtuple
from lamp.utils.util import parallel_apply, constructor_of
from lamp.app.controllers.base import ObjectBaseUnit
from lamp.utils.util import timeit


class TrendCandidate(ObjectBaseUnit):
    TYPE = 'TrendCandidate'

    def __init__(self, name, code, benefit, ops):
        super(TrendCandidate, self).__init__(name, code, 0)
        self.benefit_rate = benefit
        self.ops = ops

    @property
    def last_n_days_date(self):
        return self.get_last_n_days_date(22)

    @property
    def last_n_days_price(self):
        return self.get_last_n_days_price(22)

    @property
    def last_n_days_vol(self):
        return self.get_last_n_days_vol(22)


@timeit('trend_candidate')
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

