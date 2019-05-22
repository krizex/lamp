import requests
from collections import namedtuple
from lamp.utils.util import parallel_apply, constructor_of
from lamp.app.controllers.base import ObjectBaseUnit

class Underestimate(ObjectBaseUnit):
    TYPE = 'Underestimate'

    def __init__(self, name, code, pos):
        super(Underestimate, self).__init__(name, code, 0)
        self.pos = pos

    @property
    def last_n_days_date(self):
        return self.get_last_n_days_date(22)

    @property
    def last_n_days_price(self):
        return self.get_last_n_days_price(22)

    @property
    def last_n_days_vol(self):
        return self.get_last_n_days_vol(22)


def get_underestimate():
    resp = requests.get('http://lamp-lbt:8000')
    js = resp.json()
    stocks = js.get('underestimate_chances', [])
    recs = []

    def build(x):
        (code, name, pos) = x
        return Underestimate(code, name, pos)

    recs = parallel_apply(stocks, build)
    recs.sort(key=lambda s: s.pos)

    return recs
