# -*- coding: utf-8 -*-
import json
import re
import requests

class Fund(object):
    def __init__(self, code):
        self.code = code
        self.fill_fund_info()

    def fill_fund_info(self):
        response = requests.get('http://fundgz.1234567.com.cn/js/%s.js' % self.code)
        r = re.match(r'jsonpgz\((.*)\);', response.text)
        data = r.group(1)
        jd = json.loads(data)
        self.ass_val_date = jd['gztime']
        self.ass_val = float(jd['gsz'])
        self.net_val_date = jd['jzrq']
        self.net_val = float(jd['dwjz'])
