# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-25 Monday
# @email: i@yanshengjia.com
# evaluate the performance of topic model


import re
from pprint import pprint
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import mean_squared_error
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from codecs import open
from time import time, localtime, strftime
import spacy
from scipy import spatial
from collections import Counter
import logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler("../data/log/lda_test.log"),
            logging.StreamHandler()
        ])
logger = logging.getLogger('lda_test')

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
        self.pos_flag = True
        self.word_dict = Counter(self.words(open('../../data/corpus/big.txt').read()))
        self.corpus_name = 'asap'
        self.corpus_path = '../../data/corpus/17zuoye/all_lowercase.txt'
        self.prompt_path = '../data/prompt/'
        self.asap_trainset_path = '../data/trainset.txt'
        self.asap_testset_path = '../data/testset.txt'
        self.model_path = '../../data/tm/'
        self.model_name = 'lda.tm'
        self.score_report_path = '../data/log/lda_score_report.txt'
        self.num_topics = 100
        self.prompts = {}
        self.docs = []
        self.y_number = []
        self.y_true = []
        self.y_pred = []
    
    def load_asap(self):
        logger.info("Loading asap dataset...")
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

    def load_lda_model(self):
        logger.info("Loading LDA model...")
        self.lda_model = gensim.models.ldamodel.LdaModel.load(self.model_path + self.model_name)
    
    def get_topic_similarity(self, doc1, doc2):
        doc1 = self.preprocess(doc1)
        doc2 = self.preprocess(doc2)
        bow1 = self.dictionary.doc2bow(doc1.split())
        bow2 = self.dictionary.doc2bow(doc2.split())
        vec1 = self.lda_model.get_document_topics(bow1)
        vec2 = self.lda_model.get_document_topics(bow2)
        similarity = gensim.matutils.cossim(vec1, vec2)
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
    evaluator.load_asap()
    evaluator.build_bow()
    evaluator.load_lda_model()
    evaluator.evaluate()
    evaluator.save_score_report()

if __name__ == "__main__":
    main()
    


