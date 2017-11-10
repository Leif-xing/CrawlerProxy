#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:      Leif.xing
@mail:        leif.xing@gmail.com
"""

import os
import sys
import subprocess as _sp


def log_traceback():
    """
    Log traceback from runtime exception and write error log to log/framework.log
    """
    traceback_template = """Traceback (most recent call last):
 File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n"""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = {
        'filename': exc_traceback.tb_frame.f_code.co_filename,
        'lineno': exc_traceback.tb_lineno,
        'name': exc_traceback.tb_frame.f_code.co_name,
        'type': exc_type.__name__,
        'message': exc_value.message,
    }
    del (exc_type, exc_value, exc_traceback)
    return traceback_template % traceback_details


def path_exists(file_to_path):
    """
    Check if path exists
    :param file_to_path: path to check
    :return: Boolean: True --> exist, False --> not exist
    """
    if os.path.exists(file_to_path):
        return True
    else:
        return False


def run_system_cmd(cmd):
    """
    Run cmd and get run state and result
    :param cmd: command to run
    :return:
    """
    status, result = _sp.getstatusoutput(cmd)
    if status:
        print(cmd)
        print(result)
    return status, result


def ftm(i_float, count):
    return float(("{0:.%sf}" % str(count)).format(float(i_float)))


def logout(separator='-', length=20, keyword=''):
    print(separator * length + ' %s ' % keyword + separator * length)
