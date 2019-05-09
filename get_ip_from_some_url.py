#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 15:20
# @Author  : Hubery
# @File    : get_ip_from_some_url.py
# @Software: PyCharm

import requests
from requests.exceptions import ConnectionError
from lxml import etree

from fake_useragent import UserAgent

base_headers = {
    'User-Agent': UserAgent().random,
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_text(url, options={}):
    """
    抓取代理
    :param url: 请求的目标url
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            print('抓取成功', url, response.status_code)
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None


def crawl_89ip(page_count=10):
    """
    获取 http://www.89ip.cn/index.html 免费代理
    :param page_count:
    :return:
    """
    start_url = 'http://www.89ip.cn/index_{}.html'
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    p89_ip_list = []
    for url in urls:
        print("Crawling", url)
        headers = {
            "Referer": url,
            "Host": "www.89ip.cn",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url, options=headers)
        if response_html:
            tree = etree.HTML(response_html)
            tr_list = tree.xpath('//table[@class="layui-table"]/tbody/tr')
            for tr in tr_list:
                proxy_type = 'http'
                ip = tr.xpath("./td[1]/text()")[0].replace('\n', '').replace('\t', '')
                port = tr.xpath("./td[2]/text()")[0].replace('\n', '').replace('\t', '')
                p89_ip_list.append((proxy_type, ip, port))
    return p89_ip_list


def crawl_qy_dai_li(page_count=5):
    """
    获取旗云代理http://www.qydaili.com/free/?action=china&page=1
    :param page_count:
    :return:
    """
    start_url = "http://www.qydaili.com/free/?action=china&page={}"
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    qy_ip_list = []
    for url in urls:
        print("Crawling", url)
        headers = {
            "Host": "www.qydaili.com",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url, options=headers)
        if response_html:
            tree = etree.HTML(response_html)
            tr_list = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
            for tr in tr_list:
                try:
                    proxy_type = tr.xpath("./td[4]/text()")[0].lower()
                    ip = tr.xpath("./td[1]/text()")[0]
                    port = tr.xpath("./td[2]/text()")[0]
                    qy_ip_list.append((proxy_type, ip, port))
                except:
                    continue
    return qy_ip_list


def crawl_3366_dai_li(page_count=5, stype='1'):
    """
    获取云代理http://www.ip3366.net/free/?stype=1&page=3
    :param page_count:
    :return:
    """
    start_url = "http://www.ip3366.net/free/?stype%s=1&page={}" % stype
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    ip_3366_list = []
    for url in urls:
        print("Crawling", url)
        headers = {
            "Host": "www.ip3366.net",
            "Upgrade-Insecure-Requests": "1",
        }
        response_html = get_text(url, options=headers)
        if response_html:
            tree = etree.HTML(response_html)
            tr_list = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
            for tr in tr_list:
                proxy_type = tr.xpath("./td[4]/text()")[0].lower()
                ip = tr.xpath("./td[1]/text()")[0]
                port = tr.xpath("./td[2]/text()")[0]
                ip_3366_list.append((proxy_type, ip, port))
    return ip_3366_list


def crawl_highanon():
    """
    http://www.proxylists.net/http_highanon.txt
    :return:
    """
    url = 'http://www.proxylists.net/http_highanon.txt'
    response_html = get_text(url=url)
    hig_ip_list = []
    if response_html:
        tem = response_html.split('\n')
        for i in tem:
            if i == '':
                continue
            try:
                ip_port = i.split(':')
                proxy_type = 'http'
                hig_ip_list.append((proxy_type, ip_port[0], ip_port[1].replace('\r', '')))
            except:
                return []
    return hig_ip_list


def craw_rmccurdy():
    """
    https://www.rmccurdy.com/scripts/proxy/good.txt
    :return:
    """
    url = 'https://www.rmccurdy.com/scripts/proxy/good.txt'
    response_html = get_text(url=url)
    hrmccurdy_ip_list = []
    if response_html:
        tem = response_html.split('\n')
        for i in tem:
            if i == '' or i == ':':
                continue
            try:
                ip_port = i.split(':')
                proxy_type = 'http'
                hrmccurdy_ip_list.append((proxy_type, ip_port[0], ip_port[1]))
            except:
                return []
    return hrmccurdy_ip_list


def verify_ip(proxy_ip, proxy_port):
    """"""

    def _verify_tet(test_url):
        proxies = {
            "http": "http://%s:%s" % (proxy_ip, proxy_port),
            "https": "https://%s:%s" % (proxy_ip, proxy_port),
        }
        try:
            print('*****************')
            print('测试%s' % test_url)
            r = requests.get(url=test_url, headers=base_headers, proxies=proxies, timeout=3)
            print(r.status_code)
            print(r.headers)
        except:
            print('验证失败')

    url = 'https://www.baidu.com/s?ie=UTF-8&wd=ip'
    http_test_url = "http://httpbin.org/get"
    https_test_url = "https://httpbin.org/get"

    _verify_tet(url)
    _verify_tet(http_test_url)
    _verify_tet(https_test_url)


if __name__ == '__main__':
    # proxy_ip_list = crawl_89ip()
    pass
    cc = crawl_qy_dai_li()
    print(cc.__len__())
    for c in cc:
        print(c)
        verify_ip(c[1], c[2])
