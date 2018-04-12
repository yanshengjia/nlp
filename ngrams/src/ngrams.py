# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-23 Thursday
# @email: i@yanshengjia.com

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
import codecs
import json
import re


def ngrams_nltk(text, n):
  # token = nltk.word_tokenize(text.lower())    # too slow
  token = re.findall(r'\w+', text.lower())
  n_grams = ngrams(token, n)
  return dict(Counter(n_grams))

def ngrams_pure(text, n):
  token = re.findall(r'\w+', text.lower())
  n_grams = []
  for i in range(len(token)-n+1):
    n_grams.append(tuple(token[i:i+n]))
  return dict(Counter(n_grams))

def main():
  text = "I need to write a program in NLTK that breaks a corpus (a large collection of txt files) into unigrams, bigrams, trigrams, fourgrams and fivegrams. I need to write a program in NLTK that breaks a corpus"
  corpus_path = '../../spell-checker/data/big.txt'
  bigrams_path = '../../n-grams/data/count/bigrams.txt'
  trigrams_path = '../../n-grams/data/count/trigrams.txt'

  with open(corpus_path, 'r') as corpus_file:
    text = corpus_file.read()
    bigrams = ngrams_pure(text, 2)
    trigrams = ngrams_pure(text, 3)
    pre1 = 'little'
    pre2 = 'note'
    biwords = (pre1, pre2)
    print bigrams[biwords]
    print sum(bigrams.values())
    print sum(trigrams.values())
    print len(bigrams)
    print len(trigrams)

  # with open(bigrams_path, 'w') as bigrams_file:
  #   bigrams = json.dumps(str(bigrams), ensure_ascii=False)
  #   bigrams_file.write(bigrams)
  
  # with open(trigrams_path, 'w') as trigrams_file:
  #   trigrams = json.dumps(str(trigrams), ensure_ascii=False)
  #   trigrams_file.write(trigrams)

if __name__ == "__main__":
  main()
