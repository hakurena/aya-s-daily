# -*- coding: utf-8 -*-

import os
import re # 引入正则表达式模块
from ftplib import FTP  

class MyFtp:

    ftp = FTP()

    def __init__(self,host,port=21):
        self.ftp.connect(host,port)

    def login(self,username='anonymous',pwd='not_needed'):
        self.ftp.set_debuglevel(1)  # 打开调试级别1，显示简略信息
        self.ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
        self.ftp.login(username,pwd) # 默认为匿名登陆
        print(self.ftp.welcome) #打印服务器的欢迎信息

    def set_localpath(self,variable,local_dir):
        os.chdir(local_dir)
        var_dir = variable # 用变量名命名子文件夹
        destination = local_dir + var_dir #本地路径
        print('     --------------------- now working on : '+ destination +' ---------------------------')
        if not os.path.exists(destination):
            os.mkdir(destination) 
        os.chdir(destination)

    def set_filename(self,variable,remotepath,time_range,fuzzy=False):
        self.ftp.cwd(remotepath)   # 要登录的ftp目录
        filelist = self.ftp.nlst() # 获取所有文件列表
        if fuzzy == True: # 启用模糊搜索，适用于目录下有复数个同变量数据的情况。
            pass # 没想好怎么写.....
        elif fuzzy == False:
            retrive_filelist = [] # 需要下载的文件列表
            for filename in filelist:
                match = re.match(variable,filename) # 匹配文件开头
                if match:
                    var_filename = match.string #如果匹配，获取文件名
                    var_year = int(var_filename.split('.')[-2]) # 检查年份是否在区间内
                    if var_year in time_range:
                        retrive_filelist.append(var_filename) #符合要求，加入下载列表
                        print(' --- match : ' + var_filename +' ---')
        return retrive_filelist

    def downloadFile(self,remotepath,filename):
        self.ftp.cwd(remotepath)   
        self.ftp.voidcmd('TYPE I') # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
        file_handle = open(filename,"wb").write   # 以写模式在本地打开文件
        self.ftp.retrbinary('RETR %s' % filename,file_handle, blocksize=8192)  # 下载文件


    def close(self):
        self.ftp.set_debuglevel(0)  # 关闭调试
        self.ftp.quit()

if __name__ == '__main__':
    host = 'ftp.cdc.noaa.gov'
    remote_path = '/Projects/Datasets/ncep.reanalysis/surface/'
    local_path = '/mnt/f/Data/NCEP_R1/'

    year_start = 1961
    year_last = 2016
    var_list= ['air']

    years = range(year_start,year_last+1,1) # 指定时间范围

    ftp = MyFtp(host)
    ftp.login()
    for var in var_list:
        ftp.set_localpath(var,local_path)
        file_list = ftp.set_filename(var,remote_path,years)
        for files in file_list:
            ftp.downloadFile(remote_path,files)
    ftp.close()