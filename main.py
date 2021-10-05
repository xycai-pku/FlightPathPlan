import folium
import cv2
import numpy as np
from math import atan2, sin, cos


def angle(point_1, point_2):
    if point_1[1] == point_2[1] == 0:
        return 0
    return atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])


def ifjoin(point, cnt):
    '''
    待补充函数
    :param point: 点
    :param cnt: 多边形点
    :return: 以该点为中心的矩阵是否与该多边形有重叠区域
    '''
    pass


def pointTrans(point, M):
    homo_point = np.array([point[0],point[1],1])
    temp_p = M.dot(homo_point)
    return np.array([temp_p[0],temp_p[1]])

#border = np.array([[0, 0], [-0.5, 0.1], [-1, 1.1], [0, 2], [0.5, 1.75], [1, 1], [0, 0]])

def draw(border):

    border = np.array(border)
    print(border)
    px = 300
    py = 200

    point_index = 0  # 旋转边下标
    omega = 0  # 旋转角度
    min_width = 9999999  # 凸多边形宽度
    point_set = []  # 变换后点集
    draw_point = []  # 绘制点集
    max_coord = []
    min_coord = []
    rotation_matrix = []  # 旋转矩阵
    trans_matrix = []  # 平移矩阵
    a_ = b_ = 0

    # 寻找最小宽度
    for i in range(0, len(border) - 1):
        w = angle(border[i], border[i + 1])
        a = border[i][0]
        b = border[i][1]
        temp = []
        for p in border:
            temp.append([(p[0] - a) * cos(w) + (p[1] - b) * sin(w), -(p[0] - a) * sin(w) + (p[1] - b) * cos(w)])
        temp = np.array(temp)
        max_c = temp.max(0)
        min_c = temp.min(0)
        # width = abs(temp.max(0)[1] - temp.min(0)[1])
        width = abs(max_c[1] - min_c[1])
        if width < min_width:
            point_index = i
            omega = w
            min_width = width
            point_set = temp
            max_coord = max_c
            min_coord = min_c
            a_ = a
            b_ = b

    rotation_matrix = np.array([[cos(omega), sin(omega), 0],
                                [-sin(omega), cos(omega), 0],
                                [0, 0, 1],
                                ])
    trans_matrix = np.array([[1, 0, -a_],
                             [0, 1, -b_],
                             [0, 0, 1]])

    #draw_point.append(point_set[point_index])  # 起始点
    now_point = point_set[point_index]
    x_pos = y_pos = 1  # 方向
    if point_set[point_index + 1][0] < point_set[point_index][0]:
        x_pos *= -1
    if min_coord[1] < 0:
        y_pos *= -1

    # 扫描线算法
    while (True):
        now_point = now_point + [x_pos * px, 0]
        # 是否换成四个角,即用栅格相交

        if cv2.pointPolygonTest(np.array(point_set, np.int32), (int(now_point[0]),int(now_point[1])),
                                False) >= 0:
            draw_point.append(now_point)

        if now_point[0] > max_coord[0] or now_point[0] < min_coord[0]:  # x方向上越界
            x_pos *= -1
            now_point = now_point + [0, y_pos * py]
            if cv2.pointPolygonTest(np.array(point_set, np.int32), (int(now_point[0]),int(now_point[1])),
                                    False) >= 0:
                draw_point.append(now_point)

        if abs(now_point[1]) > abs(min_coord[1]) and abs(now_point[0]) > max_coord[1]:
            break

    for i in range(0, len(point_set)):
        point_set[i] = pointTrans(point_set[i], np.linalg.inv(trans_matrix).dot(np.linalg.inv(rotation_matrix)))
    for i in range(0, len(draw_point)):
        draw_point[i] = pointTrans(draw_point[i], np.linalg.inv(trans_matrix).dot(np.linalg.inv(rotation_matrix)))

    draw_point.insert(0,np.array([a_,b_]))

    return draw_point

# def draw(points):
#     points = points.reshape((-1, 1, 2))
#     img = np.zeros((512, 512, 3), np.uint8)
#     cv2.polylines(img, [points], True, (0, 255, 255), 2)
#     for i in draw_point:
#         cv2.circle(img, center=(int(i[0] * 100 + 200), int(i[1] * 100 + 200)), radius=2, color=(0, 0, 255), thickness=1)
#     cv2.imwrite("test.jpg", img)
#
#
# draw(np.array(point_set * 100 + (200, 200), np.int32))
