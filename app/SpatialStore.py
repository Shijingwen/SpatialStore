#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25
# @Author  : Jingwen Shi
# @File    : SpatialStore.py
# @Function:

from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/shenzhen/original_data_10000')
def original_data():
    return render_template('shenzhen_original_data_10000.html', name="original_data_10000")


if __name__ == '__main__':
   app.run()
