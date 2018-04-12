#-*-coding:utf8-*-

import requests
from lxml import etree

url = 'http://weibo.cn/?vt=4' #此处请修改为微博地址
url_login = 'https://login.weibo.cn/login/'

html = requests.get(url).content
selector = etree.HTML(html)
password = selector.xpath('//input[@type="password"]/@name')[0]
vk = selector.xpath('//input[@name="vk"]/@value')[0]
action = selector.xpath('//form[@method="post"]/@action')[0]
print action
print password
print vk
new_url = url_login + action
data = {
    'mobile' : '15961887272',
     password : 'ysj950205',
    'remember' : 'on',
    'backURL' : 'http%3A%2F%2Fweibo.cn%2F', #此处请填写微博地址
    'backTitle' : u'微博',
    'tryCount' : '',
    'vk' : vk,
    'submit' : u'登录'
    }

newhtml = requests.post(new_url,data=data).content
new_selector = etree.HTML(newhtml)
# print newhtml.content
content = new_selector.xpath('//span[@class="ctt"]')
for each in content:
    text = each.xpath('string(.)')
    print text


