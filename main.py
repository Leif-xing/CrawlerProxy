#!/usr/bin/env python
"""
   File Name：    main.py
   Description :  程序入口
   Author :       Leif.xing
   Date：         2017-09-28
"""
import os
import sys
from optparse import OptionParser

sys.path.append(os.getcwd())
from lib.business import catch, verify


def parse_args():
    parser = OptionParser()
    parser.add_option('-f', '--fetch', action='store_true', dest='fetch',
                      help='Fetch proxies from proxy servers')
    parser.add_option('-v', '--verify', action='store_true', dest='verify',
                      help='Verify proxies for proxy validation')
    return parser.parse_args()


def main():
    (options, args) = parse_args()
    if options.fetch:
        catch()
    elif options.verify:
        verify()
    else:
        print('Param error, please check by -h!')


if __name__ == "__main__":
    main()
