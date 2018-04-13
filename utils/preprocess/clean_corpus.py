# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-15 Friday
# @email: i@yanshengjia.com

import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from codecs import open
from time import time
import spacy

class Clean:
    def __init__(self, parent=None):
        self.parent = parent
        self.corpus_path = '../../data/corpus/17zuoye/raw/all.txt'
        self.output_path = '../../data/corpus/17zuoye/all_clean.txt'
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = set(stopwords.words('english'))
        self.punctuation = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

    def clean(self, doc):
        doc = self.words(doc)
        doc = self.remove_punctuation(doc)
        doc = self.length_selector(doc, 3)
        doc = self.remove_stopwords(doc)
        doc = self.lemmatize(doc)
        # doc = self.pos_filter(doc, 'NOUN')
        return doc

    def words(self, doc):
        word_list = re.findall(r'\w+', doc.lower())
        str = ' '.join(word_list)
        return str

    def remove_punctuation(self, doc):
        punc_free = ''.join(char for char in doc if char not in self.punctuation)
        return punc_free

    def length_selector(self, doc, min_len):
        len_free = ' '.join(i for i in doc.split() if len(i) >= min_len)
        return len_free

    def remove_stopwords(self, doc):
        stopwords_free = ' '.join([i for i in doc.split() if i not in self.stopwords])
        return stopwords_free
    
    def lemmatize(self, doc):
        lemmatized = ' '.join(self.lemmatizer.lemmatize(word) for word in doc.split())
        return lemmatized
    
    def pos_filter(self, doc, pos_flag):
        new_doc = self.nlp(doc)
        filtered = ' '.join(str(token) for token in new_doc if token.pos_ == pos_flag)
        return filtered

    def mincer(self):
        t0 = time()
        with open(self.corpus_path, mode='r', encoding='utf8') as corpus_file:
            with open(self.output_path, mode='a', encoding='utf8') as output_file:
                output_file.seek(0)
                output_file.truncate()
                for line in corpus_file.readlines():
                    line = line.strip()
                    if len(line.split()) != 0:
                        newline = self.clean(line)
                        if len(newline.split()) != 0:
                            output_file.write(newline + '\n')
        print("Cleaning done in %0.3fs" % (time() - t0))
    
def main():
    dustman = Clean()
    dustman.mincer()

if __name__ == "__main__":
    main()
