import os
import csv
import pandas as pd
import shutil
import time
import tarfile
import zipfile
import traceback
import gird_algorithm
import other


def un_tar(localpath, temppath, file_name):
  #untar zip file"""
    tar = tarfile.open(localpath + "//" + file_name)
    names = tar.getnames()
    if os.path.isdir(temppath +"//"+file_name.replace('.tar.gz',"") ):
        pass
    else:
        os.mkdir(temppath +"//"+file_name.replace('.tar.gz' ,   "") )
    #因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar.extract(name, temppath +"//"+file_name.replace('.tar.gz',"") )
    tar.close()
    return temppath +"//"+file_name.replace('.tar.gz',"")


def un_zip(localpath,temppath,file_name):
    #print(file_name,type(file_name))
    new_file = file_name[:-4]
    zip_file = zipfile.ZipFile(localpath+"//"+file_name)
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件
    for f in zip_list:
        zip_file.extract(f, temppath+"//"+new_file)  # 循环解压文件到指定目录
    zip_file.close()  # 关闭文件，必须有，释放内存
    return temppath+"//"+new_file

def readgzip(path,gzfile,gird_data,type_str):
    # type =zip ,gzip
    df = pd.read_csv(path + "//" + gzfile, compression=type_str, header=0, sep=',', quotechar='"',
                     error_bad_lines=False, encoding='gbk')
    for num in range(1, len(df['服务小区ID'])):
        cur_lon = float(df['UE经度'][num])
        cur_lat = float(df['UE纬度'][num])
        girdid = gird_algorithm.gird_num(cur_lat, cur_lon)
        rsrp = int(df['服务小区RSRP'][num]) - 140
        rsrq = int(df['服务小区RSRQ'][num])*0.5-20
        gird_data.append([girdid,df['服务小区ID'][num], cur_lon, cur_lat, rsrp,rsrq])
    return gird_data
def create_point_dict(gird_data,path,newfilename):
    if len(gird_data) > 0 :
        dt, dtime = other.get_date()
        #生成点图
        out = open(path +"//"+ '%s_%s.csv' % (newfilename,dtime), "w", newline="")
        csv_writer = csv.writer(out, dialect="excel")
        # Number of samples
        csv_writer.writerow(['gird_id','ECI', 'lon', 'lat', 'rsrp','rsrq'])
        #for girdid in gird_data:
        csv_writer.writerows(gird_data)

def nokia_parser(out_path,temp_path,file,path,p,total):
    start = time.time()
    gird_data = []
    filepath = un_tar(out_path, temp_path, file)
    newfilename = file.replace(".tar.gz","")
    gzfiles = os.listdir(filepath)
    for gzfile in gzfiles:
        # tempdata = readgzip(filepath, gzfile)
        try:
            readgzip(filepath, gzfile, gird_data, 'gzip')
        except Exception as e:
            print(e)
    shutil.rmtree(filepath)
    end = time.time()
    #print('Task  runs %0.2f seconds.' % ((end - start)))
    print("解析完成%s..........费时%0.2f秒  [%s/%s]"%(file,(end - start),p,total))
    create_point_dict(gird_data, path,newfilename)
def zte_parser(out_path,temp_path,file,path,p,total):
    start = time.time()
    gird_data = []
    filepath = un_zip(out_path, temp_path, file)
    newfilename = file.replace(".zip","")
    zipfiles = os.listdir(filepath)
    for zip_file in zipfiles:
        try:
            extracting = zipfile.ZipFile(filepath + "//" + zip_file)
            extracting.extractall(filepath)
            extracting.close()
            csvfile = zip_file.replace(".zip", ".csv")
            with open(filepath + "//" + csvfile, 'r', encoding='gbk') as f:
                reader = csv.reader(f)
                n = 0
                for i in reader:
                    n += 1
                    if n > 2:
                        ser_len = len(i[6])
                        serverid = int(i[6][5:ser_len])  # int(i[6][5:11])*256+int(i[6][11:13])
                        cur_lon = i[14]
                        cur_lat = i[16]
                        rsrp = int(i[9])- 140
                        if i[10] is None :
                            rsrq = None
                        else:
                            rsrq = int(i[10])*0.5 -20
                        # print(serverid,cur_lon,cur_lat,rsrp)
                        if cur_lon is not None and len(cur_lon) > 0:
                            girdid = gird_algorithm.gird_num(float(cur_lat), float(cur_lon))
                            gird_data.append([girdid, serverid, cur_lon, cur_lat, rsrp,rsrq])
            os.remove(filepath + "//" + csvfile)
            os.remove(filepath + "//" + zip_file)
        except Exception  as e:
            pass
    shutil.rmtree(filepath)
    end = time.time()
    print("解析完成%s..........费时%0.2f秒  [%s/%s]"%(file,(end - start),p,total))
    create_point_dict(gird_data, path,newfilename)

def main(p,total,file,out_path,temp_path,path):
    try:
        #print(file, round(p / total * 100, 2))
        if 'tar.gz' in file:
            nokia_parser(out_path, temp_path, file, path,p,total)
        if '.zip' in file:
            zte_parser(out_path, temp_path, file, path,p,total)
    except Exception as e:

        traceback.print_exc(e)
