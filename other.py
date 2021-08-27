import datetime,os,sys

def get_date():
    t = datetime.datetime.now()
    dt = t.strftime('%Y-%m-%d')
    dtime = t.strftime('%Y%m%d%H%M%S')
    return dt,dtime

def view_bar(file,num, total):  #显示进度条
    rate = num/total
    rate_num = round(rate * 100,6)
    number=int(50*rate)
    r = '\r[%s%s]%s%%....%s/%s   目前正在读取文件%s' % ("#"*number, " "*(50-number), rate_num, num,total,file)
    print("\r {}".format(r),end=" ")   #\r回到行的开头
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在

        return False
