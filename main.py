import folium
import cv2
import numpy as np
from math import atan2,sin,cos

def angle(point_1,point_2):
    if point_1[1] == point_2[1] == 0:
        return 0
    return atan2(point_2[1] - point_1[1],point_2[0] - point_1[0])

def ifjoin(point,cnt):
    pass

border = np.array([[0, 0], [-0.5,0.1],[-1, 1.1], [0,2],[0.5,1.75],[1,1],[0,0]])

px = 0.3
py = 0.1

point_index = 0   #旋转边下标
omega = 0         #旋转角度
min_width = 999999  #凸多边形宽度
point_set = []    #变换后点集
draw_point = []   #绘制点集
max_coord = []
min_coord = []

for i in range(0,len(border)-1):
    w = angle(border[i],border[i+1])
    a = border[i][0]
    b = border[i][1]
    temp = []
    for p in border:
        temp.append([(p[0]-a)*cos(w)+(p[1] - b)*sin(w), -(p[0]-a)*sin(w)+(p[1] - b)*cos(w)] )
    temp = np.array(temp)
    max_c = temp.max(0)
    min_c = temp.min(0)
    #width = abs(temp.max(0)[1] - temp.min(0)[1])
    width = abs(max_c[1] - min_c[1])
    if width < min_width:
        point_index = i
        omega = w
        min_width = width
        point_set = temp
        max_coord = max_c
        min_coord = min_c

draw_point.append(point_set[0])  # 起始点
now_point = point_set[0]
x_pos= y_pos = 1   # 方向
if point_set[point_index+1][0] < point_set[point_index][0]:
    x_pos *= -1
if min_coord[1] < 0:
    y_pos *= -1

#扫描线算法
while(True):
    now_point = now_point + [x_pos*px , 0]
    #是否换成四个角,即用栅格相交

    if cv2.pointPolygonTest(np.array(point_set*100,np.int0),tuple(np.array(now_point*100,np.int0)),False) >= 0:
        draw_point.append(now_point)

    if now_point[0] > max_coord[0] or now_point[0] < min_coord[0]:    # x方向上越界
        x_pos *= -1
        now_point = now_point + [ 0,y_pos*py]
        if cv2.pointPolygonTest(np.array(point_set * 100, np.int0), tuple(np.array(now_point * 100, np.int0)),
                                False) >= 0:
            draw_point.append(now_point)

    if abs(now_point[1]) > abs(min_coord[1]) and abs(now_point[0]) > max_coord[1]:
        break


def draw(points):
    points = points.reshape((-1,1,2))
    img = np.zeros((512,512,3),np.uint8)
    cv2.polylines(img,[points],True,(0,255,255),2)
    for i in draw_point:
        cv2.circle(img,center = (int(i[0]*100+200),int(i[1]*100 + 200)), radius= 2,color=(0,0,255),thickness=1)


    #cv2.imshow(winname,img)
    cv2.imwrite("test.jpg",img)


draw(np.array(point_set*100+(200,200),np.int32))

