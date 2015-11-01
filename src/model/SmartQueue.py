# -*- coding: utf-8 -*-

__author__ = 'Sapocaly'

import Queue


# 这是一个限定内存利用的queue

class SmartQueue():
    def __init__(self, threshold= 10000):
        self.threshold = threshold
        self.q = Queue.Queue(maxsize = int(threshold * 1.2))
        self.size = 0

    def put(self, item):
        self.q.put(item)
        self.size += 1

    def get(self):
        self.size -= 1
        return self.q.get()

    def save(self):
        #对外接口
        pass

    def load(self):
        #对外接口
        pass
