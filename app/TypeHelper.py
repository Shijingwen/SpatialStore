#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26
# @Author  : Jingwen Shi
# @File    : TypeHelper.py
# @Function:


def get_basic_type(obj):
    return type(obj).__name__


def list_to_gps_list_dict(list, fist_lat=True):

    list_dict_gps = []
    for i in list:
        p={}
        if fist_lat:
            p["lat"] = i[0]
            p["lon"] = i[1]
        else:
            p["lat"] = i[1]
            p["lon"] = i[0]
        list_dict_gps.append(p)

    return  list_dict_gps


def index_it(obj = ['Adam', 'Lisa', 'Bart', 'Paul']):
    for index, name in enumerate(obj):
        print index, '-', name
    # Print Result:
    # 0 - Adam
    # 1 - Lisa
    # 2 - Bart
    # 3 - Paul


def dataframe_to_list(df, colum):
    return df[colum].values.tolist()


def arr_interval_label(arr, spliter=[]):
    label = []
    for i in arr:
        interval = 0
        for j in spliter:
            if i <= j:
                label.append(interval)
                break
            else:
                interval += 1
    return label
