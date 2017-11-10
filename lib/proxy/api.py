# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   File Name：    proxy_fetch.py
   Description :  抓取免费代理
   Author :       Leif.xing
   Date：         2017-09-28
"""
import os
import sys
import requests
from lxml import html
from dotmap import DotMap
from tomorrow import threads
from user_agent import generate_user_agent

sys.path.append(os.getcwd())
from lib.business import insert, query, delete, update, exists
from lib.base import logout

header = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


def random_user_agent():
    global header
    header['User-Agent'] = generate_user_agent()


def proxy_goubanjia(debug=False):
    def url_factory(pages=5):
        return ('http://www.goubanjia.com/free/gngn/index%s.shtml' % str(i + 1)
                for i in range(pages))

    @threads(20)
    def download(url):
        """
        此处多线程并发执行，只允许返回Tomorrow对象，多余运行结果可以考虑放入缓存做后期处理
        需要加入异常处理机制，将错误url放在缓存中，以便能够从缓存中继续抓数据
        :param url:
        :return:
        """
        try:
            print(url)
            random_user_agent()
            return requests.get(url, headers=header, timeout=5)
        except Exception as e:
            print(e)

    dm = DotMap()
    dm.source = 'goubanjia'
    responses = [download(url) for url in url_factory()]
    responses.insert(0, download('http://www.goubanjia.com/free/gngn/index.shtml'))
    xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()"""
    for response in responses:
        tree = html.fromstring(response.text)
        table_rows = tree.xpath('//tbody/tr')
        for row in table_rows:
            tds = row.xpath('./td')
            dm.ip = ''.join(tds[0].xpath(xpath_str))
            dm.port = tds[0].xpath(".//span[contains(@class, 'port')]/text()")[0]
            dm.anonymity = tds[1].xpath('.//a/text()')[0]
            dm.category = tds[2].xpath('.//a/text()')[0].lower()
            if not exists(ip=dm.ip):
                insert(dm.toDict())
            if debug:
                print('-' * 150)
                print(dm.toDict())


def proxy_data5u(debug=False):
    """
    抓取高匿代理，服务器周期性提供新的代理，需要定时抓取
    :return:
    """

    @threads(2)
    def download(url):
        """
        :param url:
        :return:
        """
        try:
            print(url)
            random_user_agent()
            return requests.get(url, headers=header, timeout=5)
        except Exception as e:
            print(e)

    dm = DotMap()
    dm.source = 'data5u'
    urls = [
        'http://www.data5u.com/free/gngn/index.shtml'
    ]
    responses = [download(url) for url in urls]
    for response in responses:
        tree = html.fromstring(response.text)
        uls = tree.xpath('//ul[@class="l2"]')
        for ul in uls:
            spans = ul.xpath('.//span')
            dm.ip = spans[0].xpath('.//li/text()')[0]
            dm.port = spans[1].xpath('.//li/text()')[0]
            dm.anonymity = spans[2].xpath('.//li/a/text()')[0]
            dm.category = spans[3].xpath('.//li/a/text()')[0].lower()
            if not exists(ip=dm.ip):
                insert(dm.toDict())
            if debug:
                print('-' * 150)
                print(dm.toDict())


def proxy_66ip(debug=False):
    """
    Url: http://www.66ip.cn/areaindex_34/3.html
    :return:
    """
    def urls_66ip(x, y):
        for i in range(x):
            for j in range(y):
                yield 'http://www.66ip.cn/areaindex_%s/%s.html' % (str(i+1), str(j+1))

    @threads(5)
    def download(url):
        """
        :param url:
        :return:
        """
        try:
            print(url)
            random_user_agent()
            return requests.get(url, headers=header, timeout=5)
        except Exception as e:
            print(e)

    dm = DotMap()
    dm.source = '66ip'
    dm.category = 'http'
    dm.anonymity = '高匿'
    responses = [download(url) for url in urls_66ip(34, 103)]
    for response in responses:
        try:
            response.encoding = 'GB2312'
            tree = html.fromstring(response.text)
            trs = tree.xpath('//div[@class="footer"]/div/table/tr')
            if len(trs) > 1:
                for tr in trs[1:]:
                    tds = tr.xpath('.//td/text()')
                    dm.ip = tds[0]
                    dm.port = tds[1]
                    if not exists(ip=dm.ip):
                        insert(dm.toDict())
                    if debug:
                        print(dm.toDict())
        except:
            pass


def proxy_ip181(debug=False):
    def download(url):
        """
        :param url:
        :return:
        """
        try:
            print(url)
            random_user_agent()
            return requests.get(url, headers=header, timeout=5)
        except Exception as e:
            print(e)

    dm = DotMap()
    dm.source = 'ip181'
    web_url = 'http://www.ip181.com/'
    response = download(web_url)
    response.encoding = 'gb2312'
    xpath_str = '//tbody/tr[not(contains(@class, "active"))]'
    tree = html.fromstring(response.text)
    trs = tree.xpath(xpath_str)
    for tr in trs:
        tds = tr.xpath('.//td/text()')
        dm.ip = tds[0]
        dm.port = tds[1]
        dm.anonymity = tds[2]
        if ',' in tds[3]:
            dm.category = 'http'
        else:
            dm.category = tds[3].lower()
        if not exists(ip=dm.ip):
            insert(dm.toDict())
        if debug:
            print('-' * 150)
            print(dm.toDict())


def verify_proxies():
    target = 'http://www.xxorg.com/tools/checkproxy/'

    def get_ip(address):
        return address.split(':')[1][2:]

    def get_category(address):
        return address.split(':')[0]

    @threads(20)
    def test(category, proxy):
        headers = {
            'User-Agent': generate_user_agent(),
            'Connection': 'keep-alive'
        }
        proxies = {
            category: proxy,
        }
        s = requests.Session()
        req = requests.Request('GET', target, headers=headers)
        prepped = s.prepare_request(req)
        try:
            html = s.send(prepped, proxies=proxies, timeout=5)
            if int(html.status_code) != 200 or 'REMOTE_ADDR' not in html.text:
                logout(keyword=proxy + ' to delete!')
                delete(ip=get_ip(proxy))
                return
            print('%s test OK, status code: %s!' % (proxy, html.status_code))
            # print(html.text + proxy + ' ~~~~~~~~~~~~~~~~')
            mql = {'ip': get_ip(proxy)}
            to_update = {
                '$set': {
                    'available': 1,
                    'category': get_category(proxy)
                }
            }
            update(mql, to_update)
            return html
        except Exception as e:
            logout(keyword=proxy + ' to delete!')
            for error in ['ProxyError', 'ConnectTimeoutError']:
                if error in str(e):
                    delete(ip=get_ip(proxy))
                    break

    def get_urls(**kwargs):
        logout(keyword=kwargs)
        docs = query(**kwargs)
        logout(keyword=docs.count())
        for doc in docs:
            category = doc['category']
            if ',' in category:
                for sub_cat in category.split(','):
                    yield sub_cat, sub_cat + '://' + doc['ip'] + ':' + doc['port']
            else:
                yield category, category + '://' + doc['ip'] + ':' + doc['port']

    responses = [test(item[0], item[1]) for item in get_urls()]


# proxy_goubanjia(debug=True)
# proxy_data5u(debug=True)
# proxy_66ip(debug=True)
# proxy_ip181(debug=True)
