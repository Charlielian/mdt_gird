
import pymysql
import configparser
import os,sys
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
config = configparser.ConfigParser()
config.read(exe_path + "//" + "conf.ini", encoding="utf-8-sig")


def mysql_get(sql_str,mysqldb):
    #db = {'ip': mysql_ip, 'db': mysql_db, 'acc': acc, 'pw': pw, 'port': int(port)}
    try:
        db = pymysql.Connect(
            host= mysqldb['ip'],
            port= mysqldb['port'],
            user= mysqldb['acc'],
            passwd= mysqldb['pw'],
            db= mysqldb['db'],
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8'          )
        #print("连接成功！！")
        cursor = db.cursor()
        cursor.execute(sql_str)
        #print(sql_str)
        record =cursor.fetchall()
         # print("导入数据成功!!")
        db.close()
        return record
    except Exception as e:
        print(e)

def get_gc():
    # 读取工参物理表
    #数据库账号密码统一在这里设置 读取config
    host = config.get("mysql_config", "ip")
    acc = config.get("mysql_config", "acc")
    pw = config.get("mysql_config", "pw")
    db = config.get("mysql_config", "db")
    port = config.get("mysql_config", "port")
    database = {'ip': host, 'db': db, 'acc': acc, 'pw': pw, 'port': int(port)}
    sql_str= "SELECT DISTINCT gc_table.ECI, gc_table.CGI, gc_table.lnBtsId,gc_table.lcrid,gc_table.CellName_Cn,gc_table.Longitude, gc_table.Latitude,     gc_table.Azimuth FROM gc_table  where networkstauts = 'T'  AND gc_table.Longitude> 0  ;"
    #print(sql_str)    gc_table.Longitude,    gc_table.Latitude,     gc_table.Azimuth
    resu_dict = mysql_get(sql_str,database)
    # print(resu_dict)
    gc_dict = {}
    for item in resu_dict:
        #print(item)
        cgi,enbid,lcrid,cellname,ECI = item['CGI'],item['lnBtsId'],item['lcrid'], item['CellName_Cn'], item['ECI']
        lon,lat,dir = item['Longitude'],item['Latitude'],item['Azimuth']
        if  ECI in gc_dict:
            gc_dict[ECI]['cellname'] = cellname
            gc_dict[ECI]['CGI'] = cgi
            gc_dict[ECI]['enbid'] = enbid
            gc_dict[ECI]['lcrid'] = lcrid
            gc_dict[ECI]['lon'] = lon
            gc_dict[ECI]['lat'] = lat
            gc_dict[ECI]['dir'] = dir
        else :
            gc_dict[ECI] ={}
            gc_dict[ECI]['cellname'] = cellname
            gc_dict[ECI]['CGI'] = cgi
            gc_dict[ECI]['enbid'] = enbid
            gc_dict[ECI]['lcrid'] = lcrid
            gc_dict[ECI]['lon'] = lon
            gc_dict[ECI]['lat'] = lat
            gc_dict[ECI]['dir'] = dir

    return gc_dict
