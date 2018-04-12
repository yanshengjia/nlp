# -*- coding: utf-8 -*-


#每个回答的div里面都有一个叫 data-aid="12345678"的东西,
#然后根据, www.zhihu.com/answer/12345678/voters_profile?&offset=10
#这个json数据连接 分析所有点赞的id和个人链接
#对于想要爬取的数据，关键在于发现要爬的这个东西的关键特征，而且这个关键特征需要和我们要爬取的数据唯一对应，这个爬虫的关键信息就是 data-aid
#一句话概述：对人工操作时发送的HTTP Request/Response进行分析，找出关键定位特征。
#firebug


import requests
#requests 发送网页请求非常简单
from bs4 import BeautifulSoup
#Beautiful Soup 是用Python写的一个HTML/XML的解析器，它可以很好的处理不规范标记并生成剖析树(parse tree)。 它提供简单又常用的导航（navigating），搜索以及修改剖析树的操作。
import time
import json
import os
import sys

url = 'http://www.zhihu.com'
loginURL = 'http://www.zhihu.com/login/email'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

data = {
    'email': 'xxxxx@gmail.com',
    'password': 'xxxxxxx',
    'rememberme': "true",
}

s = requests.session()
# 如果成功登陆过,用保存的cookies登录
if os.path.exists('cookiefile'):
    with open('cookiefile') as f:
        cookie = json.load(f)
    s.cookies.update(cookie)
    req1 = s.get(url, headers=headers)
    with open('zhihu.html', 'w') as f:
        f.write(req1.content)
# 第一次需要手动输入验证码登录
else:
    req = s.get(url, headers=headers)
    print req
    
    soup = BeautifulSoup(req.text, "html.parser")
    xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
    
    data['_xsrf'] = xsrf
    
    timestamp = int(time.time() * 1000)
    captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
    print captchaURL
    
    with open('zhihucaptcha.gif', 'wb') as f:
        captchaREQ = s.get(captchaURL)
        f.write(captchaREQ.content)
    loginCaptcha = raw_input('input captcha:\n').strip()
    data['captcha'] = loginCaptcha
    # print data
    loginREQ = s.post(loginURL,  headers=headers, data=data)
    # print loginREQ.url
    # print s.cookies.get_dict()
    if not loginREQ.json()['r']:
        # print loginREQ.json()
        with open('cookiefile', 'wb') as f:
            json.dump(s.cookies.get_dict(), f)
    else:
        print 'login failed, try again!'
        sys.exit(1)

# 以晨航大神57赞回答为例 15949124
# http://www.zhihu.com/answer/15949124/voters_profile?&offset=40
# http://www.zhihu.com/question/31241550/answer/51370799

zanBaseURL = 'http://www.zhihu.com/answer/15949124/voters_profile?&offset={0}'
page = 0
count = 0
while 1:
    zanURL = zanBaseURL.format(str(page))
    page += 10
    zanREQ = s.get(zanURL, headers=headers)
    zanData = zanREQ.json()['payload']
    if not zanData:
        break
    for item in zanData:
        # print item
        zanSoup = BeautifulSoup(item, "html.parser")
        zanInfo = zanSoup.find('a', {'target': "_blank", 'class': 'zg-link'})
        if zanInfo:
            print 'nickname:', zanInfo.get('title'),  '    ',
            print 'person_url:', zanInfo.get('href')
        else:
            anonymous = zanSoup.find(
                                     'img', {'title': True, 'class': "zm-item-img-avatar"})
            print 'nickname:', anonymous.get('title')

        count += 1
    print count