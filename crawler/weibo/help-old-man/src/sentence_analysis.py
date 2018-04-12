#! /usr/bin/env python
# -*- coding: utf-8 -*-	


from snownlp import SnowNLP

s = SnowNLP(u':#微感动#【一次搀扶，四载照顾[心]】路遇一摔倒老人蜷缩在地，她将老人扶起送回家。不放心老人她次日再去拜访，得知老人孤身一人后从此义务照顾！每天看望，帮洗衣服，陪着聊天…她坚持至今4年！她说当下好多人不敢扶老人，想用行动改变大家看法！31岁山西籍好人赵艳善心无畏惧[赞]（央视记者杨晓东）')

print '中文分词：'
for each in s.words:
	print each,
print '\n'

print '词性标注：'
for each in s.tags:
	print "('" + each[0] + "','" + each[1] + "')"
print '\n'

print '拼音：'
for each in s.pinyin:
	print each,
print '\n'

print '提取文本关键字：'
for each in s.keywords(3):
	print each,
print '\n'

print '提取文本摘要：'
for each in s.summary(3):
	print each
print '\n'

print '分割成句子：'
for each in s.sentences:
	print each
print '\n'

	
print "积极情感度：" + str(s.sentiments) + '\n'


	