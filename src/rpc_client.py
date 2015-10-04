#!usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2

__author__ = 'Sapocaly'

from utils import DBconfig

import xmlrpclib

import utils.PathHelper
utils.PathHelper.configure_dir()

import src.DB.Entry as Entry
import src.DB.DAL as DAL


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
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def save_html(url,html):
    import base64
    encoded_html = base64.b64encode(html)
    print encoded_html
    with DAL.connection():
        t = Entry.Page(url=url, content=encoded_html)
        Entry.Page.add(t)
        del(t)

def parse_html(html):

    pass

config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
DAL.create_engine(**config_args)
#html = fetch("http://www.baidu.com")
#save_html("http://www.baidu.com",html)
while True:
    proxy = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
    multicall = xmlrpclib.MultiCall(proxy)
    multicall.get()
    result = multicall()
    start_url = tuple(result)[0]
    html = fetch(start_url)
    new_urls = parse_html(html)
    save_html(start_url,html)

for url in new_urls:
    multicall.put(url)



