

import datetime,time
import os,sys,csv
import pandas as pd
#from tqdm import tqdm
import sql_model,other
import angle_class
import Matri_algorithm


def cel_dd(gird_dict,girdid):
    if 'None' in gird_dict[girdid]['cel2']:
        cel2 = None
    else:
        cel2 = gird_dict[girdid]['cel2']
    if 'None' in gird_dict[girdid]['cel3']:
        cel3 = None
    else:
        cel3 = gird_dict[girdid]['cel3']
    if 'None' in gird_dict[girdid]['cel4']:
        cel4 = None
    else:
        cel4 = gird_dict[girdid]['cel4']

    if 'None' in gird_dict[girdid]['cel5']:
        cel5 = None
    else:
        cel5 = gird_dict[girdid]['cel5']
    if 'None' in gird_dict[girdid]['cel6']:
        cel6 = None
    else:
        cel6 = gird_dict[girdid]['cel6']
    return cel2,cel3,cel4,cel5,cel6
def create_girdcsv(gird_dict,outpath):
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # 写入栅格csv
    dt, dtime = other.get_date()
    # 生成点图
    out = open(outpath+"//"+'gird_%s.csv' % (dtime), "w", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    # Number of samples
    csv_writer.writerow(['gird_id', 'samples', 'rsrp', 'rsrq', 'lon', 'lat','cel1','cel2','cel3','cel4','cel5','cel6'])
    # for girdid in gird_data:
    # csv_writer.writerows(gird_data)
    for girdid in gird_dict:
        cel2,cel3,cel4,cel5,cel6 =cel_dd(gird_dict,girdid)
        csv_writer.writerow([girdid
                            , gird_dict[girdid]['samples']
                            , round(gird_dict[girdid]['rsrp'],2)
                            , round(gird_dict[girdid]['rsrq'],2)
                            , gird_dict[girdid]['lon']
                            , gird_dict[girdid]['lat']
                            ,gird_dict[girdid]['cel1']
                            ,cel2
                            ,cel3
                            ,cel4
                            ,cel5
                            ,cel6 ])


def eci_gc(seci,gc_dict):
    scellname,slon,slat,sdir = None,0,0,0
    if str(seci) in gc_dict:
        scellname = gc_dict[str(seci)]['cellname']
        slon = float(gc_dict[str(seci)]['lon'])
        slat = float(gc_dict[str(seci)]['lat'])
        sdir = int(gc_dict[str(seci)]['dir'])
    return  scellname,slon,slat,sdir

def create_matrixcsv(matrix_cell,outpath):
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # 写入栅格csv
    dt, dtime = other.get_date()
    gc_dict = sql_model.get_gc()
    # 生成点图
    out = open(outpath + "//" + 'matrix_cell_%s.csv' % (dtime), "w", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(['SECI','scellname', 'DECI','dcellname', 'Correlation_degree','dist','ttCA','ttNA'])
    for seci in matrix_cell :
        scellname,slon,slat,sdir = eci_gc(seci,gc_dict)
        for deci in matrix_cell[seci]:
            try:
                dcellname, dlon, dlat, ddir = eci_gc(deci, gc_dict)

                dist,ttCA,ttNA = angle_class.tta(slon,slat,sdir,dlon,dlat,ddir)

                csv_writer.writerow([seci,scellname,deci,dcellname,matrix_cell[seci][deci],dist,ttCA,ttNA])
            except Exception as e:
                print(e)



def create_cellcsv(cell_dict,outpath):
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # 写入栅格csv
    dt, dtime = other.get_date()
    gc_dict = sql_model.get_gc()
    # 生成点阵CSV
    out = open(outpath +"//"+'cell_gird_%s.csv' % (dtime), "w", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(['ECI','enbid','lcrid','cellname', 'gird_id', 'samples', 'rsrp', 'rsrq', 'lon', 'lat'])
    # for girdid in gird_data:
    # csv_writer.writerows(gird_data)
    for cur_eci in cell_dict:
        cellname = None
        enbid = int(cur_eci / 256)
        lcrid = divmod(cur_eci, 256)[1]
        cgi = '460-00-' + str(enbid) + '-' + str(lcrid)
        if str(cur_eci) in gc_dict :
            cellname = gc_dict[str(cur_eci)]['cellname']
        else:
            pass
        for cur_girdid in cell_dict[cur_eci]:
            csv_writer.writerow([cur_eci,enbid,lcrid,cellname
                                    , cur_girdid, cell_dict[cur_eci][cur_girdid]['samples']
                                    , round(cell_dict[cur_eci][cur_girdid]['rsrp'],2)
                                    , round(cell_dict[cur_eci][cur_girdid]['rsrq'],2)
                                    , cell_dict[cur_eci][cur_girdid]['lon']
                                    , cell_dict[cur_eci][cur_girdid]['lat']])





def gird_main(path):
    gird_dict = {}
    # {gird:{rsrp: , samples: , cells:{cel1:{rsrp:,samples:},cel2:{rsrp:,samples:} }  }
    cell_dict = {}
    # {cel1:{gird1:{rsrp:,samples:},gird2:{rsrp:,samples:}},cel2:{gird3:{rsrp:,samples:},gird4:{rsrp:,samples:}},}
    matrix_cell = {}
    cell_gird = {}
    gird_cell = {}
    # {cell1:{cell2:XX,cell3:XX}}
    files = os.listdir(path)
    p = 0
    for file in files:
        p += 1
        other.view_bar(file,p, len(files))
        df = pd.read_csv(path + "//" + file, header=0, sep=',', error_bad_lines=False, encoding='gbk')
        girdid = df['gird_id']
        eci = df['ECI']
        rsrp = df['rsrp']
        rsrq = df['rsrq']
        total_Num = len(girdid)
        for num in range(0, total_Num):
            try:
                cur_girdid = girdid[num]
                cur_eci = eci[num]
                cur_rsrp = int(rsrp[num])
                cur_rsrq = int(rsrq[num])
                # 关联性计算
                gird_dict =Matri_algorithm.gird_dict_create(cur_girdid,gird_dict,cur_rsrp,cur_rsrq)
                cell_dict = Matri_algorithm.cell_dict_create(cur_girdid,cur_eci,cell_dict,cur_rsrp,cur_rsrq)
                cell_gird,gird_cell =Matri_algorithm.cell_gird_create(cur_eci,cur_girdid,cell_gird,gird_cell)
            except Exception as e:
                print(e)
    #关联计算汇总至 matrix_cell表
    for cur_eci in cell_gird :
        gird_list = list(set([x for x in cell_gird[cur_eci]] ))#list(set(ids))
        gird_sum = len(gird_list)#总栅格数
        eci_list = Matri_algorithm.girdincell(gird_list,gird_cell)
        for  d_eci in eci_list :
            if d_eci != cur_eci :
                d_gird_list = list(set([x for x in cell_gird[d_eci]] ))
                repeat_list = [x for x in gird_list if x in d_gird_list]
                repeat_num = len(repeat_list)
                if cur_eci in matrix_cell :
                    matrix_cell[cur_eci][d_eci] = round(100*repeat_num/gird_sum,2)
                else:
                    matrix_cell[cur_eci] = {d_eci:round(100*repeat_num/gird_sum,2)}
    return  gird_dict,cell_dict,matrix_cell

def gird_cells(cell_dict):
    #栅格6强小区计算
    gird_cels = {}
    gc_dict = sql_model.get_gc()
    for cur_eci in cell_dict:
        if str(cur_eci) in gc_dict:
            celname = gc_dict[str(cur_eci)]['cellname']
        else:
            celname = '111'
        for cur_girdid in cell_dict[cur_eci]:
            cur_samples = cell_dict[cur_eci][cur_girdid]['samples']
            if cur_girdid in gird_cels:
                eci_list = []
                celname_list = []
                celsamples_list = []
                for num in range(1, 7):
                    eci_list.append(gird_cels[cur_girdid]['cel' + str(num)]['eci'])
                    celname_list.append(gird_cels[cur_girdid]['cel' + str(num)]['cellname'])
                    celsamples_list.append(gird_cels[cur_girdid]['cel' + str(num)]['samples'])
                for num in range(0, 6):
                    if cur_samples > gird_cels[cur_girdid]['cel' + str(num + 1)]['samples']:
                        # 插入列表
                        eci_list.insert(num, cur_eci)
                        celname_list.insert(num, celname)
                        celsamples_list.insert(num, cur_samples)

                        break
                for num in range(1, 7):
                    gird_cels[cur_girdid]['cel' + str(num)]['eci'] = eci_list[num - 1]
                    gird_cels[cur_girdid]['cel' + str(num)]['cellname'] = celname_list[num - 1]
                    gird_cels[cur_girdid]['cel' + str(num)]['samples'] = celsamples_list[num - 1]
            else:
                gird_cels[cur_girdid] = {}
                gird_cels[cur_girdid]['cel1'] = {}
                gird_cels[cur_girdid]['cel1']['eci'] = str(cur_eci)
                gird_cels[cur_girdid]['cel1']['cellname'] = celname
                gird_cels[cur_girdid]['cel1']['samples'] = cur_samples
                for num in range(2, 7):
                    gird_cels[cur_girdid]['cel' + str(num)] = {}
                    gird_cels[cur_girdid]['cel' + str(num)]['eci'] = None
                    gird_cels[cur_girdid]['cel' + str(num)]['cellname'] = None
                    gird_cels[cur_girdid]['cel' + str(num)]['samples'] = 0
    return gird_cels
def main(path):
    dt, dtime = other.get_date()
    gird_dict, cell_dict, matrix_cell = gird_main(path )
    #完成gird栅格后，进行小区栅格相关性计算
    #cell_dict[cur_eci][cur_girdid] = {'rsrp': cur_rsrp, 'rsrq': cur_rsrq, 'samples': 1, 'lon': r_lon,'lat': r_lat}
    gird_cels = gird_cells(cell_dict)
                #if cur_samples > gird_cels[cur_girdid]['cel1']:
    #完成最多采样点6个小区进行插入字典数据
    for cur_girdid in gird_cels :
        for cel_num in gird_cels[cur_girdid]:
            gird_dict[cur_girdid][cel_num] = str(gird_cels[cur_girdid][cel_num]['cellname']) +"("+str(gird_cels[cur_girdid][cel_num]['eci']) +")"+":"+str(gird_cels[cur_girdid][cel_num]['samples'])


    #小区关联
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    # cell_dict[cur_eci][cur_girdid]['rsrp'] = cur_rsrp
    # cell_dict[cur_eci][cur_girdid]['samples'] = 1
    other.mkdir(exe_path +"//"+"result"+"//"+dtime)
    outpath = exe_path +"//"+"result"+"//"+dtime
    create_matrixcsv(matrix_cell,outpath)
    create_girdcsv(gird_dict,outpath)
    create_cellcsv(cell_dict,outpath)









