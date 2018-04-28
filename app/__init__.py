#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25
# @Author  : Jingwen Shi
# @File    : __init__.py.py
# @Function:

from SpatialStore import Flask
app = Flask(__name__)

from app import views
