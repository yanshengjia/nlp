# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-02-27 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import codecs
import multiprocessing
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences
import logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler("./w2v.log"),
            logging.StreamHandler()
        ])
logger = logging.getLogger('w2v')


class W2V:
    def __init__(self, parent=None):
        self.parent = parent
        self.emb_dim = 200
        self.wiki_text_path = '../../../../data/wikipedia/enwiki.txt'
        self.asap_text_path = '../../../../data/corpus/asap_train.txt'
        self.w2v_corpus_path = '../../../../data/corpus/w2v/'
        self.w2v_model_path = '../../../../data/model/w2v/wiki.en.' + str(self.emb_dim) + '.model'
        self.w2v_vector_path = '../../../../data/model/w2v/wiki.en.' + str(self.emb_dim) + '.vector'
        self.sentences = []
    
    def read_articles(self):
        total = 0
        with codecs.open(self.wiki_text_path, mode="r", encoding='utf8', errors='ignore') as wiki_in:
            logger.info('Reading wiki articles from: ' + self.wiki_text_path)
            wiki_counter = 0
            for line in wiki_in:
                self.sentences.append(line.strip().split())
                wiki_counter += 1
                total += 1
            logger.info('   Done! ' + str(wiki_counter) + ' wiki articles')
        
        with codecs.open(self.asap_text_path, mode="r", encoding='utf8', errors='ignore') as asap_in:
            logger.info('Reading asap training articles from: ' + self.asap_text_path)
            asap_counter = 0
            for line in asap_in:
                self.sentences.append(line.strip().split())
                asap_counter += 1
                total += 1
            logger.info('   Done! ' + str(asap_counter) + ' wiki articles')
            logger.info('Total ' + str(total) + ' articles')

    def train_w2v(self):
        logger.info('Traing w2v model...')
        # CBOW
        model = Word2Vec(PathLineSentences(self.w2v_corpus_path), sg=1, size=self.emb_dim, window=5, min_count=5, workers=multiprocessing.cpu_count()/12)
        model.save(self.w2v_model_path)
        model.wv.save_word2vec_format(self.w2v_vector_path, binary=False)

def main():
    trainer = W2V()
    # trainer.read_articles()
    trainer.train_w2v()

if __name__ == '__main__':
    main()