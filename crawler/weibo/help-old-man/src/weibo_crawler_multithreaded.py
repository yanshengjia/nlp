#-*-coding:utf8-*-
# use Cookie to login weibo.cn
# multithread

import sys
import threading
reload(sys)
sys.setdefaultencoding( "utf-8" )
import requests
from lxml import etree


f1 = open('多线程扶老人.txt','w')

cookie = {"Cookie": "_T_WM=2430b59919b4ec07936f0ac8af279443; _T_WL=1; _WEIBO_UID=2605773190; SUB=_2A257P30ZDeTxGeRI61cW9y3NwjyIHXVYwANRrDV6PUJbrdANLWTCkW1b77bcttUruxpY6VddcOq9anqmkg..; gsid_CTandWM=4uyq9b8017AxccgiUQbx0aVSB34; PHPSESSID=278bd598d3d063f18149842b6545435a"} # 此处填写 cookie
_page = {}  # 字典

def crawler(page):
    pageStr = '%d' %page # 将int型 page 转成字符串 
    
    payload = {'pos':'search','keyword':'扶老人','smblog':'搜微博','page':pageStr} # 为url传递参数
    # 这些数据会以键/值对的形式置于url中，跟在一个问号后面。e.g.http://weibo.cn/search/？key=value 
    #  requests 允许使用 params 关键字参数，以一个字典来提供这些参数
    
    url = 'http://weibo.cn/search/'  #此处请修改为微博搜索网址

    # 获取二进制响应
    html = requests.get(url, params = payload, cookies = cookie).content # 使用 content 时返回的是一个 byte型 数据
    # html 为一个 response对象，可以从这个对象中获取所有我们想要的信息
    # HTTP请求：get post put delete 分别对应 查 改 增 删
    
    # 获取状态码
    statusCode = requests.get(url, params = payload, cookies = cookie).status_code
    print 'page = ' + pageStr + '  HTTP状态码：' + '%d' %statusCode  # 打印状态码
    
    selector = etree.HTML(html)
    content = selector.xpath('//span[@class="ctt"]')
    
    s = 'page = ' + pageStr + '\n' + '\n'
    for each in content:
        text = each.xpath('string(.)')
        s += text + '\n' 
    s += '\n'
    _page[pageStr] = s # 把字典_page中 key=pageStr 的元素的value赋为s


thread = [] # 线程列表

# 创建线程
for i in range(1,101):    # range [1,100]
    t = threading.Thread(target=crawler,args=(i,))
    thread.append(t)

# 开始线程
for t in thread:
    t.start()

# 等待线程终止
for t in thread:
    t.join()

for each in _page:
    f1.write(_page[each])

