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
from utils.helper import get_ip_address


def verify_ip(proxy_ip, proxy_port):
    """"""

    def _verify_test(test_url):
        proxies = {
            "http": "http://%s:%s" % (proxy_ip, proxy_port),
            "https": "https://%s:%s" % (proxy_ip, proxy_port),
        }
        try:
            _start = time.time()
            r = requests.get(url=test_url, headers=settings.BASE_HEADERS, proxies=proxies, timeout=3)
            if r.status_code == 200:
                speed = '%.2f秒' % (time.time() - _start)
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
        except:
            pass
        return False, 0, 0

    protocol = 0
    http_test_url = settings.HTTP_TEST_URL
    http_result, http_types, http_speed = _verify_test(http_test_url)
    protocol += 1 if http_result else 0

    https_test_url = settings.HTTPS_TEST_URL
    https_result, https_types, https_speed = _verify_test(https_test_url)
    protocol += 2 if https_result else 0

    types = 0
    speed = 0
    if protocol == 1:
        types = http_types
        speed = http_speed
    elif protocol == 2:
        types = https_types
        speed = https_speed
    elif protocol == 3:
        types = http_types
        speed = http_speed
    else:
        return None
    ip_address = get_ip_address(proxy_ip)
    time.sleep(1)
    proxy_info = {
        "ip": proxy_ip,
        "port": proxy_port,
        "protocol": protocol,
        "types": types,
        "speed": speed,
        'ip_address': ip_address
    }
    return proxy_info

