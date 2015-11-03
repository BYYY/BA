# -*- coding:utf-8 -*-
import re
import os

import requests

__author__ = 'Sapocaly'


class ZhihuFetcher:
    def __init__(self, email, password):
        self.url = 'http://www.zhihu.com'
        self.login_url = self.url + '/login/email'
        self.login_data = {
            'email': email,
            'password': password,
            'rememberme': 'true',
        }
        self.headers_base = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'Referer': 'http://www.zhihu.com/',
        }

        self.session = requests.session()
        self.xsrf = self.__get_xsrf(self.url)
        self.login_data['_xsrf'] = self.xsrf.encode('utf-8')
        captcha_url = 'http://www.zhihu.com/captcha.gif'
        captcha = self.session.get(captcha_url, stream=True)
        f = open('captcha.gif', 'wb')
        for line in captcha.iter_content(10):
            f.write(line)
        f.close()
        captcha_str = raw_input('please input captcha from captcha.gif:')
        self.login_data['captcha'] = captcha_str
        res = self.session.post(self.login_url, headers=self.headers_base, data=self.login_data)
        self.m_cookies = res.cookies
        os.remove('captcha.gif')

    def __get_xsrf(self, url=None):
        r = self.session.get(url, headers=self.headers_base)
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', r.text)
        if xsrf == None:
            return ''
        else:
            return xsrf.group(0)

    def fetch(self, url):
        res = self.session.get(url, headers=self.headers_base, cookies=self.m_cookies)
        return (res.text).encode('utf-8')
