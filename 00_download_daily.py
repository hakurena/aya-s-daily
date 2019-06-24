# -*- coding: utf-8 -*-
#!/usr/bin/python3

import os


variables = ['uwnd','vwnd','shum','air','omega']

years = range(1961,2017,1)

work_dir = '/home/gult/aya/MAM/daily_hgt_NCEP'

for var in variables:
	os.chdir(work_dir)
	data_dir = '/'+ var +'_daily'
	destination = work_dir+data_dir
	print('     --------------------- now working on : '+destination+' ---------------------------')
	if not os.path.exists(destination):
		os.mkdir(destination) 
	os.chdir(destination)

	for yr in years:
		filename = var+'.'+str(yr)+'.nc'
		url_link = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/'+filename
		command  = 'wget -c '+url_link
		# print('       ----- processing '+filename+' -----')
		if not os.path.exists('./'+filename):
			retrieve = os.system(command)
			# if not retrieve==None:
			print('complete, continue!')
		else:
			print('file exist, continue!')
			pass

