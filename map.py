import folium
from flask import Flask,request,make_response
import pyproj
from main import draw
import numpy as np
import webbrowser

app = Flask(__name__)

proj = pyproj.Proj(proj = 'tmerc',lon_0 = 116,lat_0 = 40,preserve_units = False)
points = []      #变换后边界点
pre_points = []  #原边界点

# m = folium.Map(location=[40,116],zoom_start=13,)
# folium.Marker(
#     location=[39.95, 115.33],
#     popup='Mt. Hood Meadows',
#     icon=folium.Icon(icon='cloud')
# ).add_to(m)
# m.add_child(folium.LatLngPopup())
# m.save("index.html")

@app.route('/get_pointer')
def resp():
    response = make_response('sucess')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    point = request.args.get('point').split(',')
    lat = float(point[0])
    lng = float(point[1])

    print(proj(lng,lat))
    points.append(np.array(proj(lng,lat)))

    pre_points.append([lat,lng])
    return  response

@app.route('/draw')
def resp_draw():
    response = make_response('sucess')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    draw_points = draw(points)
    m = folium.Map(location=[40,116],zoom_start=13,)

    for j in range(0,len(pre_points)-1):
        folium.PolyLine(
            locations=[[pre_points[j][0],pre_points[j][1]], [pre_points[j+1][0],pre_points[j+1][1]]],
            icon=folium.Icon(color='red')
        ).add_to(m)

    folium.PolyLine(
        locations=[[pre_points[0][0],pre_points[0][1]], [pre_points[len(pre_points)-1][0],pre_points[len(pre_points)-1][1]]],
        icon=folium.Icon(color='red')
    ).add_to(m)

    for i in range(0,len(draw_points)):
        reverse = proj(draw_points[i][0],draw_points[i][1],inverse = True)
        folium.Marker(
            location=[reverse[1],reverse[0] ],
            icon=folium.Icon(color = 'red')
        ).add_to(m)

        if i > 1:
            reverse_last = proj(draw_points[i-1][0],draw_points[i-1][1],inverse = True)
            folium.PolyLine(
                locations=[[reverse_last[1],reverse_last[0]],[reverse[1],reverse[0]]],
                color='blue'
            ).add_to(m)

    m.save("test_draw.html")
    webbrowser.open("test_draw.html")

    return m._repr_html_()

if __name__ == '__main__':
    app.debug = True
    app.run()