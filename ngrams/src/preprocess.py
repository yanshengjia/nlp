# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-29 Wednesday
# @email: i@yanshengjia.com

import re


# tokenize & lowercase
def preprocess(corpus_path, output_path):
    corpus_file = open(corpus_path, 'r')
    output_file = open(output_path, 'a')
    for line in corpus_file.readlines():
        line = line.strip()
        word_list = re.findall(r'\w+', line.lower())
        space = ' '
        string = space.join(word_list)
        output_file.write(string + '\n')

def main():
    corpus_path = '../../data/corpus/17zuoye/raw/all.txt'
    output_path = '../data/corpus/corpus.txt'
    preprocess(corpus_path, output_path)

if __name__ == "__main__":
    main()
    
    