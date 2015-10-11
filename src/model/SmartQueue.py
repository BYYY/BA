# -*- coding: utf-8 -*-

__author__ = 'Sapocaly'

import Queue


# 这是一个限定内存利用的queue

class SmartQueue(Queue.Queue):
    def __init__(self):
        #设置初始容量
        Queue.__init__(self)

    def put(self):
        #对外接口
        pass

    def get(self):
        #对外接口
        pass

    def save(self):
        #对外接口
        pass

    def load(self):
        #对外接口
        pass
