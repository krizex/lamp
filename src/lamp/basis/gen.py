# -*- coding: utf-8 -*-
from lamp.log import log
from lamp import config
import tushare as ts
import json
import os

def fetch_basis():
    log.info('Fetching stock basics...')
    pro = ts.pro_api('4105aca09e41fde2adac11ff8cdf7e05cef205d946e06935562e0010')
    ret = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    log.info('Fetched')
    df = ret[['ts_code', 'name']]
    df = df.set_index('ts_code')
    return json.loads(df.to_json(orient='index'))


def persistent_json(data, f):
    with open(f, 'w') as f:
        json.dump(data, f)

def persistent_basis_to(f):
    data = fetch_basis()
    persistent_json(data, f)

def main():
    persistent_basis_to(config.basis_persistent_file)

if __name__ == '__main__':
    main()
