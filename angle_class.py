from math import radians, cos, sin, asin, sqrt,atan2,atan,pi
from operator import  mod
def tt_angle(s_lon,s_lat,d_lon,d_lat):
    #正北角度计算
    r2 = 0.017453293
    lon1, lat1, lon2, lat2 = map(radians, [s_lon, s_lat, d_lon, d_lat])
    angle = 0
    y_se = lat2 - lat1;
    x_se = lon2 - lon1;
    if x_se == 0 and y_se > 0:
        angle = 360
    if x_se == 0 and y_se < 0:
        angle = 180
    if y_se == 0 and x_se > 0:
        angle = 90
    if y_se == 0 and x_se < 0:
        angle = 270
    if x_se > 0 and y_se > 0:
        angle = atan(x_se / y_se) * 180 / pi
    elif x_se < 0 and y_se > 0:
        angle = 360 + atan(x_se / y_se) * 180 / pi
    elif x_se < 0 and y_se < 0:
        angle = 180 + atan(x_se / y_se) * 180 / pi
    elif x_se > 0 and y_se < 0:
        angle = 180 + atan(x_se / y_se) * 180 / pi
    return x_se,y_se,angle

def dist_juli(s_lon,s_lat,d_lon,d_lat):
    #距离计算
    r2 = 0.017453293
    lon1, lat1, lon2, lat2 = map(radians, [s_lon, s_lat, d_lon, d_lat])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    dist = round(c * r * 1000, 2)
    return dist

def tta(s_lon,s_lat,dir_s,d_lon,d_lat,dir_d):
    # 将十进制度数转化为弧度
    dist = dist_juli(s_lon,s_lat,d_lon,d_lat)
    #夹角计算
    if dist ==0:
        ttNA =0
        ttCA =0
    else:
        lgR,ltR,tt =tt_angle(s_lon,s_lat,d_lon,d_lat)
        #邻区方向角于本站点夹角
        ttNA =round(180 -abs(mod(abs(180+tt-dir_d),360 )-180),2)
        #本站方向角于目标站点夹角
        ttCA =round(180- abs(mod(abs(tt-dir_s),360 )-180),2)

    return dist,ttCA,ttNA

def radius(lon,lat,dir,r):
    r2 = 0.017453293
    lon_d = lon + r / 1000 * sin(dir * r2) / (111 * cos(lat * r2))

    lat_d = lat + (r / 1000 * cos(dir * r2)) / (111)

    return lon_d,lat_d
def cross(p1,p2,p3):#跨立实验
    x1=dist_juli(p2[0],p2[1],p1[0],p2[1])
    y1=dist_juli(p2[0],p2[1],p2[0],p1[1])
    x2=dist_juli(p3[0],p3[1],p1[0],p3[1])
    y2=dist_juli(p3[0],p3[1],p3[0],p1[1])

    return x1*y2-x2*y1

def IsIntersec(p1,p2,p3,p4): #判断两线段是否相交
    #p1,p2为 line1的开始及结束点； p2 = [111.8816,21.72756] p1 = [111.87839,21.73469]
    # p3,p4为 line2的开始及结束点；p3 = [111.8816,21.72756] p4= [111.87839,21.73469]
    #快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
    if(max(p1[0],p2[0])>=min(p3[0],p4[0])    #矩形1最右端大于矩形2最左端
    and max(p3[0],p4[0])>=min(p1[0],p2[0])   #矩形2最右端大于矩形1最左端
    and max(p1[1],p2[1])>=min(p3[1],p4[1])   #矩形1最高端大于矩形2最低端
    and max(p3[1],p4[1])>=min(p1[1],p2[1])): #矩形2最高端大于矩形1最低端
    #若通过快速排斥则进行跨立实验
        if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0 and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
            D=1
        else:
            D=0
    else:
        D=0
    return D




