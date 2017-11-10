# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   File Name：    proxy_fetch.py
   Description :  Mongodb模板
   Author :       Leif.xing
   Date：         2017-09-28
"""
import os
import sys

sys.path.append(os.getcwd())
from lib.base import MongoDB


mdb = MongoDB('proxy', 'crawler')
cursor = mdb.coll


def insert(doc):
    cursor.insert(doc)


def query(**kwargs):
    if kwargs:
        return cursor.find(kwargs)
    else:
        return cursor.find()


def delete(**kwargs):
    cursor.delete_one(kwargs)


def update(query, to_update):
    cursor.update(query, to_update)


def upsert(query, to_update):
    cursor.update(query, to_update, True)


def exists(**kwargs):
    return True if cursor.find(kwargs).count() else False
