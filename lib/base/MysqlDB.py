#! /usr/bin/python
# -*- coding: utf-8 -*- 
"""
@author ----> Leif.Xing
@mail   ----> leif.xing@gmail.com
"""

import sys
import pymysql


class MysqlDB(object):
    def __init__(self):
        self.config = {"host": "localhost",
                       "port": 3306,
                       "user": "root",
                       "passwd": "huaqin123",
                       "db": "information_schema",
                       "charset": "utf8"
                       }
        self.conn = None
        self.cursor = None
        self.db = None
        self.table = None
        self.sql = ""
        self.param = ()
        self.field = ()
        self.sets = None
        self.DEBUG = False

    def open(self):
        """
        根据配置打开数据库，返回对应表的cursor
        :return:
        """
        try:
            self.conn = pymysql.connect(
                host=self.config["host"],
                port=self.config["port"],
                user=self.config["user"],
                passwd=self.config["passwd"],
                db=self.config["db"],
                charset=self.config["charset"]
            )
        except Exception as e:
            print("Connection for mysql db failed, Error: %s!" % e)
            sys.exit()
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def field_count(self):
        """
        返回表的字段数
        :return:
        """
        if self.field:
            return len(self.field)
        else:
            return None

    def get_insert_sql(self):
        if self.field:
            val_str = self.field_count() * "\'%s\',"
            val_str = val_str[:-1]
            return 'insert into %s %s values(%s)' % (self.table, "%s", val_str)

    @staticmethod
    def filter_char(src):
        """
        sql语句预处理
        :param src:
        :return:
        """
        src = src.replace("\\", "")
        if "'" in src:
            return src.replace("'", "\\'")
        else:
            return src

    @staticmethod
    def add_special_char(src):
        """
        sql语句查询前的预处理
        :param src:
        :return:
        """
        if '"' in src:
            return src.replace('"', '\\"')
        else:
            return src

    def results_align(self):
        """
        格式化打印输出
        :return:
        """
        if self.sets:
            length = len(self.sets[0])
            print(("+" + "-"*29)*length)
            for item in self.sets:
                tmp_str = ""
                for term in item:
                    unicode_count = repr(term).count("\\u")
                    tmp_str += term.ljust(40-unicode_count)
                print(tmp_str)
            print(("+" + "-"*29)*length)

    def run(self, fetch_flag=False):
        """
        根据sql语句和设定的参数执行数据库查询，设置结果集并返回其数量
        """
        if self.cursor:
            if self.sql and self.param:
                sql_cmd = self.sql % self.param
            elif self.sql:
                sql_cmd = self.sql
            else:
                print("SQL cmd is Null, nothing to do!")
                return None
        else:
            print("Cursor is Null, please check!")
            return None
        rows = self.cursor.execute(sql_cmd)
        if fetch_flag:
            self.sets = self.cursor.fetchall()
            if self.DEBUG:
                self.results_align()
        return rows

    def commit(self):
        """
        执行数据库插入或更新操作
        :return:
        """
        if self.conn:
            self.conn.commit()
        else:
            print("DB not opened, please check!")
