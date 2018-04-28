#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25
# @Author  : Jingwen Shi
# @File    : FileHelper.py
# @Function:

import pandas as pd
import json
import chardet


# Open .csv-like file and load into DataFrame
def read_csv(path, col_names):
    try:
        if col_names:
            data = pd.DataFrame(pd.read_csv(path, names=col_names, index_col=False))
        else:
            data = pd.DataFrame(pd.read_csv(path, index_col=False))
        return data
    except IOError:
        print 'File is not accessible or not found!'
        return


# Splite.csv-like file accroding to assigned line number
def split_csv(path, col_names, write_path, num_rows):
    try:
        data = pd.DataFrame(pd.read_csv(path, names=col_names, nrows=num_rows))
        data.to_csv(write_path, index=False, header=False)
    except IOError:
        print 'File is not accessible or not found!'


def write_csv(data, path, sep=','):
    pd_data = pd.DataFrame(data)
    pd_data.to_csv(path, sep=sep, index_label=False, index=False, header=False)


# Open .json-like file and load into DataFrame
def read_json(path):
    with open(path, 'r') as f:
        load_dict = json.load(f)
        print("This file is encoded in :")
        print(type(load_dict["type"]))
        return load_dict["features"]


# Transfer data to geo json point format
#dict_data = {"cellid":{}, "mid":{"lat":,"lon":}}
def dict_to_geojson(dict_data,  type='LineString'):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for i in range(len(dict_data["mid"])):
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': type,
                               'coordinates': []}}
        feature['geometry']['coordinates'] = [dict_data["mid"][i]["lon"], dict_data["mid"][i]["lat"]]
        feature['properties'] = {"cellid": str(dict_data["cellid"][i])}
        geojson['features'].append(feature)
    return geojson


def write_json(context, path):
    with open(path, "w") as f:
        json.dump(context, f)
        print("Write to :"+path)


def notice_write(path, string='',format=''):
    print("Write"+string+" into:" + path)
    if format:
        print("Every line represents gps list of a road segment. Format:")
        print(format)


def append_file(data, path, notice=True):
    dtype = type(data).__name__
    with open(path, 'a') as f:
        if dtype == 'list' or dtype == 'dict':
            for i in data:
                f.write(str(i))
                f.write('\n')
            if notice:
                notice_write(path=path, format=data[0])
        else:
            f.write(str(data))
            f.write('\n')
            if notice:
                notice_write(path=path)

