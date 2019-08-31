import folium

import branca

map = folium.Map(location=[49.060329, -122.462227], zoom_start=6, titles="test title",width='75%', height='75%')

lat = [(49.060329)]
lon = [(-122.462227)]
title = [("test")]
description = [("test1")]

# folium.Marker(location=[49.060329, -122.462227], popup="Test").add_to(map)
for lt,ln,nm,ds in zip(lat,lon,title,description):
    test = folium.Html("<b>" + nm + "</b><br>" + ds, script=True) # i'm assuming this bit runs fine
    iframe = branca.element.IFrame(html=test, width=350, height=150)
    popup = folium.Popup(iframe, parse_html=True)
    folium.Marker(location=[lt,ln],radius=6,color='grey',fill_color='yellow', popup=popup).add_to(map)

'''
for lt,ln,nm,ds in zip(lat,lon,title,description):
    test = folium.Html('<b>nm<br>desc</b>', script=True) # i'm assuming this bit runs fine
    iframe = branca.element.IFrame(html=test, width=350, height=150)
    popup = folium.Popup(iframe, parse_html=True)
    folium.Marker(location=[lt,ln],radius=6,color='grey',fill_color='yellow', popup=popup)).add_to(map)
'''
map.save("maps/mapEmbed.html")