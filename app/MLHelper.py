#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27
# @Author  : Jingwen Shi
# @File    : MLHelper.py
# @Function: Machine Learning

from sklearn.cluster import KMeans


def kmeans(data, n_clusters=3):
    estimator = KMeans(n_clusters=n_clusters, max_iter=10000)  # Build a cluster
    estimator.fit(data)  # Fit in data
    result={}
    result['label'] = estimator.labels_  # Fetch label
    result['centroids'] = estimator.cluster_centers_  # Fetch the centers
    result['inertia'] = estimator.inertia_
    return result
# sklearn.cluster.KMeans(
#     n_clusters=8,
#     init='k-means++',
#     n_init=10,
#     max_iter=300,
#     tol=0.0001,
#     precompute_distances='auto',
#     verbose=0,
#     random_state=None,
#     copy_x=True,
#     n_jobs=1,
#     algorithm='auto'
#     )
