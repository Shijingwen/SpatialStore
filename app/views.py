#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25
# @Author  : Jingwen Shi
# @File    : views.py
# @Function:

from app import app
from flask import render_template


@app.route('/')
def hello_world():
    return render_template('index.html', name="index")

@app.route('/shenzhen/original_data_10000')
def original_data_10000():
    return render_template('shenzhen_original_data_10000.html', name="original_data_10000")

@app.route('/shenzhen/road_layer')
def road_layer():
    return render_template('shenzhen_road_layer.html', name="road_layer")

@app.route('/shenzhen/road_midgps_cellid_10000')
def road_cellid_10000():
    return render_template('shenzhen_road_midgps_cellid_10000.html', name="road_midgps_cellid_10000")

@app.route('/shenzhen/road_midgps_cellid_25285')
def road_cellid_all():
    return render_template('shenzhen_road_midgps_cellid_25285.html', name="road_midgps_cellid_25285")

@app.route('/shenzhen/road_split')
def road_split():
    return render_template('shenzhen_road_split.html', name="road_split")