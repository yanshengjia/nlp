# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-21 Tuesday
# @email: i@yanshengjia.com
# 将 17zuoye 的语料库中的一个句子转成单词编号列表

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
        word_list = sorted(WORDS.items(), key=lambda x: x[1], reverse=True)
        reversed_word_list = []
        for word in word_list:
            reversed_word_list.append(word[0])
    
    with codecs.open(corpus_path, mode='r', encoding='UTF8') as corpus_file:
        corpus = []
        for line in corpus_file.readlines():
            line = line.strip()
            corpus.append(line)
    return WORDS, reversed_word_list, corpus

def generate_index(WORDS, word_list, corpus):
    size = len(corpus)
    sentence_id = random.randint(0, size-1)
    sentence = corpus[sentence_id]
    word_seg = words(sentence)
    index_list = []
    for word in word_seg:
        if word in WORDS:
            index = word_list.index(word)
        else:
            index = size
        index_list.append(index)
    return sentence_id, sentence, index_list

def main():
    corpus_path = '../../data/corpus/17zuoye/all.txt'
    WORDS, word_list, corpus = loadCorpus(corpus_path)
    sentence_id, sentence, index_list = generate_index(WORDS, word_list, corpus)
    print sentence_id
    print sentence
    print index_list

if __name__ == "__main__":
    main()