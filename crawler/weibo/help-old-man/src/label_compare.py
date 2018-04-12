#! /usr/bin/env python
# -*- coding: utf-8 -*-	
# use SnowNLP to analyse weibo sentimentally

import sys
reload(sys)
sys.setdefaultencoding('utf8')

fin1 = open("humanLabel.txt",'r')	# humanLabel
fin2 = open("machineLabel.txt",'r')	# machineLabel
fcompare = open("result_labelCompare.txt","w")

humanLabel = {}
machineLabel = {}
match = {}
success = 0
count = 1
accuracy = 0.0

fcompare.write("积极态度类标为1，中立态度类标为0，消极态度类标为-1" + '\n')
fcompare.write("微博 	      人工类标 机器类标 匹配情况" + '\n')
for n in fin1.readlines():
	n = n.strip('\n')
	humanLabel[count] = n
	m = fin2.readline()
	m = m.strip('\n')
	machineLabel[count] = m
	count += 1

for k in range(1,count):
	if humanLabel[k] == machineLabel[k]:
		match[k]='Y'
		success += 1
	else:
		match[k]='N'
	fcompare.write(str(k) + '	 		' + str(humanLabel[k]) + ' 		' + str(machineLabel[k]) + ' 		' + str(match[k]) + '\n')

accuracy = float(success) * 100 / len(humanLabel)
fcompare.write("匹配成功：" + str(success) + "对，准确率" + str(accuracy) + "%")

