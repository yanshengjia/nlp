# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-02-27 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import re
import codecs
import gensim
from gensim.corpora import WikiCorpus
import logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler('./preprocess.log'),
            logging.StreamHandler()
        ])
logger = logging.getLogger('preprocess')


class Preprocess:
    def __init__(self, parent=None):
        self.parent = parent
        self.wiki_dump_path = '../../../../data/wikipedia/enwiki-latest-pages-articles.xml.bz2'
        self.wiki_text_path = '../../../../data/wikipedia/enwiki.txt'
        self.asap_tsv_path = '../../../../data/corpus/training_set_rel3.tsv'
        self.asap_text_path = '../../../../data/corpus/asap_train.txt'
        self.wiki_asap_text_path = '../../../../data/corpus/wiki_asap.txt'
    
    def dispose_wiki(self):
        logger.info('Reading wikipedia dump from: ' + self.wiki_dump_path)
        wiki = WikiCorpus(self.wiki_dump_path, lemmatize=False, dictionary={})

        with codecs.open(self.wiki_text_path, mode='a', encoding='utf8') as wiki_text_out:
            wiki_text_out.seek(0)
            wiki_text_out.truncate()
            counter = 0
            for text in wiki.get_texts():
                article = ' '.join(text).encode('ascii', 'ignore').decode('ascii') + '\n'
                wiki_text_out.write(article)
                counter += 1
                if (counter % 10000 == 0):
                    logger.info("Saved " + str(counter) + " articles")
            logger.info("Finished! Saved " + str(counter) + " articles in " + self.wiki_text_path)
    
    def clean(self, string):
        tokens = re.findall(r'\w+', string.lower())
        new_str = ' '.join(tokens)
        return new_str

    def read_asap(self):
        logger.info('Reading asap dataset from: ' + self.asap_tsv_path)
        with codecs.open(self.asap_text_path, mode='a', encoding='utf8', errors='ignore') as asap_out:
            asap_out.seek(0)
            asap_out.truncate()
            with codecs.open(self.asap_tsv_path, mode="r", encoding='utf8', errors='ignore') as asap_in:
                counter = 0
                for line in asap_in:
                    if counter == 0:
                        counter += 1
                        continue
                    tokens = line.strip().split('\t')
                    article = tokens[2].strip()
                    article = self.clean(article) + '\n'
                    counter += 1
                    asap_out.write(article)
                logger.info("Finished! Saved " + str(counter - 1) + " articles in " + self.asap_text_path)
    
    def concat(self):
        with open(self.wiki_asap_text_path, 'wb') as wfd:
            for f in [self.wiki_text_path, self.asap_text_path]:
                with open(f, 'rb') as fd:
                    shutil.copyfileobj(fd, wfd, 1024*1024*10)


def main():
    dustman = Preprocess()
    dustman.dispose_wiki()
    dustman.read_asap()

if __name__ == "__main__":
    main()