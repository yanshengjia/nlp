# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-25 Monday
# @email: i@yanshengjia.com

import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from codecs import open
from time import time, localtime, strftime
import spacy
from collections import Counter
import multiprocessing
import logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler("../data/log/d2v_train.log"),
            logging.StreamHandler()
        ])
logger = logging.getLogger('d2v_train')

class Doc2vec:
    def __init__(self, parent=None):
        self.parent = parent
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = set(stopwords.words('english'))
        self.punctuation = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.pos_list = ['NOUN']
        self.pos_flag = False
        self.word_dict = Counter(self.words(open('../../data/corpus/big.txt').read()))
        self.prompt_path = '../data/prompt/'
        self.asap_trainset_path = '../data/trainset.txt'
        self.asap_testset_path = '../data/testset.txt'
        self.model_path = '../../data/tm/'
        self.cores = multiprocessing.cpu_count()
        self.docs = []
        self.prompts = {}
    
    def words(self, text):
        return re.findall(r'\w+', text.lower())

    def preprocess(self, doc):
        word_list = re.findall(r'\w+', doc.lower())
        known = ' '.join(word for word in word_list if word in self.word_dict)
        punc_free = ''.join(ch for ch in known if ch not in self.punctuation)
        length_free = ' '.join(i for i in punc_free.split() if len(i) >= 1)
        stop_free = ' '.join([i for i in length_free.split() if i not in self.stopwords])
        lemmatized = ' '.join(self.lemmatizer.lemmatize(word) for word in stop_free.split())
        normalized = lemmatized
        if self.pos_flag:
            new_doc = self.nlp(lemmatized)
            normalized = ' '.join(str(token) for token in new_doc if token.pos_ in self.pos_list)
        return normalized

    def read_corpus(self):
        logger.info("Loading corpus...")
        with open(self.asap_trainset_path, mode='r', encoding='utf8') as trainset:
            for line in trainset.readlines():
                tokens = line.strip().split('\t')
                essay_id = int(tokens[0])
                prompt_id = int(tokens[1])
                essay = tokens[2]
                score = float(tokens[3])
                doc = self.preprocess(essay)
                if len(doc.split()) != 0:
                    tagged_doc = TaggedDocument(doc.split(), [essay_id])
                    self.docs.append(tagged_doc)

    def train_doc2vec(self):
        logger.info("Training doc2vec model...")
        # PV-DM w/ concatenation - window=5 (both sides) approximates paper's 10-word total window size
        self.dm_concat_model = Doc2Vec(dm=1, dm_concat=1, size=100, window=5, negative=5, hs=0, min_count=2, workers=2)
        # PV-DM w/ average
        self.dm_mean_model = Doc2Vec(dm=1, dm_mean=1, size=100, window=5, negative=5, hs=0, min_count=2, workers=2)
        # PV-DBOW 
        self.dbow_model = Doc2Vec(dm=0, size=100, negative=5, hs=0, min_count=2, workers=2)
        
        self.d2v_model = self.dm_mean_model
        self.model_name = 'd2v_dm_mean.tm'
        logger.info("Model: " + self.model_name)

        self.d2v_model.build_vocab(self.docs)
        self.d2v_model.train(self.docs, total_examples=len(self.docs), epochs=100)

    def save_model(self):
        logger.info("Saving doc2vec model...")
        self.d2v_model.save(self.model_path + self.model_name)

def main():
    d2v = Doc2vec()
    d2v.read_corpus()
    d2v.train_doc2vec()
    d2v.save_model()

if __name__ == '__main__':
    main()

