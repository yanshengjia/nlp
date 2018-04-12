# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-05 Tuesday
# @email: i@yanshengjia.com

import re
import json
import codecs
from collections import Counter
from spell_chekcer import *

class Evaluator:
    def __init__(self, parent=None):
        self.parent = parent
        self.spell_checker = SpellChecker()
        self.corpus_path = '../../data/corpus/17zuoye/raw/all.txt'
        self.word_dict = Counter(self.words(open(self.corpus_path).read()))
        self.raw_path = '../data/testset/raw/raw_'
        self.essay_path = '../data/testset/essay/essay_'
        self.typo_path = '../data/testset/typo/typo_'
        self.badcase_path = '../data/badcase.txt'
        self.badcase = ""
        self.typo_counter = 0
        self.correct_counter = 0
        self.precision = 0.0

    def words(self, text):
        return re.findall(r'\w+', text.lower())

    def evaluate(self, number):
        essay_path = self.essay_path + str(number) + ".txt"
        typo_path = self.typo_path + str(number) + ".txt"
        typo_dict = {}    # {typo: true word}
        typo_quantity = 0
        correct_quantity = 0
        uncorrect_quantity = 0
        badcase = ""

        with codecs.open(typo_path, mode='r', encoding='UTF8') as typo_file:
            for line in typo_file.readlines():
                line = line.strip()
                word_typo = line.split(': ')
                word = word_typo[0]
                typo = word_typo[1]
                typo_dict[typo] = word
        
        with codecs.open(essay_path, mode='r', encoding='UTF8') as essay_file:
            essay = essay_file.read()
            word_list = self.words(essay)

            for i in range(len(word_list)):
                word = word_list[i]
                if word in typo_dict:
                    if i >= 2:
                        pre1 = word_list[i-1]
                        pre2 = word_list[i-2]
                    else:
                        pre1 = ''
                        pre2 = ''
                    typo_quantity += 1
                    correction = self.spell_checker.correction(word, pre1, pre2)

                    if correction == typo_dict[word]:
                        correct_quantity += 1
                    else:
                        uncorrect_quantity += 1
                        badcase += "typo: " + word + "    prediction: " + correction + "    true: " + typo_dict[word] + "\n"

            precision = float(correct_quantity) / float(typo_quantity)
        return badcase, typo_quantity, correct_quantity

    def batchEvaluate(self, begin, end):
        for i in range(begin, end + 1):
            badcase, typo_quantity, correct_quantity = self.evaluate(i)
            self.typo_counter += typo_quantity
            self.correct_counter += correct_quantity

            if not badcase == "":
                self.badcase += "[essay " + str(i) + "]\n" + badcase + "\n"
        self.precision = float(self.correct_counter) / float(self.typo_counter)
        with codecs.open(self.badcase_path, mode='w', encoding='UTF8') as badcase_file:
            badcase_file.write(self.badcase)

def main():
    evaluator = Evaluator()
    evaluator.batchEvaluate(1, 500)
    print "precision: " + str(evaluator.precision)
    
if __name__ == "__main__":
    main()
