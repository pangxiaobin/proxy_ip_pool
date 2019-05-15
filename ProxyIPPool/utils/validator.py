#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-5-15 下午6:03
# @Author  : Hubery
# @File    : validator.py
# @Software: PyCharm
import json
import time

import requests

from ProxyIPPool import settings


def verify_ip(proxy_ip, proxy_port):
    """"""

    def _verify_tet(test_url):
        proxies = {
            "http": "http://%s:%s" % (proxy_ip, proxy_port),
            "https": "https://%s:%s" % (proxy_ip, proxy_port),
        }
        try:
            _start = time.time()
            print('*****************')
            print('测试%s' % test_url)
            r = requests.get(url=test_url, headers=settings.BASE_HEADERS, proxies=proxies, timeout=3)
            if r.status_code == 200:
                speed = '%.2f' % (time.time() - _start)
                r_dict = json.loads(r.text)
                headers = r_dict.get('headers', '')
                ip = r_dict.get('origin')
                proxy_connection = headers.get('Proxy-Connection', None)
                if ',' in ip:
                    types = 3  # 透明
                elif proxy_connection:
                    types = 2  # 普匿
                else:
                    types = 1  # 高匿
                return True, types, speed
            print(r.status_code)
            print(r.headers)
        except:
            pass
        return False, 0, 0

    http_test_url = settings.HTTP_TEST_URL
    https_test_url = settings.HTTPS_TEST_URL

    _verify_tet(http_test_url)
    _verify_tet(https_test_url)


if __name__ == '__main__':
    _sta = time.time()
    time.sleep(1)
    print("%.2f" % (time.time() - _sta))