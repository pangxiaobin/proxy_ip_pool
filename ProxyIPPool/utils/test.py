#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-5-16 上午11:20
# @Author  : Hubery
# @File    : test.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor
import threading
import time


def action(max_num):
    my_sum = 0
    for i in range(max_num):
        print(threading.current_thread().name + ' ' + str(i))
        my_sum += 1
    return my_sum


with ThreadPoolExecutor(max_workers=2) as pool:
    # 向线程池提交一个task, 50会作为action()函数的参数
    future1 = pool.submit(action, 50)
    # 向线程池再提交一个task, 100会作为action()函数的参数
    future2 = pool.submit(action, 100)

    def get_result(future):
        print(future.result())
    # 为future1添加线程完成的回调函数
    future1.add_done_callback(get_result)
    # 为future2添加线程完成的回调函数
    future2.add_done_callback(get_result)
    print('--------------')