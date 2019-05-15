#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-5-15 下午4:54
# @Author  : Hubery
# @File    : helper.py
# @Software: PyCharm

import json
import requests
from requests.exceptions import ConnectionError

from ProxyIPPool import settings


def get_text(url, options={}):
    """
    抓取代理
    :param method: 请求方法
    :param url: 请求的目标url
    :param options:
    :return:
    """
    headers = dict(settings.BASE_HEADERS, **options)
    print('正在抓取', url)
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            print('抓取成功', url, res.status_code)
            return res.text
    except ConnectionError:
        print('抓取失败', url)
        return None


def get_ip_address(ip):
    """
    获取ip地址
    :param ip:
    :return:
    """
    url = 'http://ip.taobao.com//service/getIpInfo.php?ip={}'.format(ip)
    headers = settings.BASE_HEADERS
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            res_dict_data = json.loads(res.text).get('data', '')
            country = res_dict_data.get('country', '')
            region = res_dict_data.get('region', '')
            city = res_dict_data.get('city', '')
            isp = res_dict_data.get('isp', '')
            ip_address = '/'.join([country, region, city, isp])
            return ip_address
        else:
            return ''
    except Exception as e:
        print('请求淘宝地址失败, 失败失败原因{}'.format(e))
        return None


if __name__ == '__main__':

    ip_address = get_ip_address('49.5.10.34')
    print(ip_address)