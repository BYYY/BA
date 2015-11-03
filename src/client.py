#!usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import xmlrpclib
import HTMLParser
from urlparse import urlparse

import utils.PathHelper

utils.PathHelper.configure_dir()

import src.core.fetcher as fetcher
from src.config import ConfigConstant

__author__ = 'Sapocaly'


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


def is_valid_url(url):
    o = urlparse(url)
    if o.scheme != 'http':
        return False
    if o.netloc != 'www.zhihu.com':
        return False
    return True


# initialize core server
deploy_config = ConfigConstant.DEPLOY_CONFIG
core_server=get_muticall('http://{}:{}/'.format(deploy_config.CORE_ADDRESS, deploy_config.CORE_PORT))

core_server.put('http://www.zhihu.com')

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
fetcher = fetcher.ZhihuFetcher(email='sym1all@hotmail.com', password='192519251925')
print 'fetcher initialized:{}'.format(fetcher.__class__)

while True:
    try:
        # dequeue url
        core_server.get()
        result = core_server()
        start_url = tuple(result)[0]
        print start_url

        # fetch html
        html = fetcher.fetch(start_url)

        # save html
        data_server.save(start_url, base64.b64encode(html))
        data_server()

        # parse for new urls
        finder.feed(html.decode('utf-8'))
        new_urls = finder.urls

        # enqueue new urls
        for url in new_urls:
            if is_valid_url(url):
                core_server.put(url)
        core_server()
    except Exception as e:
        print e
