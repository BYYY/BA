#!usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import xmlrpclib
import HTMLParser
from urlparse import urlparse, urljoin

import utils.PathHelper

utils.PathHelper.configure_dir()

import src.core.fetcher as fetcher
from src.config import ConfigConstant

__author__ = 'Sapocaly'

import time

class Urlfinder(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.urls.append(value)


class SimpleMultiCall:
    def __init__(self, server):
        self.multicall = xmlrpclib.MultiCall(server)
        self.server = server

    def __getattr__(self, name):
        return self.multicall.__getattr__(name)

    def __call__(self):
        result = self.multicall.__call__()
        self.multicall = xmlrpclib.MultiCall(self.server)
        return result


def get_muticall(url):
    proxy = xmlrpclib.ServerProxy(url)
    return SimpleMultiCall(proxy)


def valid_url(url):
    o = urlparse(url)
    if o.scheme == '' and o.netloc == '':
        return urljoin('http://www.centre.edu', url)
    if o.scheme != 'http' and o.scheme != 'https':
        return False
    if o.netloc != 'www.centre.edu':
        return False
    return url


# initialize core server
deploy_config = ConfigConstant.DEPLOY_CONFIG
core_server=get_muticall('http://{}:{}/'.format(deploy_config.CORE_ADDRESS, deploy_config.CORE_PORT))

core_server.put(['http://www.centre.edu'])

# get data server config
core_server.get_config()
print 'initialize connection to core-server...'
print 'getting configurations...'
success, config = core_server()
data_addresses = config['DATA-SERVICE']
ip, port = data_addresses[0]
print 'configurations:'
print config


# initialize data server
print 'initialize connection to data-server:{}:{}...'.format(ip, port)
data_server = get_muticall("http://{}:{}/".format(ip, port))

# initialize variable
finder = Urlfinder()
print 'initialize fetcher...'
#fetcher = fetcher.ZhihuFetcher(email='sym1all@hotmail.com', password='192519251925')
fetcher = fetcher.BaseFetcher()
print 'fetcher initialized:{}'.format(fetcher.__class__)

while True:
    try:
        core_server=get_muticall('http://{}:{}/'.format(deploy_config.CORE_ADDRESS, deploy_config.CORE_PORT))
        # dequeue url
        core_server.get()
        result = core_server()
        start_url = tuple(result)[0]
        print start_url

        # fetch html
        stamp_a = time.time()
        html = fetcher.fetch(start_url)
        print 'fetch cost:{}'.format(time.time() - stamp_a)

        # save html
        stamp_a = time.time()
        data_server.save(start_url, base64.b64encode(html))
        data_server()
        print 'save cost:{}'.format(time.time() - stamp_a)

        # parse for new urls
        finder.feed(html.decode('utf-8'))
        new_urls = finder.urls
        finder.urls = []

        # enqueue new urls
        url_list = []
        for url in new_urls:
            url = valid_url(url)
            if url:
                url_list.append(url)
        core_server.put(url_list)
        stamp_a = time.time()
        core_server()
        print 'put cost:{}'.format(time.time() - stamp_a)
    except Exception as e:
        print e
