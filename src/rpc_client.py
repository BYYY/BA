#!usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2

import urllib
import re

__author__ = 'Sapocaly'

from utils import DBconfig

import xmlrpclib

import utils.PathHelper
utils.PathHelper.configure_dir()

import src.DB.Entry as Entry
import src.DB.DAL as DAL

import urlfinder

import base64
#DB saving related
# config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
# config_args = dict(zip(['host', 'user', 'passwd', 'database'],
#                           [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
# DAL.create_engine(**config_args)
#
# t = Entry.Page(url='test_url', content='糖糖糖')
# Entry.Page.add(t)
# del (t)


#rpc cal related
#ip 10.84.14.55 for remote usage

def fetch(url):
    print 'starting fetch ',url
    response = urllib2.urlopen(url)
    html = response.read()
    print 'fetched!!!!!!!!!!!!!!!!!!!!'
    return html

def save_html(url,html):

    encoded_html = base64.b64encode(html)
    #print encoded_html
    #with DAL.connection():
    t = Entry.Page(url=url, content=encoded_html)
    Entry.Page.add(t)
        #del(t)


config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
DAL.create_engine(**config_args)

proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8001/")
multicall = xmlrpclib.MultiCall(proxy)

multicall.put('http://www.kenrockwell.com')

result = multicall()
print tuple(result)[0]

while True:
    print 'this is a loop!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    try:
        proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8001/")
        multicall = xmlrpclib.MultiCall(proxy)
        multicall.get()
        result = multicall()

        finder = urlfinder.urlfinder();
        start_url = tuple(result)[0]

        html = fetch(start_url)
        finder.feed(html)
        new_urls = finder.urls

        print 'hahaha'
        proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8001/")
        multicall = xmlrpclib.MultiCall(proxy)
        for url in new_urls:
            print url
            multicall.put(url)
        print 'huehuehue'

        print tuple(multicall())

        save_html(start_url,html)

        print 'xiexiexie'

    except Exception as e:
        print e
        print 'oops!!!!!!!!!!!'



