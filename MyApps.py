
import os,sys,time
import parser_MM #解析模块
import gird_Matrix #栅格处理模块
import gird_algorithm #栅格算法
import sql_model #数据库处理模块
import angle_class #方位距离处理模块
import other #其他模块
import multiprocessing #多线程
import configparser
exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
config = configparser.ConfigParser()
config.read(exe_path + "//" + "conf.ini", encoding="utf-8-sig")
if __name__ == "__main__":
    multiprocessing.freeze_support() #添加此条防止windows出现进程冲突
    out_path = config.get("main", "mdtpath")   #M1M2存放目录
    temp_path = config.get("main", "tmeppath") #临时目录
    path = config.get("main", "pointpath") # 输出点目录
    p_num = multiprocessing.Pool(int(config.get("main","Thread")))  # 进程数 视电脑配置定
    dt, dtime = other.get_date() #获取当前系统时间
    start = time.time()
    print("程序开始..................................")
    point_path = path + "//" + dtime #以时间戳为名字新建点文件夹
    gird_Matrix.mkdir(point_path)  #新建点文件夹
    files = os.listdir(out_path) #获取MDT文件清单
    total = len(files)
    p = 0
    for file in files :
        p +=1
        #print(file,round(p/total*100,2))
        #main(p,total,file,out_path,temp_path,path)
        p_num.apply_async(parser_MM.main, args=(p,total,file,out_path,temp_path,point_path ,))
            #print(list(tempdata))
    p_num.close()
    p_num.join()
    print("开始解析点阵数据........................")
    gird_Matrix.main(point_path)
    end = time.time()
    print("\n"+"程序运行结束..........费时%0.2f秒    " % ((end - start)))



