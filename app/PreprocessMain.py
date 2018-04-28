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

global path
global col_names
global path2
global path3
path = "./data/GPS_2016_11_01"
col_names = ["carid", "lon", "lat", "time", "device",
            "speed", "ori", "no", "notice", "card",
            "state", "color", "null"]
path2 = "./data/10000_20161101.csv"
path3 = "./static/node-way.json"


def get_mid(list_gps, flag_dict=True):

    len = list_gps.__len__()
    # mid_lon = 0.5*(arr_gps[0][0] + arr_gps[len-1][0])
    # mid_lat = 0.5*(arr_gps[0][1] + arr_gps[len-1][1])
    # p["lat"] = mid_lat
    # p["lon"] = mid_lon
    mid_pos = len/2
    r = [list_gps[mid_pos][1], list_gps[mid_pos][0]]

    if flag_dict:
        p={}
        p["lat"] = list_gps[mid_pos][1]
        p["lon"] = list_gps[mid_pos][0]
        return p
    else:
        l = [list_gps[mid_pos][1], list_gps[mid_pos][0]]
        return l


def road_mid(path, flag_dict=True):
    load_data = FileHelper.read_json(path)
    count1 = 0  # Total
    count2 = 0  # Empty
    count3 = 0  # Reminder
    list_mid = []
    list_cellid = []
    for i in load_data:
        str = u"FeatureCollection"
        count1 += 1
        tmp = []
        try:
            if i["type"] == str:
                if i["features"]:
                    # print(i["features"][0]["geometry"]["coordinates"])
                    tmp = i["features"][0]["geometry"]["coordinates"]
                else:
                    count2 += 1
            else:
                tmp = i["geometry"]["coordinates"]

            if tmp:
                arr_gps = np.array(tmp)
                mid_point = get_mid(arr_gps, flag_dict=flag_dict)
                list_mid.append(mid_point)
                if flag_dict:
                    list_cellid.append(MapHelper.get_cellid(mid_point))
                count3 += 1
        except TypeError:
            print('Json read error: '+i)

    print("Count : ")
    print(count1)
    print(count2)
    print(count3)

    dict_total = {}
    dict_total["mid"] = list_mid
    dict_total["cellid"] = list_cellid
    return dict_total


GPS_road = [[22.52579116821289, 113.98915100097656], [22.525806427001953, 113.98920440673828],
            [22.525835037231445, 113.98924255371094], [22.525875091552734, 113.98927307128906],
            [22.52594757080078, 113.9892807006836], [22.867931365966797, 113.90546417236328],
            [22.867944717407227, 113.9048843383789], [22.867963790893555, 113.904296875]]

####### Test basic function of folium #######
#MapHelper.basic_map_funs()

####### Fetch 10000 original data and pin them on shenzhen map #######
#FileHelper.split_csv(path, col_names, path2, 1000)
#MapHelper.map_cars_shenzhen(path2, col_names)

####### Calculate mid point and cellid of road and show on shenzhen map #######
#road_id = road_mid(path3, flag_dict=True)
# FileHelper.write_json(FileHelper.dict_to_geojson(road_id))

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
# kmeans = MLHelper.kmeans(road_id['mid'])
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
# FileHelper.write_csv(data=road_id["cellid"], path="./static/road_mid_point_cellid.csv")
cellid = FileHelper.read_csv(path="./static/road_mid_point_cellid.csv", col_names=['cellid'])
after_sort = cellid.sort_values(by=['cellid']).reset_index(drop=True)
split1 = after_sort.get_value(index=after_sort.__len__()/3-1, col='cellid')
split2 = after_sort.get_value(index=2*after_sort.__len__()/3-1, col='cellid')
split3 = after_sort.get_value(index=after_sort.__len__()-1, col='cellid')
list_label = TypeHelper.arr_interval_label(cellid['cellid'].tolist(), [split1, split2, split3])
labels = FileHelper.write_csv(data=list_label, path="./static/road_sort_labels.csv")
gps = FileHelper.read_csv(path="./static/road_mid_point_gps.csv", col_names=['lat', 'lon'])
labels = FileHelper.read_csv(path="./static/road_sort_labels.csv", col_names=['color'])
colors = ['green', 'blue', 'red']
list_color = []
for i in labels['color']:
    list_color.append(colors[int(i)])
DiagramsHelper.scatter(data=gps, path='./static/road_cellid_sort.jpg', color=list_color)