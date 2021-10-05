import folium

#DFW, LGA coordinates
coordinates=[(32.900908, -97.040335),(40.768571, -73.861603)]

m = folium.Map(location=[32.900908, -97.040335], zoom_start=4)

#line going from dfw to lga
aline=folium.PolyLine(locations=coordinates,weight=2,color = 'blue')
m.add_child(aline)
m.save("test.html")