import datetime


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
    return ruler


if __name__ == '__main__':
    ruler = calc_ruler(40.8, 28.3, 10)
    print 'Ruler:'
    for i, r in enumerate(ruler):
        print '%2d:    %.3f' % (i, r)
