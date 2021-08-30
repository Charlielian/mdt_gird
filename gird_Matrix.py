

import datetime,time
import os,sys,csv
import pandas as pd
#from tqdm import tqdm
import sql_model,other
import angle_class
import Matri_algorithm
import file_model

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


def None2zore(text):
    if 'None' in text :
        return 0
    else:
        return  text
def eci_gc(seci,gc_dict):
    result_dict = {'cellname':'111','lon':0,'lat':0,'dir':0,'earfcn':0,'pci':0,'tac':0}
    #scellname,slon,slat,sdir = None,0,0,0
    if str(seci) in gc_dict:
        result_dict['cellname'] = None2zore(gc_dict[str(seci)]['cellname']) #gc_dict[str(seci)]['cellname']
        result_dict['lon'] =     float(None2zore(gc_dict[str(seci)]['lon']))              #float(gc_dict[str(seci)]['lon'])
        result_dict['lat'] =  float(None2zore(gc_dict[str(seci)]['lat']))      #float(gc_dict[str(seci)]['lat'])
        result_dict['dir'] = int(None2zore(gc_dict[str(seci)]['dir']))
        result_dict['earfcn'] = int(None2zore(gc_dict[str(seci)]['earfcn'])) # int(gc_dict[str(seci)]['earfcn'])
        result_dict['pci'] = int(None2zore(gc_dict[str(seci)]['pci'])) #int(gc_dict[str(seci)]['pci'])
        result_dict['tac'] = int(None2zore(gc_dict[str(seci)]['tac'])) #int(gc_dict[str(seci)]['tac'])
    return  result_dict









def gird_main(path):
    gird_dict = {}  # {gird:{rsrp: , samples: , cells:{cel1:{rsrp:,samples:},cel2:{rsrp:,samples:} }  }
    cell_dict = {}  # {cel1:{gird1:{rsrp:,samples:},gird2:{rsrp:,samples:}},cel2:{gird3:{rsrp:,samples:},gird4:{rsrp:,samples:}},}
    matrix_cell = {} #相关性字典 {cell1:{cell2:XX,cell3:XX}}
    cell_gird = {} #小区栅格字典
    gird_cell = {}  # 栅格字典
    pci_dict = {}
    gc_dict = sql_model.get_gc()
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


    #处理cell_gird内的rsrp
    # gird_cell = {gird_id:{eci1:rsrp,eci2:rsrp}}
    # cell_dict = {eci1:{girdid:{rsrp:-100,rsrq:-8,samples:11}}}
    # for  cur_girdid in  gird_cell:
    #     for cur_eci in gird_cell[cur_girdid]:
    #         gird_cell[cur_girdid][cur_eci]= cell_dict[cur_eci][cur_girdid]['rsrp']
    #关联计算汇总至 matrix_cell表
    for cur_eci in cell_gird :
        #增加过滤条件 rsrp相差在-10dB以内为有效小区
        gird_list = list(set([x for x in cell_gird[cur_eci]] ))#list(set(ids))
        gird_sum = len(gird_list)#总栅格数
        eci_list = Matri_algorithm.girdincell(gird_list,gird_cell)
        for  d_eci in eci_list :
            if d_eci != cur_eci :
                d_gird_list = list(set([x for x in cell_gird[d_eci]] ))
                repeat_list = [x for x in gird_list if x in d_gird_list]
                total_gird = 0
                for  gird in repeat_list :
                    if   abs(float(cell_dict[cur_eci][gird]['rsrp']) - float(cell_dict[d_eci][gird]['rsrp'])) <=10 :
                        total_gird +=1
                    else:
                        pass
                #repeat_num = total_gird # len(repeat_list)
                cresult_dict = eci_gc(cur_eci, gc_dict)
                s_earfcn ,s_pci = cresult_dict['earfcn'],cresult_dict['pci']
                sresult_dict = eci_gc(d_eci, gc_dict)
                d_earfcn, d_pci = sresult_dict['earfcn'], sresult_dict['pci']
                if s_earfcn == d_earfcn and s_pci == d_pci:
                    pci_tt = str(s_earfcn) + '_' + str(s_pci) + "-" + str(d_earfcn) + '_' + str(d_pci)
                    if  cur_eci in pci_dict :
                        if d_eci in pci_dict[cur_eci]:
                            pass
                        else:
                            pci_dict[cur_eci][d_eci] = {'pci_matrix': pci_tt,
                                                        'matrix': round(100 * total_gird / gird_sum, 2)}

                    else:
                        pci_dict[cur_eci] = {}
                        pci_dict[cur_eci][d_eci] = {'pci_matrix':pci_tt,'matrix':round(100*total_gird/gird_sum,2)}
                else:
                    pci_tt = str(s_earfcn) + '_' + str(s_pci) + "-" + str(d_earfcn) + '_' + str(d_pci)
                if cur_eci in matrix_cell :
                    if  d_eci in  matrix_cell[cur_eci] :
                        pass
                    else:
                        matrix_cell[cur_eci][d_eci] = {}
                        matrix_cell[cur_eci][d_eci]['pci_matrix'] = pci_tt
                        matrix_cell[cur_eci][d_eci]['matrix'] = round(100*total_gird/gird_sum,2)
                else:
                    matrix_cell[cur_eci] = {}
                    matrix_cell[cur_eci][d_eci] = {}
                    matrix_cell[cur_eci][d_eci]['pci_matrix'] = pci_tt
                    matrix_cell[cur_eci][d_eci]['matrix']  =round(100*total_gird/gird_sum,2)


    #pci优化思路
    # for  cur_eci in pci_dict :
    #     for  d_eci in pci_dict[cur_eci]:
    #         s_matrix = pci_dict[cur_eci][d_eci]['matrix']
    #         d_matrix = pci_dict[d_eci][cur_eci]['matrix']
    #         if  s_matrix >  d_matrix  and  s_matrix >50 :
    #             result_dict  =eci_gc(cur_eci,gc_dict)
    #             earfcn = result_dict['earfcn']
    return  gird_dict,cell_dict,matrix_cell
def pcianalysis(matrix_cell):
    pass
def gird_cells(cell_dict):
    #栅格6强小区计算
    gird_cels = {}
    gc_dict = sql_model.get_gc()
    for cur_eci in cell_dict:
        result_dict = eci_gc(cur_eci,gc_dict)
        celname =  result_dict['cellname']
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
    #完成最多采样点6个小区进行插入字典数据
    for cur_girdid in gird_cels :
        for cel_num in gird_cels[cur_girdid]:
            gird_dict[cur_girdid][cel_num] = str(gird_cels[cur_girdid][cel_num]['cellname']) +"("+str(gird_cels[cur_girdid][cel_num]['eci']) +")"+":"+str(gird_cels[cur_girdid][cel_num]['samples'])
    #小区关联
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    result_path = exe_path +"//"+"result"+"//"+dtime
    other.mkdir(result_path) #判断结果目录是否存在，不存在则新建
    file_model.create_matrixcsv(matrix_cell,result_path)
    file_model.create_girdcsv(gird_dict,result_path)
    file_model.create_cellcsv(cell_dict,result_path)



path = 'd:/temp/20210827/20210826-mdt'
main(path)



