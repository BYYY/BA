#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entries as classes
"""

from src.DB.Model import Model


class Page(Model):
    table = 'page_content'  # table name is page_content
    fields = ['id', 'url', 'content']


class Url(Model):
    table = 'cached_url'  # table name cached_url
    fields = ['url']

class UrlMap(Model):
    table = 'url_map'
    fields = ['id', 'url', 'hashed_name', 'hashed_folder']