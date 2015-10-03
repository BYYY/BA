#!usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sapocaly'

import xmlrpclib

import src.DB.Entry as Entry
import src.DB.DAL as DAL

config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       ['10.84.14.55', 'root', 'byyyserver', 'BA']))

DAL.create_engine(**config_args)
t = Entry.Page(url='test_url', content='糖糖糖')
Entry.Page.add(t)
del (t)

proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
multicall = xmlrpclib.MultiCall(proxy)
multicall.put('www.centre.edu')
result = multicall()
print tuple(result)
