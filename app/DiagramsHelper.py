#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27
# @Author  : Jingwen Shi
# @File    : DiagramsHelper.py
# @Function:

import matplotlib.pyplot as plt
import numpy as np


def scatter(data, path, color=[]):
    X = data['lon']
    Y = data['lat']
    if color:
        c = color
    else:
        c = np.arctan2(Y, X)
    plt.scatter(X, Y, s=1, c=c, alpha=.5)
    plt.savefig(path, dpi=300)
    plt.show()
    # plt.xlim(-1.5, 1.5)
    # plt.xticks(())  # ignore xticks
    # plt.ylim(-1.5, 1.5)
    # plt.yticks(())  # ignore yticks
