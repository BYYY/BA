#!usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import urllib2
import xmlrpclib
import HTMLParser
from urlparse import urlparse

import utils.PathHelper

utils.PathHelper.configure_dir()

__author__ = 'Sapocaly'


def fetch(url):
    response = urllib2.urlopen(url, timeout=8)
    html = response.read()
    return html


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


class Urlfinder(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.urls.append(value)


def is_valid_url(url):
    o = urlparse(url)
    if o.scheme != 'http':
        return False
    if o.netloc != 'www.kenrockwell.com':
        return False
    return True


# initialize core server
core_server = get_muticall("http://127.0.0.1:8833/")

core_server.put('http://www.kenrockwell.com')

# get data server config
core_server.get_config()
success, config = core_server()
data_addresses = config['DATA-SERVICE']
ip, port = data_addresses[0]

# initialize data server
data_server = get_muticall("http://{}:{}/".format(ip, port))

# initialize variable
finder = Urlfinder()

while True:
    try:
        # dequeue url
        core_server.get()
        result = core_server()
        start_url = tuple(result)[0]
        print 'start:', start_url

        # fetch html
        html = fetch(start_url)

        # save html
        data_server.save(start_url, base64.b64encode(html))
        data_server()

        # parse for new urls
        finder.feed(html)
        new_urls = finder.urls

        # enqueue new urls
        for url in new_urls:
            if is_valid_url(url):
                print url
                core_server.put(url)
        core_server()
    except Exception as e:
        print e
