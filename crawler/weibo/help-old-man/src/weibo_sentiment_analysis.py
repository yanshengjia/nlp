#! /usr/bin/env python
# -*- coding: utf-8 -*-	
# use SnowNLP to analyse weibo sentimentally

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from snownlp import SnowNLP

fin = open("helpOldman.txt","r")
fout = open("result_helpOldman.txt","w")
flabel = open("machineLabel.txt","w")

add = 0.0
average = 0.0
high = 0.0
low = 1.0
count = 1
countPositive = 0
countNegative = 0
countMiddle = 0 
ratePositive = 0.0
rateMiddle = 0.0
rateNegative = 0.0
label = []	# class label

for line in fin.readlines():
	line = line.decode('utf-8')	# utf-8 ---> unicode
	s = SnowNLP(line)
	
	fout.write("第" + str(count) + "条微博：" + '\n')
	fout.write('\n')
	
	
	fout.write('中文分词：')
	fout.write('\n')
	for each in s.words:
		fout.write(each,)
		fout.write(' ')
	fout.write('\n' + '\n')
	
	fout.write('词性标注：')
	fout.write('\n')
	for each in s.tags:
		fout.write("('" + each[0] + "','" + each[1] + "')")
		fout.write('\n')
	fout.write('\n')
	
	fout.write('拼音：')
	fout.write('\n')
	for each in s.pinyin:
		fout.write(each,)
		fout.write(' ')
	fout.write('\n' + '\n')
	
	fout.write('提取文本关键字：')
	fout.write('\n')
	for each in s.keywords(3):
		fout.write(each,)
		fout.write(' ')
	fout.write('\n' + '\n')
	
	fout.write('提取文本摘要：')
	fout.write('\n')
	for each in s.summary(3):
		fout.write(each)
		fout.write('\n')
	fout.write('\n')
	
	fout.write('分割成句子：')
	fout.write('\n')
	for each in s.sentences:
		fout.write(each)
		fout.write('\n')
	fout.write('\n')
	
	sentiment = s.sentiments
	fout.write("积极情感度：" + str(sentiment) + '\n')
	fout.write('\n' + '\n')
	
	add += sentiment
	
	# find max&min sentiment
	if sentiment > high:
		high = sentiment
	elif sentiment < low:
		low = sentiment
	
	# classify
	if sentiment > 0.6:
		countPositive += 1
		label.insert(count, 1)
	elif sentiment < 0.4:
		countNegative += 1
		label.insert(count, -1)
	else:
		countMiddle += 1
		label.insert(count, 0)
		
	count += 1	

count -= 1
ratePositive = countPositive * 100 / float(count)
rateMiddle = countMiddle * 100 / float(count)
rateNegative = countNegative * 100 / float(count)
average = add / float(count)

fout.write("微博总数：" + str(count) + "条" + '\n')
fout.write("最积极态度值：" + str(high) + '\n')
fout.write("最消极态度值：" + str(low) + '\n')
fout.write("平均态度值：" + str(average) + '\n')
fout.write("持积极态度的微博条数为：" + str(countPositive) + "条，占比" + str(ratePositive) + "%" + '\n')
fout.write("持中立态度的微博条数为：" + str(countMiddle) + "条，占比" + str(rateMiddle) + "%" + '\n')
fout.write("持消极态度的微博条数为：" + str(countNegative) + "条，占比" + str(rateNegative) + "%" + '\n')
fout.write("注：情感值∈[0,1]。情感值∈[0,0.4)，认为微博作者持消极态度；情感值∈[0.4,0.6]，中立态度；情感值∈(0.6,1]，积极态度。" + '\n')

for k, v in enumerate(label):
        flabel.write(str(v) + '\n')

# fin1 = open("humanLabel.txt",'r')
# fcompare = open("labelCompare.txt","w")

# humanLabel = []
# count = 1
# match = 0

# fcompare.write("积极态度类标为1，中立态度类标为0，消极态度类标为-1" + '\n')
# for n in fin1.readlines():
# 	humanLabel.insert(count, n)
# 	count += 1

# for i in range(1, count)
# 	if humanLabel[i] == label
fin.close()
fout.close()
flabel.close()