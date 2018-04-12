# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-21 Thursday
# @email: i@yanshengjia.com
# split ASAP (https://www.kaggle.com/c/asap-aes) dataset to trainset and testset (8:2)

from codecs import open
from pprint import pprint
import random


class ASAPReader:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = '../../data/asap/training_set_rel3.tsv'
        self.trainset_path = '../data/trainset.txt'
        self.testset_path = '../data/testset.txt'
        self.trainset_doc = ""
        self.testset_doc = ""
        self.trainset_counter = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }
        self.testset_counter = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }

    def read_asap_dataset(self):
        with open(self.file_path, mode='r', encoding='utf8', errors='ignore') as input_file:
            input_file.next()
            for line in input_file:
                tokens = line.strip().split('\t')
                essay_id = int(tokens[0])
                essay_set = int(tokens[1])
                essay = tokens[2].strip()
                score = float(tokens[6])
                dice = random.randint(1, 10)
                if dice <= 2:
                    self.testset_doc = str(essay_id) + '\t' + str(essay_set) + '\t' + essay + '\t' + str(score) + '\n'
                    self.testset_counter[0] += 1
                    self.testset_counter[essay_set] += 1
                    self.save_testset()
                else:
                    self.trainset_doc = str(essay_id) + '\t' + str(essay_set) + '\t' + essay + '\t' + str(score) + '\n'
                    self.trainset_counter[0] += 1
                    self.trainset_counter[essay_set] += 1
                    self.save_trainset()

    def save_trainset(self):
        with open(self.trainset_path, mode='a', encoding='utf8', errors='ignore') as output_file:
            output_file.write(self.trainset_doc)

    def save_testset(self):
        with open(self.testset_path, mode='a', encoding='utf8', errors='ignore') as output_file:
            output_file.write(self.testset_doc)
    
    def print_dataset_info(self):
        print "Trainset:"
        pprint(self.trainset_counter, width=1)
        print "Testset:"
        pprint(self.testset_counter, width=1)


def main():
    asap_reader = ASAPReader()
    asap_reader.read_asap_dataset()
    asap_reader.print_dataset_info()

if __name__ == '__main__':
    main()