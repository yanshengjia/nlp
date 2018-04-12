# Word2Vec for NEA

Train better word embeddings for NEA.

## Approach

1. Train a new w2v model

   1. Build a new corpus based on wikipedia English articles [data](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2) and ASAP [dataset](https://www.kaggle.com/c/asap-aes/data)
   2. Preprocess
   3. Train a new w2v model by [gensim](https://radimrehurek.com/gensim/models/word2vec.html)

2. Fine-tune pre-trained word vectors

   1. Use ASAP dataset to fine-tune fastText pre-trained English [word vectors](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.vec)

   ​