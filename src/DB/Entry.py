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
    table = 'cached_url'  # table name is page_content
    fields = ['url']