# -*- coding: utf-8 -*-

import os
import re # 引入正则表达式模块
import datetime as dt
import pandas as pd
from ftplib import FTP  

class MyFtp:

    ftp = FTP()

    def __init__(self,host,port=21):
        self.ftp.connect(host,port)

    def login(self,username='anonymous',pwd='not_needed'):
        self.ftp.set_debuglevel(0)  # 打开调试级别0，不显示信息
        self.ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
        self.ftp.login(username,pwd) # 默认为匿名登陆
        print(self.ftp.welcome) #打印服务器的欢迎信息

    def set_localpath(self,filetime,local_dir):
        os.chdir(local_dir)
        var_dir = filetime # 用变量名命名子文件夹
        destination = local_dir + var_dir #本地路径
        print('     --------------------- local on : '+ destination +' ---------------------------')
        if not os.path.exists(destination):
            os.mkdir(destination) 
        os.chdir(destination)
        return destination

    def set_remotepath(self,filetime,remote_dir,remote_group):
        self.ftp.cwd(os.path.join(remote_dir,remote_group)) # 由于JRA55的文件并不全部存储在一个磁盘上，所以先进入目录所在的绝对路径
        self.ftp.cwd(filetime) # 在每个数据文件夹（如anl_p125）下是每个月数据的软连接，切进去会跳转到实际位置
        destination = self.ftp.pwd() # 获取yyyymm文件夹后会给出该文件夹实际所在的绝对路径
        print('     --------------------- remote on : '+ destination +' ---------------------------')
        self.ftp.cwd(destination) 
        return destination

    def set_filename(self,variable,remotepath,fuzzy=False):
        self.ftp.cwd(remotepath)   # 要登录的ftp目录
        filelist = self.ftp.nlst() # 获取所有文件列表
        retrive_filelist = [] 
        for filename in filelist:
            match = re.match(variable,filename) # 匹配文件开头
            if match:
                var_filename = match.string # 如果匹配，获取文件名
                retrive_filelist.append(var_filename) # 加入下载列表
                # print(' --- match : ' + var_filename +' ---') 
        return retrive_filelist

    def downloadFile(self,remotepath,filename):
        self.ftp.cwd(remotepath)   
        self.ftp.voidcmd('TYPE I') # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
        file_handle = open(filename,"wb").write   # 以写模式在本地打开文件
        self.ftp.retrbinary('RETR %s' % filename,file_handle, blocksize=8192)  # 下载文件

    def test_file_completeness(self,local_dir,remote_dir,filename):
        self.ftp.voidcmd('TYPE I') # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
        remote_size = self.ftp.size(os.path.join(remote_dir,filename)) # 获取远程文件大小

        local_path = os.path.join(local_dir,filename)
        local_size = os.path.getsize(local_path) if os.path.exists(local_path) else 0 # 获取本地文件大小，若不存在则设为0

        if local_size == remote_size:
            return 1 #已下载完成
        elif local_size < remote_size:
            return 0 #未下载/未完成
        else:
            return -1 #出问题了！

    def set_timerange(self,time_start,time_last): 
        #返回输入输出日期之间的所有yyyymm列表
        date_start = dt.datetime.strptime(time_start,'%Y%m%d')
        date_end = dt.datetime.strptime(time_last,'%Y%m%d')
        daterange = pd.date_range(start=date_start,end=date_end,freq='M')
        timelist = daterange.strftime('%Y%m')
        return list(timelist)



    def close(self):
        self.ftp.set_debuglevel(0)  # 关闭调试
        self.ftp.quit()

# class MyFtp def - end

def sort_key(string):
    # 提取文件末尾的时间信息（yyyymmddhh），其中文件末尾无日期的设为-1
    if string:
        try:
            suffix = re.findall(r'(\d+)$', string)[0]
        except:
            suffix = -1
        return int(suffix)

def sort_file(filelist):
    # 根据上个函数提取的日期对列表排序
    filelist.sort(key=sort_key)
    return filelist


if __name__ == '__main__':
    host = 'ds.data.jma.go.jp'
    username = 'jra06342'
    pwd = 'AEy9aGLH'

    remote_path = '/data19/JRA-55/Hist/Daily'
    remote_data_group = 'anl_p125'
    local_path = '/home/gult/data/JRA55_daily/anl_p125/'

    time_start = '19690501'
    time_last = '20161231'

    variable = 'anl_p125_hgt'

    ftp = MyFtp(host)
    ftp.login(username=username,pwd=pwd)

    timelist = ftp.set_timerange(time_start,time_last)
    for filetime in timelist:
        print('          * ---------------- time : {} ---------------- * '.format(filetime))
        remote_dir = ftp.set_remotepath(filetime,remote_path,remote_data_group)
        local_dir = ftp.set_localpath(filetime,local_path)
        file_list = ftp.set_filename(variable,remote_dir)
        file_list = sort_file(file_list)
        print('          * ---------------- nfile : {} ---------------- * '.format(len(file_list)))
        count = 0
        for files in file_list:
            count+=1
            completeness = ftp.test_file_completeness(local_dir,remote_dir,files)
            if completeness == 0:
                # 若未下载或未下载完，则下载该文件
                print('               * ----- working on : {i} of {n} ----- * '.format(i=count,n=len(file_list)))
                print('                       '+ files )
                ftp.downloadFile(remote_dir,files)
            elif completeness == 1:
                # 若已下载完，pass
                print('               * ----- ! finished ! : {i} of {n}, pass {file} ----- * '.format(i=count,n=len(file_list),file=files))
                continue
            else:
                # 若本地文件大小大于服务器上的，报错，给出文件信息并退出
                print(' *** ! error ! : {i} of {n}, filename : {file} , exiting *** '.format(i=count,n=len(file_list),file=files))
                os.exit(0)
    ftp.close()

   