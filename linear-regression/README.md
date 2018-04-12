# Multiple Linear Regression

做每篇文章的 essay embeddings，用多元线性回归模型来训练数据并预测文章分数

- 将一篇文章中每个词的词向量相加，得到该文章的词向量
- 词向量的50维作为50个 x 值
- 文章的 true label 作为 y 值
- training set: nea/data/fold_0/train.tsv_
- test set: nea/data/fold_0/test.tsv
- prompt id: 1
- score range: [2, 12]
