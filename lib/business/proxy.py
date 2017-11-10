# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   File Name：    proxy_fetch.py
   Description :  业务代码逻辑
   Author :       Leif.xing
   Date：         2017-09-28
"""
import os
import sys

sys.path.append(os.getcwd())
from lib.proxy import proxy_ip181, proxy_66ip, proxy_data5u, proxy_goubanjia, \
    verify_proxies


def catch():
    proxy_data5u()
    proxy_goubanjia()
    proxy_ip181()
    proxy_66ip()


def verify():
    verify_proxies()
