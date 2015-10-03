#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model class for all entries
"""

import src.DB.DAL as DAL


# governing class for all entries. this is a dict
class Model(dict):
    table = None
    fields = None
    index = None

    # get key, vales from **args
    def __init__(self, **args):
        super(Model, self).__init__(**args)
        # 存一份用户不修改的信息
        for kw in args.keys():
            self['_' + kw] = args[kw]

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self['_' + key] = value

    def _query_dict(self):
        query_dict = {}
        for key in self.keys():
            if key[0] == '_':
                query_dict[key] = self[key]
        return query_dict

    def _working_dict(self):
        working_dict = {}
        for key in self.keys():
            if key[0] != '_':
                working_dict[key] = self[key]
        return working_dict

    # todo: 同步
    def save(self):
        DAL.update(self.__class__.table, **self)
        for key in self.__class__.fields:
            self[key] = self['_' + key]

    @classmethod
    def get(cls, **args):
        selection = DAL.select_from(cls.table, **args)
        # 获取entry信息，创建新instance，initialize，生成list
        return [cls(**dict(zip(cls.fields, entry))) for entry in selection]

    @classmethod
    def add(cls, lst):
        if type(lst) == cls:
            DAL.insert_into(cls.table, **lst._working_dict())
        else:
            # 是否需要保持事务性?
            with DAL.connection():
                for entry in lst:
                    DAL.insert_into(cls.table, **entry._working_dict())

    # remove, 即可传入多个Entry也可传入list of Entry
    @classmethod
    def remove(cls, lst):
        if type(lst) == cls:
            DAL.delete_from(cls.table, **lst._working_dict())
        else:
            with DAL.connection():
                for entry in lst:
                    DAL.delete_from(cls.table, **entry._working_dict())
