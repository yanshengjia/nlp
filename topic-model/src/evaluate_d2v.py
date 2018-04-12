# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-27 Wednesday
# @email: i@yanshengjia.com

import re
import math
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from codecs import open
from time import time, localtime, strftime
import spacy
from collections import Counter
from scipy import spatial
from sklearn.metrics import mean_squared_error
import multiprocessing
import logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler("../data/log/d2v_test.log"),
            logging.StreamHandler()
        ])
logger = logging.getLogger('d2v_test')


asap_ranges = {
	0: (0, 60),
	1: (2,12),
	2: (1,6),
	3: (0,3),
	4: (0,3),
	5: (0,4),
	6: (0,4),
	7: (0,30),
	8: (0,60)
}

class Evaluate:
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
        self.model_list = ['d2v_dbow.tm', 'd2v_dm_concat.tm', 'd2v_dm_mean.tm']
        self.model_name = self.model_list[2]
        self.score_report_path = '../data/log/' + self.model_list[2] + '_score_report.txt'
        self.cores = multiprocessing.cpu_count()
        self.docs = []
        self.prompts = {}
        self.y_number = []
        self.y_true = []
        self.y_pred = []

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

    def read_prompt(self):
        logger.info("Reading prompts...")
        for i in range(1, 9):
            prompt_path = self.prompt_path + 'prompt' + str(i) + '.txt'
            with open(prompt_path, mode='r', encoding='utf8') as prompt_file:
                prompt = prompt_file.read()
                self.prompts[i] = prompt

    def normalize_score(self, score, prompt_id):
        'normalize to [0, 1]'
        low, high = asap_ranges[prompt_id]
        normalized_score = float(score - low) / (high - low)
        return normalized_score

    def load_d2v_model(self):
        logger.info("Loading d2v model...")
        self.d2v_model = Doc2Vec.load(self.model_path + self.model_name)

    def get_topic_similarity(self, doc1, doc2):
        doc1 = self.preprocess(doc1)
        doc2 = self.preprocess(doc2)
        vec1 = list(self.d2v_model.infer_vector(doc1.split()))
        vec2 = list(self.d2v_model.infer_vector(doc2.split()))
        similarity = 1.0 - spatial.distance.cosine(vec1, vec2)
        similarity = (similarity + 1.0) / 2.0   # normalize to [0, 1]
        return similarity

    def evaluate(self):
        logger.info("Evaluating...")
        counter = 0
        with open(self.asap_testset_path, mode='r', encoding='utf8') as testset:
            for line in testset.readlines():
                counter = counter + 1
                print(counter)
                tokens = line.strip().split('\t')
                essay_id = int(tokens[0])
                prompt_id = int(tokens[1])
                essay = tokens[2]
                true_label = self.normalize_score(float(tokens[3]), prompt_id)
                prompt = self.prompts[prompt_id]
                pred_label = self.get_topic_similarity(essay, prompt)
                self.y_number.append(essay_id)
                self.y_true.append(true_label)
                self.y_pred.append(pred_label)
        self.mse = mean_squared_error(self.y_true, self.y_pred)
        logger.info("mse: " + str(self.mse))
    
    def save_score_report(self):
        with open(self.score_report_path, mode='a', encoding='utf8') as report:
            report.seek(0)
            report.truncate()
            report.write("essay_id    pred    true\n")
            size = len(self.y_number)
            for i in range(size):
                info = str(self.y_number[i]) + '    ' + str(self.y_pred[i]) + '    ' + str(self.y_true[i]) + '\n'
                report.write(info)
            report.write("MSE: " + str(self.mse))

def main():
    evaluator = Evaluate()
    evaluator.read_prompt()
    evaluator.load_d2v_model()
    evaluator.evaluate()
    evaluator.save_score_report()

if __name__ == "__main__":
    main()

