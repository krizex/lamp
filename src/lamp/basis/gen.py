# -*- coding: utf-8 -*-
from lamp.log import log
from lamp import config
import tushare as ts
import json
import os

def fetch_basis():
    for _ in range(10):
        try:
            log.info('Fetching stock basics...')
            pro = ts.pro_api('4105aca09e41fde2adac11ff8cdf7e05cef205d946e06935562e0010')
            ret = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            log.info('Fetched')
            df = ret[['ts_code', 'name']]
            df = df.set_index('ts_code')
            return df.to_json(orient='index')
        except:
            log.exception('Fetch stock basics fail, retrying...')

    raise RuntimeError('Fetch stock basics fail')


def main():
    filename = config.basis_persistent_file
    if os.path.isfile(filename):
        os.remove(filename)

    from lamp.utils.file.sf import SharedFile
    sf = SharedFile(filename)
    sf.exclusive_create(fetch_basis)

if __name__ == '__main__':
    main()
