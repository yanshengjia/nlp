# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-11-17 Friday
# @email: i@yanshengjia.com

import re
import json
import codecs
from collections import Counter


class SpellChecker:
    def __init__(self, parent=None):
        self.parent = parent
        self.corpus_path = '../../data/corpus/17zuoye/raw/all.txt'
        self.lm_path = '../../data/lm/lm.json'
        self.lm = self.loadLM()
        self.word_dict = Counter(self.words(open(self.corpus_path).read()))

    def loadLM(self):
        with open(self.lm_path) as lm_json:
            lm = json.load(lm_json)
        return lm

    def words(self, text):
        return re.findall(r'\w+', text.lower())

    # ngrams (n up to 3) conditional probability of 'word' with backoff strategy
    # P(c | a b)
    # ... a b c ...
    # c: candidate, always in our word list
    # a b: words before c, may or may not in our word list
    def probability(self, c, b, a):
        abc = a + ' ' + b + ' ' + c
        ab = a + ' ' + b
        bc = b + ' ' + c

        if abc in self.lm:
            p = pow(10, float(self.lm[abc]['log_p']))
        else:
            if ab in self.lm:
                if bc in self.lm:
                    p = pow(10, float(self.lm[ab]['log_bw']) + float(self.lm[bc]['log_p']))
                else:
                    p = pow(10, float(self.lm[ab]['log_bw']) + float(self.lm[b]['log_bw']) + float(self.lm[c]['log_p']))
            else:
                if bc in self.lm:
                    p = pow(10, float(self.lm[bc]['log_p']))
                else:
                    if b in self.lm:
                        p = pow(10, float(self.lm[b]['log_bw']) + float(self.lm[c]['log_p']))
                    else:
                        p = pow(10, float(self.lm[c]['log_p']))

        return p

    # most probable spelling correction for word
    def correction(self, word, pre1, pre2):
        candidates_list = self.candidates(word)
        probability_dict = {}
        correction_str = ''

        for candidate in candidates_list:
            p = self.probability(candidate, pre1, pre2)
            probability_dict[candidate] = p

        prediction = max(probability_dict, key=probability_dict.get)
        # probability_list = sorted(probability_dict.items(), key=lambda x: x[1], reverse=True)
        # print probability_list

        # for item in probability_list:
        #     correction_str += item[0] + ' '

        return prediction

    # generate possible spelling corrections for word
    def candidates(self, word):
        return self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word))

    # the subset of `words` that appear in the dictionary of WORDS
    def known(self, words):
        return set(w for w in words if w in self.word_dict)

    # all edits that are one edit away from 'word'
    def edits1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    # all edits that are two edits away from 'word'
    def edits2(self, word):
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    # return True if the word exists in the dictionary
    def lookup(self, word):
        if word in self.word_dict:
            return True
        else:
            return False
