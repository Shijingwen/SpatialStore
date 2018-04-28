#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25
# @Author  : Jingwen Shi
# @File    : MapHelper.py
# @Function:

import folium
import FileHelper
import s2sphere
import TypeHelper

# Tutorial from http://folium.readthedocs.io/en/latest/quickstart.html#getting-started
def basic_map_funs():
    # Default to OpenStreetMap
    map = folium.Map(location=[22.5425, 114.0545], zoom_start=14)
    # Enable lat/lng popovers
    map.add_child(folium.LatLngPopup())
    # Add a point maker
    folium.Marker([22.5401, 114.0500], popup='My point').add_to(map)
    # Add a circle maker
    folium.CircleMarker(
                    [22.5425, 114.0545],
                    radius=50,
                    popup='My circle',
                    color='#3186cc',
                    fill_color='#3186cc'
                    ).add_to(map)
    # Add a polygon maker
    folium.RegularPolygonMarker(
        [22.5300, 114.0500],
        popup='Triangle Marker',
        fill_color='#132b5e',
        number_of_sides=3,
        radius=10
        ).add_to(map)
    # Save as html
    map.save('./templates/map.html')


def map_cars(map, location):
    for index, row in location.iterrows():
        folium.Marker([row.lat, row.lon], popup='My point').add_to(map)


def map_cars_shenzhen(path, col_names):
    map = folium.Map(location=[22.5425, 114.0545], zoom_start=16)
    dataset = FileHelper.read_csv(path, col_names)
    location = dataset[["lat", "lon"]]
    map_cars(map, location)
    map.save('./templates/shenzhen_original_data_10000.html')


def pin_markers(location=[22.5425, 114.0545], zoom_start=14, add_child=True, list_dict_gps=[], label=[], w_path='./templates/map.html'):
    # Default to OpenStreetMap
    map = folium.Map(location=location, zoom_start=zoom_start)
    if add_child:
        # Enable lat/lng popovers
        map.add_child(folium.LatLngPopup())

    for i in range(list_dict_gps.__len__()):
        if i%100 == 0:
            print i
        p = [list_dict_gps[i]["lat"], list_dict_gps[i]["lon"]]
        folium.Marker(p, popup=str(label[i]), icon=folium.Icon(color='green')).add_to(map)

    # Save as html
    map.save(w_path)


def add_layer(location=[22.5425, 114.0545], zoom_start=15, add_child=False, list_json_path=['./static/node-way.json'],w_path='./templates/map.html'):
    map = folium.Map(location=location, zoom_start=zoom_start, tiles="Mapbox Bright")
    if add_child:
        # Enable lat/lng popovers
        map.add_child(folium.LatLngPopup())
    line_colors=['blue', 'green', 'red', 'yellow', 'black']
    for index,json_path in enumerate(list_json_path):
        folium.GeoJson(open(json_path).read(), name='geojson').add_to(map)
        #folium.GeoJson(open(json_path), name='geojson').add_to(map)
    map.save(w_path)


# Tutorial from https://s2sphere.readthedocs.io/en/latest/
def get_cellid(point):
    p = s2sphere.LatLng.from_degrees(point["lat"], point["lon"])
    tokens = s2sphere.CellId.from_lat_lng(p).to_token()
    return tokens