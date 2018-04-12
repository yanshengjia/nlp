# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-15 Friday
# @email: i@yanshengjia.com

from sklearn.cluster import KMeans
import numpy as np

def kmeans():
    X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    kmeans.labels_
    # array([0, 0, 0, 1, 1, 1], dtype=int32)
    kmeans.predict([[0, 0], [4, 4]])
    # array([0, 1], dtype=int32)
    kmeans.cluster_centers_
    # array([[ 1.,  2.], [ 4.,  2.]])

def main():
    kmeans()

if __name__ == "__main__":
    main()