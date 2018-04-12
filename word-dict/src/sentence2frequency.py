# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-21 Tuesday
# @email: i@yanshengjia.com
# 将 17zuoye 的语料库中的一个句子转成单词词频序列

import re
import json
import codecs
import random
from collections import Counter

def words(text):
    return re.findall(r'\w+', text.lower())

def loadCorpus(corpus_path):
    with codecs.open(corpus_path, mode='r', encoding='UTF8') as corpus_file:
        WORDS = Counter(words(corpus_file.read()))
    
    with codecs.open(corpus_path, mode='r', encoding='UTF8') as corpus_file:
        corpus = []
        for line in corpus_file.readlines():
            line = line.strip()
            corpus.append(line)
    return WORDS, corpus

def generate_frequency(WORDS, corpus):
    size = len(corpus)
    sentence_id = random.randint(0, size-1)
    sentence = corpus[sentence_id]
    word_seg = words(sentence)
    frequency_list = []
    for word in word_seg:
        if word in WORDS:
            frequency = WORDS[word]
        else:
            frequency = 0
        frequency_list.append(frequency)
    return sentence_id, sentence, frequency_list

def main():
    corpus_path = '../../data/corpus/17zuoye/all.txt'
    WORDS, corpus = loadCorpus(corpus_path)
    sentence_id, sentence, frequency_list = generate_frequency(WORDS, corpus)
    print sentence_id
    print sentence
    print frequency_list

if __name__ == "__main__":
    main()