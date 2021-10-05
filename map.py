import folium
from flask import Flask,request,make_response

app = Flask(__name__)

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
    lon = float(point[0])
    lat = float(point[1])
    print(lat,lon)
    return  response

if __name__ == '__main__':
    app.debug = True
    app.run()