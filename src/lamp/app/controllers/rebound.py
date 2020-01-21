from lamp.model import Rebound
from lamp.log import log
from lamp.utils.util import parallel_apply, constructor_of
from lamp.app.controllers.base import ObjectBaseUnit
import traceback


class ReboundUnit(ObjectBaseUnit):
    def __init__(self, rebound):
        super(ReboundUnit, self).__init__(rebound.code, rebound.name, 0, rebound.note)
        self.days = rebound.days
        self.ratio = rebound.ratio

    def lowest_price(self):
        return self.trend_low_ndays(self.days)

    def rebound_price(self):
        return self.lowest_price() * (1 + self.ratio)

    def calc_trend_position_of_cur_price(self):
        lowest = self.lowest_price()
        rebound = self.rebound_price()
        return (self.cur_price - lowest) / 1.0 / (rebound - lowest)


def get_rebounds():
    records = Rebound.query.all()
    def build(x):
        return constructor_of(ReboundUnit)(x)

    records = parallel_apply(records, build)
    records = sorted(records)

    return records

def get_records():
    return Rebound.query.all()
