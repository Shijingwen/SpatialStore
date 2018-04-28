#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26
# @Author  : Jingwen Shi
# @File    : PreprocessMain.py
# @Function:

import FileHelper
import MapHelper
import numpy as np
import MLHelper
import DiagramsHelper
import TypeHelper

global path_gps
global col_names
global path_gps_10000
global path_node_way
path_gps = "./data/GPS_2016_11_01"
col_names = ["carid", "lon", "lat", "time", "device",
            "speed", "ori", "no", "notice", "card",
            "state", "color", "null"]
path_gps_10000 = "./data/10000_20161101.csv"
path_node_way = "./static/node-way.json"


def get_mid(list_gps, flag_dict=True):

    len = list_gps.__len__()
    mid_pos = len/2
    split_mid = list_gps[mid_pos].split(',')
    split_num = []
    for i in split_mid:
        split_num.append(float(i))
    if flag_dict:
        p={}
        p["lat"] = split_num[1]
        p["lon"] = split_num[0]
        return p
    else:
        l = [split_num[1], split_num[0]]
        return l


def road_gps(path, wpath='./static/road_gps.txt'):
    load_data = FileHelper.read_json(path)
    count1 = 0  # Total
    count2 = 0  # Empty
    count3 = 0  # Reminder
    list_total = []
    for i in load_data:
        str_collection = u"FeatureCollection"
        count1 += 1
        tmp = []
        try:
            if i["type"] == str_collection:
                if i["features"]:
                    # print(i["features"][0]["geometry"]["coordinates"])
                    tmp = i["features"][0]["geometry"]["coordinates"]
                else:
                    count2 += 1
            else:
                tmp = i["geometry"]["coordinates"]

            if tmp:
                str_tmp = '|'.join(str(i)[1:str(i).__len__()-1] for i in tmp)
                list_total.append(str_tmp)
                count3 += 1
        except TypeError:
            print('Json read error')

    print("Count : ")
    print(count1)
    print(count2)
    print(count3)

    FileHelper.append_file(data=list_total, path=wpath)


def road_mid(rpath='./static/road_gps.txt', flag_dict=True):

    list_mid = []
    list_cellid = []
    with open(rpath, 'r') as f:
        for line in f:
            split_line = line[0:line.__len__()-1].split('|')
            mid_point = get_mid(split_line, flag_dict=flag_dict)
            list_mid.append(mid_point)
            if flag_dict:
                list_cellid.append(MapHelper.get_cellid(mid_point))

    dict_total = {}
    dict_total["mid"] = list_mid
    dict_total["cellid"] = list_cellid
    return dict_total


def link_road(rpath='./static/road_gps.txt', wpath='./static/road_relation.txt'):
    list_str_total = []
    with open(rpath, 'r') as f:
        for line in f:
            split_line = line[0:line.__len__()-1].split('|')
            list_str_total.append(split_line)

    list_relation_all= []
    for index1, i1 in enumerate(list_str_total):
        relation_one = []
        for i2 in i1:
            for index2, j1 in enumerate(list_str_total):
                for j2 in j1:
                    if index1 != index2 and i2 == j2:
                        relation_one.append(index2)
        list_relation_all.append(relation_one)
    FileHelper.append_file(data=list_relation_all, path=wpath)


def show_link(rpath1='./static/road_mid_point_gps.csv', rpath2='./static/road_relation.txt'):

    with open(rpath1, 'r') as f1, open(rpath2, 'r') as f2:
        list_relation = []
        gps = FileHelper.read_csv(path=rpath1, col_names=['lat', 'lon'])
        for i in f2:
            delete = i[1:i.__len__()-2]
            if delete != '':
                # Remove[] of txt and transform str list into int.
                list_int = TypeHelper.str_to_int(delete.split(','))
            else:
                list_int.append(int(-1))
            list_relation.append(list_int)
        DiagramsHelper.link(data=gps, relation=list_relation, path='./static/road_relation.jpg')


GPS_road = [[22.52579116821289, 113.98915100097656], [22.525806427001953, 113.98920440673828],
            [22.525835037231445, 113.98924255371094], [22.525875091552734, 113.98927307128906],
            [22.52594757080078, 113.9892807006836], [22.867931365966797, 113.90546417236328],
            [22.867944717407227, 113.9048843383789], [22.867963790893555, 113.904296875]]

