#!/usr/bin/env python
"""
   File Name：    proxy.py
   Description :  代理验证程序
   Author :       Leif.xing
   Date：         2017-09-28
"""
import sys
import time
from user_agent import generate_user_agent
from requests import Request, Session

try:
    proxy = sys.argv[1]
except:
    # proxy = 'http://106.39.160.135:8888'
    proxy = 'http://106.14.51.145:8118'
category = 'https' if 'https' in proxy.lower() else 'http'
url = 'http://www.dianping.com/shop/4102470/review_more'
# url = 'http://www.xxorg.com/tools/checkproxy/'
s = Session()
headers = {
    # 使用随机UA可能会导致服务端返回403，原因在于部分冷门UA会被作为反爬检测项
    # 'User-Agent': generate_user_agent(),
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2977.88 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept': 'application/json,text/javascript',
    # 大众点评测试用Cookie
    'Cookie': '_hc.v=bcc4c451-c822-02ae-690e-ed19108f2616.1510283101; _lxsdk_cuid=15fa3e3473fc8-0e26b9b7a46952-5b123112-100200-15fa3e34740c8; _lxsdk=15fa3e3473fc8-0e26b9b7a46952-5b123112-100200-15fa3e34740c8; s_ViewType=1; PHOENIX_ID=0a4885a0-15fa4e830a5-72711c; _tr.u=63GEubgsUJuQPYj7; JSESSIONID=462A9B06E62CDEA11354D6790CEFBE58; aburl=1; cy=79; cye=haerbin; _lxsdk_s=15fa5a64f4e-960-35d-0d8%7C%7C5'
}
proxies = {
    category: proxy,
}
req = Request('GET', url, headers=headers)
prepped = s.prepare_request(req)
start = time.time()
response = s.send(prepped,
                  proxies=proxies,
                  timeout=5
                  )
print(response.text)
print(headers)
print('Time cost on request %s' % str(round((time.time() - start), 3)))
print(response.status_code)
print(response.headers)
print(response.request.headers)
