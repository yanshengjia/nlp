# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-20 Monday
# @email: i@yanshengjia.com

import re
import json
import codecs
from collections import Counter

def words(text):
    return re.findall(r'\w+', text.lower())

def loadCorpus(corpus_path):
    with codecs.open(corpus_path, mode='r', encoding='UTF8') as corpus_file:
        WORDS = Counter(words(corpus_file.read()))
    return WORDS

def saveDict(dict_path, dict):
    with codecs.open(dict_path, mode='w', encoding='UTF8') as dict_file:
        dict = json.dumps(dict, ensure_ascii=False)
        dict_file.write(dict)

def saveList(list_path, dict):
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    with codecs.open(list_path, mode='w', encoding='UTF8') as list_file:
        dict = json.dumps(dict, ensure_ascii=False)
        list_file.write(dict)

def P(word, WORDS):
    N=sum(WORDS.values())
    return WORDS[word] / float(N)

def main():
    corpus_path = '../data/big.txt'
    dict_path = '../data/word_dict.txt'
    list_path = '../data/word_list.txt'
    WORDS = loadCorpus(corpus_path)
    saveList(list_path, WORDS)
    saveDict(dict_path, WORDS)

    # print len(WORDS)
    # print sum(WORDS.values())
    # print WORDS.most_common(10)
    # print P('the', WORDS)

if __name__ == '__main__':
    main()
