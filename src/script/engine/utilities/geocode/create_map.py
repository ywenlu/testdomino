import folium
import json
import numpy as np

def get_coordinates(feature):
    coords = feature['geometry']['coordinates']
    try:
        sum(coords)
        return coords
    except:
        return [np.nan, np.nan]

    
def get_center_map(data):
    coordinates = [get_coordinates(feature) for feature in data['features']]
    coordinates = np.array(coordinates)
    center = np.nanmean(coordinates, axis = 0)
    return center[1], center[0]


def create_map(filename):
    with open(filename) as f:
        data = json.load(f)
    lat, lng = get_center_map(data)
    
    m = folium.Map(location=[lat, lng], tiles='Stamen Terrain', zoom_start=4)
    m.choropleth(geo_data=open(filename).read())
    return m

def _add_markers(m, features):
    for feature in features:
        long, lat = feature['geometry']['coordinates']
        address = feature['properties']['Response']
        folium.CircleMarker(
            location=[lat, long],
            radius=8,
            popup=address,
            weight = 2,
            color='#3186cc',
            fill=True,
            fill_color='#ff9966',
            fill_opacity = .75
        ).add_to(m)
    
def folium_map(filename):
    with open(filename) as f:
        data = json.load(f)

    features = data['features']
    lat, long = get_center_map(data)

    m = folium.Map(location=[lat, long], zoom_start=4)
    _add_markers(m, features)
    
    return m
