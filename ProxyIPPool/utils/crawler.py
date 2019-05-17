#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-5-15 下午5:49
# @Author  : Hubery
# @File    : crawler.py
# @Software: PyCharm

import os
import django

from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from queue import Queue
from utils.helper import get_text
from utils.validator import verify_ip

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProxyIPPool.settings')
django.setup()

from IPPool.models import ProxyIP

# 创建队列
q = Queue()

# 创建更新队列
update_q = Queue()


def crawl_89ip(page_count=2):
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
                ip = tr.xpath("./td[1]/text()")[0].replace('\n', '').replace('\t', '')
                port = tr.xpath("./td[2]/text()")[0].replace('\n', '').replace('\t', '')
                q.put((ip, port))
                p89_ip_list.append((ip, port))
    return p89_ip_list


def crawl_qy_dai_li(page_count=2):
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
                    # proxy_type = tr.xpath("./td[4]/text()")[0].lower()
                    ip = tr.xpath("./td[1]/text()")[0]
                    port = tr.xpath("./td[2]/text()")[0]
                    q.put((ip, port))
                    qy_ip_list.append((ip, port))
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
                # proxy_type = tr.xpath("./td[4]/text()")[0].lower()
                ip = tr.xpath("./td[1]/text()")[0]
                port = tr.xpath("./td[2]/text()")[0]
                q.put((ip, port))
                ip_3366_list.append((ip, port))
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
                hig_ip_list.append((ip_port[0], ip_port[1].replace('\r', '')))
                q.put((ip_port[0], ip_port[1].replace('\r', '')))
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
    rmccurdy_ip_list = []
    if response_html:
        tem = response_html.split('\n')
        for i in tem:
            if i == '' or i == ':':
                continue
            try:
                ip_port = i.split(':')
                proxy_type = 'http'
                rmccurdy_ip_list.append((proxy_type, ip_port[0], ip_port[1]))
                q.put((ip_port[0], ip_port[1].replace('\r', '')))
            except:
                return []
    return rmccurdy_ip_list


def run():
    craw_ip_list = [crawl_89ip, crawl_qy_dai_li]
    # craw_ip_list = [crawl_89ip, crawl_qy_dai_li, crawl_3366_dai_li, crawl_highanon, craw_rmccurdy]

    with ThreadPoolExecutor(max_workers=4) as pool1:
        for future in craw_ip_list:
            pool1.submit(future)

    with ThreadPoolExecutor(max_workers=8) as pool2:
        """
        get_result 为用add_done_callback()方法来添加回调函数，该回调函数形如 fn(future)。当线程任务完成后，
        程序会自动触发该回调函数，并将对应的 Future 对象作为参数传给该回调函数
        """
        def get_result(future):
            proxy_info = future.result()
            if proxy_info:
                # 如果数据存在存入数据
                protocol = proxy_info.get('protocol', None)
                types = proxy_info.get('types', None)
                ip = proxy_info.get('ip', None)
                port = proxy_info.get('port', None)
                speed = proxy_info.get('speed', None)
                ip_address = proxy_info.get('ip_address', None)
                proxy_ip = ProxyIP.objects.filter(protocol=protocol, types=types, ip=ip, port=port,
                                                  ip_address=ip_address).first()
                if not proxy_ip:
                    print('save', proxy_info)
                    ProxyIP.objects.create(protocol=protocol, types=types, ip=ip, port=port, speed=speed,
                                           ip_address=ip_address)

        while not q.empty():
            proxy_ip_port = q.get()
            q.task_done()
            pool2.submit(verify_ip, proxy_ip_port[0], proxy_ip_port[1]).add_done_callback(get_result)

    q.join()
    print('done')


def update_ip():
    """
    定期检测数据的可用性
    :return:
    """
    def check_ip(ip, port):
        proxy_info = verify_ip(ip, port)
        db_ip = ProxyIP.objects.filter(ip=ip, port=port).first()
        if proxy_info:
            db_ip.save()
        else:
            db_ip.delete()

    proxy_all = ProxyIP.objects.all()
    for proxy_info in proxy_all:
        update_q.put(proxy_info)

    with ThreadPoolExecutor(max_workers=8) as pool3:
        while not update_q.empty():
            proxy_info = update_q.get()
            update_q.task_done()
            pool3.submit(check_ip, proxy_info.ip, proxy_info.port)


if __name__ == '__main__':
    run()
    update_ip()