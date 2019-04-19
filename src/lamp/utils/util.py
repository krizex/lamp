import datetime
from lamp.log import log


def ndays_before_today(n):
    now = datetime.datetime.now()
    d = now - datetime.timedelta(days=n)
    return d


def calc_ruler(high, low, size):
    ruler = []
    rate = (1.0 * high / low) ** (1.0 / size) - 1
    cur = low / (1.0 + rate)
    for _ in range(size + 1):
        cur *= (1.0 + rate)
        ruler.append(cur)

    # The ruler has an additional grid, that means the first buy point is ruler[1]
    ruler = ruler[::-1]
    return ruler, rate


def parallel_apply(recs, f):
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(8)
    rets = pool.map(f, recs)
    pool.close()
    pool.join()
    # reject the unit which processed failed
    return [x for x in rets if x is not None]

def constructor_of(unit_cls):
    def builder(code):
        try:
            return unit_cls(code)
        except:
            log.exception('Fail to process %s', code)
            return None

    return builder
