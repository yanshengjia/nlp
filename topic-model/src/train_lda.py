# !/usr/bin/python
# -*- coding:utf-8 -*-
# @author: Shengjia Yan
# @date: 2017-12-13 Wednesday
# @email: i@yanshengjia.com

import re
from pprint import pprint
from sklearn.datasets import fetch_20newsgroups
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from codecs import open
from time import time, localtime, strftime
import spacy
from collections import Counter
import logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler("../data/log/lda_train.log"),
            logging.StreamHandler()
        ])
logger = logging.getLogger('lda_train')

class LDA:
    def __init__(self, parent=None):
        self.parent = parent
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = set(stopwords.words('english'))
        self.punctuation = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.pos_list = ['NOUN']
        self.pos_flag = True
        self.word_dict = Counter(self.words(open('../../data/corpus/big.txt').read()))
        self.corpus_name = 'asap'
        self.corpus_path = '../../data/corpus/17zuoye/all_lowercase.txt'
        self.prompt_path = '../data/prompt/'
        self.asap_trainset_path = '../data/trainset.txt'
        self.asap_testset_path = '../data/testset.txt'
        self.model_path = '../../data/tm/'
        self.model_name = 'lda.tm'
        self.prompts = {}
        self.docs = []      # [doc0, doc1, doc2, ...]    doc0: [word0, word1, word2, ...]

    def load_corpus(self):
        logger.info("Loading 17zuoye dataset...")
        with open(self.corpus_path, mode='r', encoding='utf8') as corpus_file:
            for line in corpus_file.readlines():
                line = line.strip()
                doc = self.preprocess(line)
                if len(doc.split()) != 0:
                    self.docs.append(doc.split())

    def load_20news(self):
        logger.info("Loading 20newsgroups dataset...")
        self.newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
        self.newsgroups_test = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'))
        pprint(list(self.newsgroups_train.target_names))
        logger.info(str(self.newsgroups_train.target_names))

        for doc in self.newsgroups_train.data:
            doc = self.preprocess(doc)
            if len(doc.split()) != 0:
                self.docs.append(doc.split())

    def load_asap(self):
        logger.info("Loading ASAP dataset...")
        with open(self.asap_trainset_path, mode='r', encoding='utf8') as train_file:
            for line in train_file.readlines():
                tokens = line.strip().split('\t')
                essay_id = int(tokens[0])
                essay_set = int(tokens[1])
                essay = tokens[2]
                score = float(tokens[3])
                doc = self.preprocess(essay)
                if len(doc.split()) != 0:
                    self.docs.append(doc.split())

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

    def words(self, text):
        return re.findall(r'\w+', text.lower())

    def build_bow(self):
        logger.info("Building bow...")
        self.dictionary = corpora.Dictionary(self.docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.docs]

    def train_lda(self):
        logger.info("Training LDA model...")
        t0 = time()
        self.num_topics = 100
        self.update_every = 1
        self.chunksize = 10000
        self.iteration = 50
        self.random_state = 0
        logger.info("[LDA] topics: %d, iterations: %d, random state: %d" % (self.num_topics, self.iteration, self.random_state))
        lda = gensim.models.ldamodel.LdaModel
        self.lda_model = lda(corpus=self.corpus, id2word=self.dictionary, num_topics=self.num_topics, update_every=self.update_every, chunksize=self.chunksize, passes=self.iteration, random_state=self.random_state)
        logger.info("LDA training cost %0.3fs" % (time() - t0))
        logger.info("num_topics: " + str(self.num_topics) + "  passes: " + str(self.iteration) + "  random_state: " + str(self.random_state))

    def print_topics(self):
        topics = "Topics:\n"
        self.topics = self.lda_model.print_topics(num_topics=-1, num_words=20)
        for topic in self.topics:
            topics += str(topic) + '\n'
        logger.info(topics)
        return topics

    def print_topic(self, n):
        logger.info(lda.print_topic(n))

    def save_model(self):
        self.lda_model.save(self.model_path + self.model_name)

    def load_model(self):
        self.lda_model = gensim.models.ldamodel.LdaModel.load(self.model_path + self.model_name)

    def get_doc_topics(self, raw_doc):
        logger.info("doc: " + raw_doc)
        doc = self.preprocess(raw_doc)
        bow = self.dictionary.doc2bow(doc.split())
        topic_distribution = self.lda_model.get_document_topics(bow)
        logger.info("topic_distribution: " + str(topic_distribution) + "\n")
        return topic_distribution

    def get_topic_similarity(self, doc1, doc2):
        doc1 = self.preprocess(doc1)
        doc2 = self.preprocess(doc2)
        bow1 = self.dictionary.doc2bow(doc1.split())
        bow2 = self.dictionary.doc2bow(doc2.split())
        vec1 = self.lda_model.get_document_topics(bow1)
        vec2 = self.lda_model.get_document_topics(bow2)
        similarity = gensim.matutils.cossim(vec1, vec2)
        return similarity

def main():
    topic_modeler = LDA()
    topic_modeler.load_asap()
    topic_modeler.build_bow()
    topic_modeler.train_lda()
    topic_modeler.print_topics()
    topic_modeler.save_model()

if __name__ == "__main__":
    main()