####### Test basic function of folium #######
#MapHelper.basic_map_funs()

####### Fetch 10000 original data and pin them on shenzhen map #######
# FileHelper.split_csv(path_gps, col_names, path_gps_10000, 1000)
# MapHelper.map_cars_shenzhen(path_gps_10000, col_names)

####### Calculate mid point and cellid of road and show on shenzhen map #######
# road_gps(path=path_node_way, wpath='./static/road_gps.txt')
# road_id = road_mid(rpath='./static/road_gps.txt', flag_dict=True)
# FileHelper.write_json(context=FileHelper.dict_to_geojson(road_id), path="./static/road_mid_cellid_string.json")

####### Add road layer on map #######
# MapHelper.pin_markers(list_dict_gps=road_id["mid"][0:10000], label=road_id["cellid"][0:10000],
#                       w_path='./templates/shenzhen_road_midgps_cellid_10000.html')
# MapHelper.pin_markers(list_dict_gps=road_id["mid"], label=road_id["cellid"],
#                       w_path='./templates/shenzhen_road_midgps_cellid_25285.html')

# list_json_path=['./static/road_mid_cellid_string.json']
# w_path='./templates/shenzhen_road_midgps_cellid_layer.html'
# list_json_path=['./static/node-way.json']
# w_path='./templates/shenzhen_road.html'
# MapHelper.add_layer(list_json_path=list_json_path, w_path=w_path)

####### Use Kmeans to class road net #######
# kmeans = MLHelper.kmeans(road_id['mid'])  # Set flag_dict=False
# FileHelper.write_csv(data=kmeans['label'], path="./static/road_kmeans_labels.csv")
# FileHelper.write_csv(data=kmeans['centroids'], path="./static/road_kmeans_centers.csv")
# FileHelper.append_file(data=kmeans['inertia'], path="./static/road_kmeans_inertia.txt")
# print ('Finish Kmeans!')

####### Show Kmeans class result #######
# FileHelper.write_csv(data=road_id['mid'], path="./static/road_mid_point_gps.csv")
# gps = FileHelper.read_csv(path="./static/road_mid_point_gps.csv", col_names=['lat', 'lon'])
# labels = FileHelper.read_csv(path="./static/road_kmeans_labels.csv", col_names=['color'])
# colors = ['green', 'blue', 'red']
# list_color = []
# for i in labels['color']:
#     list_color.append(colors[int(i)])
# DiagramsHelper.scatter(data=gps, path='./static/road_kmeans.jpg', color=list_color)

####### Show Hilbert average class result #######
# FileHelper.write_csv(data=road_id["cellid"], path="./static/road_mid_point_cellid.csv") # Set flag_dict=True
# cellid = FileHelper.read_csv(path="./static/road_mid_point_cellid.csv", col_names=['cellid'])
# after_sort = cellid.sort_values(by=['cellid']).reset_index(drop=True)
# split1 = after_sort.get_value(index=after_sort.__len__()/3-1, col='cellid')
# split2 = after_sort.get_value(index=2*after_sort.__len__()/3-1, col='cellid')
# split3 = after_sort.get_value(index=after_sort.__len__()-1, col='cellid')
# list_label = TypeHelper.arr_interval_label(cellid['cellid'].tolist(), [split1, split2, split3])
# labels = FileHelper.write_csv(data=list_label, path="./static/road_sort_labels.csv")
# gps = FileHelper.read_csv(path="./static/road_mid_point_gps.csv", col_names=['lat', 'lon'])
# labels = FileHelper.read_csv(path="./static/road_sort_labels.csv", col_names=['color'])
# colors = ['green', 'blue', 'red']
# list_color = []
# for i in labels['color']:
#     list_color.append(colors[int(i)])
# DiagramsHelper.scatter(data=gps, path='./static/road_cellid_sort.jpg', color=list_color)

####### Build road link relation #######
# link_road(rpath='./static/road_gps.txt', wpath='./static/road_relation.txt')
show_link(rpath1='./static/road_mid_point_gps.csv', rpath2='./static/road_relation.txt')