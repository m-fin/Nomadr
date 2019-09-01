from flask import redirect, render_template, request, session

import folium

import branca

import mysql.connector
import sqlite3

import os
import logging

import subprocess
import json

# Connect database
connector = sqlite3.connect('database.db')
db = connector.cursor()

def apology(message, code):
    return render_template("error.html", code=code, message=message)

def makeMap():
    # Build empty map at specified location and zoom
    # EDIT this to specify location based on user (search?)

    # map = folium.Map(location=[49.060329, -122.462227], zoom_start=6, titles="test title",width='80%', height='80%')
    # map = folium.Map(location=[49.060329, -122.462227], zoom_start=6, titles="test title",width='100%', height='100%')
    # map = folium.Map(location=[49.060329, -122.462227], zoom_start=6, titles="test title")

    # Get user location
    ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    userLocation = subprocess.check_output('curl http://api.ipstack.com/' + ip + '?access_key=27104e68a758ad15540f3065ff3254dc', shell=True)
    userLocation = json.loads(userLocation.decode("ascii"))

    if userLocation["latitude"] == None or userLocation["longitude"] == None:
        mapLatitude = 0
        mapLongitude = 0
        mapZoom = 1
    else:
        mapLatitude = userLocation["latitude"]
        mapLongitude = userLocation["longitude"]
        mapZoom = 6

    map = folium.Map(location=[mapLatitude, mapLongitude], zoom_start=mapZoom, titles="test title",width='80%', height='80%')

    locations = db.execute('SELECT * FROM locations').fetchall()

    for entry in locations:
        id = entry[0]
        datetime = entry[1]
        latitude = entry[2]
        longitude = entry[3]
        title = entry[4]
        description = entry[5]
        locType = entry[6]

        test = folium.Html("<b>" + title + "</b><br>" + description, script=True) # i'm assuming this bit runs fine
        iframe = branca.element.IFrame(html=test, width=350, height=150)
        popup = folium.Popup(iframe, parse_html=True)
        folium.Marker(location=[latitude,longitude],radius=6,color='grey',fill_color='yellow', popup=popup).add_to(map)

    map.save("maps/mapEmbed.html")

# def addToMap():

#     connector.commit()

#     # # dummy data
#     # lat = [(49.060329), (50.060329)]
#     # lon = [(-122.462227), (-123.462227)]
#     # title = [("test69696969"), ("cock")]
#     # description = [("test669699696"), ("and balls")]

#     # for lt,ln,nm,ds in zip(lat,lon,title,description):
#     #     db.execute('INSERT INTO locations (latitude, longitude, title, description) VALUES (?, ?, ?, ?)', (lt, ln, nm, ds))
#     #     # db.execute('INSERT INTO locations (lat, long) VALUES (?, ?)', (lat, lon))