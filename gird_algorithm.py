import math
def gird_num(rlat,rlon):
    #经纬度算栅格号算法，栅格大小为50米X50米
    #赤道附近以50米距离的弧度计算，100米转换为弧度的为经度 0.0009865，纬度0.0009017 ,一圈大约为15579个栅格，以此类推。
    girdid = math.floor((rlat - 20.05085) / (0.0009017 / 2)) * 15579 + math.floor((rlon - 109.42843) / (0.0009865 / 2)) + 1
    return girdid
def gird_parser(girdid):
    # 经度ROUNDDOWN(栅格号/15579,0)+0.5
    delta_lat = int(girdid/15579)+0.5
    r_lat = 20.05085+delta_lat*0.0009017/2
    # 纬度 MOD(栅格号,15579)+0.5
    delta_lat = divmod(girdid,15579)[1]+0.5
    r_lon = 109.42843+(delta_lat-1)*0.0009865/2

    return round(r_lon,7),round(r_lat,8)
