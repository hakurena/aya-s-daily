#!/bin/bash

#----------------------------------------------------------
#--------------  修改所需的变量&时间段  ---------------------

export Variables=("uwnd" "vwnd" "shum" "air" "omega");
export Workdir="/home/gult/aya/MAM/daily_hgt_NCEP";
export yrStrt=1961
export yrLast=2016
#----------------------------------------------------------
#----------------------------------------------------------

for (( i = 1; i <= ${#Variables[*]}; i++ )); do

	#为每个变量指定输出文件夹
	export Variable_dir=${Workdir}/${Variables[i-1]}_daily
	echo "               -------------   set var_path "${Variable_dir}"   -------------"
	#切换到存放路径，若不存在 则建立文件夹
	if [[ ! -d ${Variable_dir} ]]; then
		mkdir $Variable_dir
	fi
	cd $Variable_dir

	#取出变量名，以备组合文件名
    export Variable_name=${Variables[i-1]}

    #下载指定时间区间内的数据
	for (( j = yrStrt; j <= yrLast; j++ )); do

		#组合文件名：如uwnd.1961.nc
		export Filename=${Variable_name}.${j}.nc
		#组合下载链接
		url_link="ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/"${Filename}

		#若文件不存在则进行下载（自动断点续传）
		#！注意！不会对已存在的文件完整性进行检验！！！
		if [[ -e "${Filename}" ]]; then
			echo "        -------------   "${Filename}" exists, continue  -------------"
		else
			echo "        -------------   downloading "${Filename}"   -------------"
			echo "    ------   url: "${url_link}"   -------------"
			wget -c $url_link
		fi
	done
done
