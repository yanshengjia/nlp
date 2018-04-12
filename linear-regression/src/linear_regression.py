# !/usr/bin/python
# -*- coding:utf-8 -*-  
# Author: Shengjia Yan
# Date: 2017-10-30
# Email: i@yanshengjia.com
# multiple linear regression
# training set: nea/data/fold_0/train.tsv
# test set: nea/data/fold_0/test.tsv
# prompt id: 1
# score range: [2, 12]

import codecs
import nltk
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

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

def get_score_range(prompt_id):
	return asap_ranges[prompt_id]

def load_data(essay_path, ref_path, w2v_path):
    train_essays_path = essay_path + 'train_essays.txt'
    test_essays_path = essay_path + 'test_essays.txt'
    train_ref_path = ref_path + 'train_ref.txt'
    test_ref_path = ref_path + 'test_ref.txt'

    # read w2v data
    with codecs.open(w2v_path, 'r', encoding='utf8') as emb_file:
        tokens = emb_file.next().split()
        vocab_size = int(tokens[0])
        emb_dim = int(tokens[1])
        embeddings = {}
        counter = 0
        for line in emb_file:
            tokens = line.split()
            word = tokens[0]
            vec = tokens[1].split(',')
            vec = [float(x) for x in vec]
            assert len(vec) == emb_dim, 'The number of dimensions does not match the header info'
            embeddings[word] = vec
            counter += 1
        assert counter == vocab_size, 'Vocab size does not match the header info'
    
    # read y-value of training set
    with codecs.open(train_ref_path, 'r', encoding='utf8') as train_ref_file:
        train_y = train_ref_file.readlines()
        train_y = [int(x.strip('\n')) for x in train_y]

    # read y-value of test set
    with codecs.open(test_ref_path, 'r', encoding='utf8') as test_ref_file:
        test_y = test_ref_file.readlines()
        test_y = [int(x.strip('\n')) for x in test_y]
    
    # read training essays
    with codecs.open(train_essays_path, 'r', encoding='utf8') as train_essays_file:
        train_essays = train_essays_file.readlines()
        train_essays = [x.strip('\n') for x in train_essays]

    # read test essays
    with codecs.open(test_essays_path, 'r', encoding='utf8') as test_essays_file:
        test_essays = test_essays_file.readlines()
        test_essays = [x.strip('\n') for x in test_essays]

    return embeddings, train_essays, train_y, test_essays, test_y

def split_essay(essay):
    essay = essay[1:-1]
    words = nltk.word_tokenize(essay)
    words = [word.lower() for word in words]
    return words

def essay2vec(embeddings, essays):
    essay_embeddings_dict = {}   # {'essay_id':1, 'vec':[50 dim]}
    essay_embeddings_list = []
    essay_counter = 0
    for essay in essays:
        essay_id = essay_counter
        essay_vec = []
        virgin = True
        words = split_essay(essay)
        for word in words:
            if word in embeddings:
                if virgin:
                    essay_vec = embeddings[word]
                    virgin = False
                else:    
                    np.add(essay_vec, embeddings[word])
        essay_embeddings_dict[essay_id] = essay_vec
        essay_embeddings_list.append(essay_vec)
        essay_counter += 1
    return essay_embeddings_dict, essay_embeddings_list

def linear_regression(train_x, train_y, test_x, test_y):
    model = linear_model.LinearRegression()
    model.fit(train_x, train_y)
    test_y_pred = model.predict(test_x)
    coefficients = model.coef_
    mse = mean_squared_error(test_y, test_y_pred)
    variance = r2_score(test_y, test_y_pred)

    print('Coefficients: \n' + str(coefficients))
    print('Mean squared error: %.2f' % mse)
    print('Variance score: %.2f' % variance)

    return test_y_pred

def generate_contrast(output_path, test_y, test_y_pred):
    with codecs.open(output_path, 'a', encoding='utf8') as contrast_file:
        contrast_file.seek(0)
        contrast_file.truncate()
        for i in range(len(test_y)):
            string = str(test_y[i]) + ' ' + str(test_y_pred[i]) + '\n'
            contrast_file.write(string)

def main():
    essay_path = '../data/essay/'
    ref_path = '../data/ref/'
    w2v_path = '../data/embedding/word_embeddings.w2v.txt'
    e2v_path = '../data/embedding/essay_embeddings.w2v.txt'
    contrast_path = '../data/result/test_contrast.txt'
    prompt_id = 1
    low, high = get_score_range(prompt_id)
    
    embeddings, train_essays, train_y, test_essays, test_y = load_data(essay_path, ref_path, w2v_path)
    train_essays_embeddings_dict, train_essays_embeddings_list = essay2vec(embeddings, train_essays)
    test_essays_embeddings_dict, test_essays_embeddings_list = essay2vec(embeddings, test_essays)
    test_y_pred = linear_regression(train_essays_embeddings_list, train_y, test_essays_embeddings_list, test_y)
    generate_contrast(contrast_path, test_y, test_y_pred)

if __name__ == '__main__':
    main()


