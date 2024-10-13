import folium
import folium.features
from folium import plugins
import json
import os
from datetime import datetime
import time

from helpers.log import logger

basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = False,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = False,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = False,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite Hybrid',
        overlay = False,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
    )
}

def get_color(r,g,b):
    return f"#{min(255,max(0,int(r))):02X}{min(255,max(0,int(g))):02X}{min(255,max(0,int(b))):02X}"

def create_map_all_walks():
    start_time = time.time()

    draw_markers = False
    
    map = folium.Map(
        location=(47.6971, 10.3167),
        zoom_start=13,
        # tiles=basemaps["Google Satellite Hybrid"],
        # max_zoom=10,
        control_scale=True,
        prefer_canvas=False,
    )

    # add maps
    folium.TileLayer("OpenStreetMap").add_to(map)
    basemaps["Google Terrain"].add_to(map)
    basemaps["Google Satellite Hybrid"].add_to(map)

    walk_config = {}
    if os.path.exists("data/walk_config.json"):
        with open("data/walk_config.json", "r") as file:
            walk_config = json.load(file)

    excluded_walks_group = folium.FeatureGroup(name='Excluded walks', show=False).add_to(map)
    included_walks_group = folium.FeatureGroup(name='Walks', show=True).add_to(map)
    for timestamp, config in walk_config.items():
        if not os.path.exists(f"data/walks/{timestamp}.json"):
            logger.error(f"Walk {timestamp}.json does not exist!")
            continue

        with open(f"data/walks/{timestamp}.json", "r") as file:
            walk_data = json.load(file)
        
        walk_group = folium.FeatureGroup(name=config["name"])
        walk_lines = folium.PolyLine(locations=[[coord["latitude"], coord["longitude"]] for coord in walk_data["data"]], 
                                     color=config["color"], 
                                     weight=3, 
                                     tooltip=config["name"])
        walk_lines.add_to(walk_group)

        # marker at start and end
        if draw_markers:
            starttime = datetime.datetime.fromtimestamp(walk_data["data"][0]["timestamp"]/1000)
            starttime = starttime.strftime("%d.%m.%Y - %H:%M:%S")
            duration = datetime.timedelta(milliseconds=walk_data["duration"])
            folium.Marker([walk_data["data"][0]["latitude"], walk_data["data"][0]["longitude"]], popup=f"Start: {starttime}", icon=folium.Icon(color='green')).add_to(walk_group)
            folium.Marker([walk_data["data"][-1]["latitude"], walk_data["data"][-1]["longitude"]], popup=f"End: ", icon=folium.Icon(color='red')).add_to(walk_group)


        if config["included"]:
            walk_group.add_to(included_walks_group)
        else:
            walk_group.add_to(excluded_walks_group)


    folium.LayerControl(collapsed=True).add_to(map)
    map.save("data/webMap.html")

    logger.info(f"Map created in {time.time()-start_time:.2f}s")
        


def create_map_one_walk(walk_data):
    
    start_time = time.time()

    draw_markers = True
    
    map = folium.Map(
        location=(47.6971, 10.3167),
        zoom_start=13,
        # tiles=basemaps["Google Satellite Hybrid"],
        # max_zoom=10,
        control_scale=True,
        prefer_canvas=False,
    )

    # add maps
    folium.TileLayer("OpenStreetMap").add_to(map)
    basemaps["Google Terrain"].add_to(map)
    basemaps["Google Satellite Hybrid"].add_to(map)

    config = {"name": str(walk_data["start_time"]), "included": True, "color": get_color(255,0,0)}
    if os.path.exists("data/walk_config.json"):
        with open("data/walk_config.json", "r") as file:
            walk_config = json.load(file)
            if walk_data["start_time"] in walk_config:
                config = walk_config[walk_data["start_time"]]

    walk_lines = folium.PolyLine(locations=[[coord["latitude"], coord["longitude"]] for coord in walk_data["data"]], 
                                color=config["color"], 
                                weight=3, 
                                tooltip=config["name"])
    walk_lines.add_to(map)

    starttime = datetime.datetime.fromtimestamp(walk_data["data"][0]["timestamp"]/1000)
    starttime = starttime.strftime("%d.%m.%Y - %H:%M:%S")
    duration = datetime.timedelta(milliseconds=walk_data["duration"])
    folium.Marker([walk_data["data"][0]["latitude"], walk_data["data"][0]["longitude"]], popup=f"Start: {starttime}", icon=folium.Icon(color='green')).add_to(map)
    folium.Marker([walk_data["data"][-1]["latitude"], walk_data["data"][-1]["longitude"]], popup=f"End: ", icon=folium.Icon(color='red')).add_to(map)


    folium.LayerControl(collapsed=True).add_to(map)
    map.save(f"data/walkMaps/{walk_data['start_time']}.html")

    logger.info(f"Map for {walk_data['start_time']} created in {time.time()-start_time:.2f}s")