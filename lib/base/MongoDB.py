#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Leif xing
@mail leif.xing@gmail.com
"""

from pymongo import MongoClient


class MongoDB(object):
    def __init__(self, db_name, coll_name):
        self.client = MongoClient('localhost', 27017)
        self.db_name = db_name
        self.coll_name = coll_name
        self.db = self.client[db_name]
        self.coll = self.db[coll_name]
        self.json = dict()

    def clear(self):
        self.json.clear()

    def switch_coll(self, collection):
        self.coll = self.db[collection]

    def insert(self):
        if self.coll:
            try:
                self.coll.insert(self.json)
            except Exception as e:
                print(self.json)
                print(e)
        else:
            print("Collection not selected!")

    def insert_list(self, src_list):
        if self.coll:
            self.coll.insert_many(src_list)
        else:
            print("Collection not selected!")

    def update(self, query, key, value):
        if self.coll:
            temp = self.coll.find_one(query)
            temp2 = temp.copy()
            temp[key] = value
            self.coll.save(temp)
            self.coll.update(temp, temp2)
        else:
            print("Collection not selected!")

    def remove(self, document):
        if self.coll:
            if document:
                self.coll.remove(document)
            else:
                self.coll.remove()
        else:
            print("Collection not selected!")

    def delete(self, **kwargs):
        if self.coll:
            self.coll.remove(kwargs)
        else:
            print("Collection not selected!")

    def drop_coll(self):
        self.coll.drop()

    def replace(self, src, dst):
        if self.coll:
            self.coll.replace_one(src, dst)
        else:
            print("Collection not selected!")

    def search(self, **kwargs):
        """
        根据查询字符串过滤文档
        :param kwargs: 查询字符串
        :return: 查询文档列表
        """
        if self.coll:
            if kwargs:
                return self.coll.find(kwargs)
            else:
                return self.coll.find()
        else:
            print("Collection not selected!")

    def one(self, **kwargs):
        if self.coll:
            if kwargs:
                return self.coll.find_one(kwargs)
        else:
            print("Collection not selected!")
