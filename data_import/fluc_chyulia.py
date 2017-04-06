from pandas import DataFrame
import pandas as pd
import numpy as np
import math
from . import models
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
import os
import json
import datetime
import csv
from decimal import *
from scipy.stats import norm

#总体波动率分析(fluctuation.html)将cost和produce合并
def fluc_cost_produce(request):
	# print("enter fluc_cost!")
	# fieldname=request.POST.get("fieldname").upper();#字段名
	SPECIFICATION=request.POST.get("SPECIFICATION");#钢种
	OPERATESHIFT=request.POST.get("OPERATESHIFT");#班次
	OPERATECREW=request.POST.get("OPERATECREW");#班别
	station=request.POST.get("station");#工位
	time1=request.POST.get("time1");
	time2=request.POST.get("time2");
	history_time1=request.POST.get("history_time1");
	history_time2=request.POST.get("history_time2");
	fluc_nature=request.POST.get("nature");#判断是cost还是prodecu
	print('fluc_nature',fluc_nature)
	############################为测试方便暂时将数据写死
	# time1='2016-01-22';
	# time2='2016-04-14';
	# history_time1='2016-01-01';
	# history_time2='2017-03-09';
	############################
	if SPECIFICATION !='blank':
		sentence_SPECIFICATION= " and SPECIFICATION='"+SPECIFICATION+"'"
	else:
		sentence_SPECIFICATION=''
	if OPERATESHIFT !='blank':
		sentence_OPERATESHIFT=" and OPERATESHIFT='"+OPERATESHIFT+"'"
	else:
		sentence_OPERATESHIFT=''
	if OPERATECREW !='blank':
		sentence_OPERATECREW=" and OPERATECREW='"+OPERATECREW+"'"
	else:
		sentence_OPERATECREW=''
	if station !='blank':
		sentence_station=" and station='"+station+"'"
	else:
		sentence_station=''
	#计算波动率的时间范围
	if time1 != '' and time2!='':
		sentence_time="and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')>'"+time1+"'and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')<'"+time2+"'"
	else:
		sentence_time=''
	#对比历史波动率的时间范围
	if history_time1 != '' and history_time2!='':
		sentence_historytime="and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')>'"+history_time1+"'and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')<'"+history_time2+"'"
	else:
		sentence_historytime=''

	time={
		'time1':time1,
		'time2':time2,
		'history_time1':history_time1,
		'history_time2':history_time2
	}
	contentVO={
		'title':'测试',
		'state':'success',
		'time':time
	}
	if fluc_nature=='cost':
		xasis_fieldname_ch=['铁水重量','耗氧量','生铁','废钢总和']
		xasis_fieldname=['MIRON_WGT','SUM_BO_CSM','COLDPIGWGT','SCRAPWGT_COUNT']
	else:
		xasis_fieldname_ch=['钢水','LDG','钢渣']
		xasis_fieldname=['TOTAL_SLAB_WGT','LDG_TOTAL_SLAB_WGT','STEEL_SLAG']

	#对任意个数字段进行字符串拼接
	field_sql=''
	for i in range(len(xasis_fieldname)):
		field_sql=field_sql+',nvl('+xasis_fieldname[i]+',0) as '+xasis_fieldname[i]

	#计算波动率的时间范围的sql
	sentence_select=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_time
	sentence="SELECT HEAT_NO "+field_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_select
	# sentence="SELECT HEAT_NO,nvl(MIRON_WGT,0) as MIRON_WGT,nvl(SUM_BO_CSM,0) as SUM_BO_CSM ,nvl(COLDPIGWGT,0) as COLDPIGWGT,nvl(SCRAPWGT_COUNT,0) as SCRAPWGT_COUNT FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_select
	

	#对比历史波动率的时间范围的sql
	sentence_selecthistory=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_historytime
	sentence_history="SELECT HEAT_NO "+field_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_selecthistory
	# sentence_history="SELECT HEAT_NO,nvl(MIRON_WGT,0) as MIRON_WGT,nvl(SUM_BO_CSM,0) as SUM_BO_CSM ,nvl(COLDPIGWGT,0) as COLDPIGWGT,nvl(SCRAPWGT_COUNT,0) as SCRAPWGT_COUNT FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_selecthistory

	# print('sentence',sentence)
	# print('sentence_history',sentence_history)

	length_result1=len(xasis_fieldname)
	#计算当前时间区间的字段波动率-------------------------------------------------------------------------------------------------
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]=sentence
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	# print('len(scrapy_records)',len(scrapy_records))


	ana_describe=calaulate_describe(scrapy_records,xasis_fieldname)
	if ana_describe['sign']==1:
		contentVO['state']='failure_current'
		return HttpResponse(json.dumps(contentVO),content_type='application/json')

	# print('-----------------------ana_describe',ana_describe)

	fluc_ratio=[]#存储各相关性字段的在当前的波动率
	for i in range(length_result1):
		describe=[ele for ele in ana_describe[xasis_fieldname[i]]]
		#value接受计算完成的字段波动率值
		value=describe[2]/describe[1]
		fluc_ratio.append(value)
	print("-------------------------fluc_ratio",fluc_ratio)


	#计算历史时间区间的字段波动率-------------------------------------------------------------------------------------------------
	sqlVO_history={}
	sqlVO_history["db_name"]="l2own"
	sqlVO_history["sql"]=sentence_history
	print(sqlVO_history["sql"])
	scrapy_records_history=models.BaseManage().direct_select_query_sqlVO(sqlVO_history)

	ana_describe_history=calaulate_describe(scrapy_records_history,xasis_fieldname)
	if ana_describe['sign']==1:
		contentVO['state']='failure_history'
		return HttpResponse(json.dumps(contentVO),content_type='application/json')
	# print('----------------------------ana_describe_history',ana_describe_history)

	fluc_ratio_history=[]#存储各相关性字段的在当前的波动率
	for i in range(length_result1):
		describe=[ele for ele in ana_describe_history[xasis_fieldname[i]]]
		#value接收计算完成的字段波动率值：标准差/期望
		value=describe[2]/describe[1]
		fluc_ratio_history.append(value)
	print("--------------------------fluc_ratio_history",fluc_ratio_history)

	#计算偏离程度
	offset_result=[]
	for i in range(length_result1):
		try:
			#当fluc_ratio_history[i]=0时，计算公式将会报错，此时表明历史数据是没有波动率的，因此偏离程度相当于无穷
			temp=(fluc_ratio[i]-fluc_ratio_history[i])/fluc_ratio_history[i]
		except:
			temp=99999999
		offset_result.append(temp)

	offset_resultlist=["%.2f%%"%(n*100) for n in list(offset_result)]
	qualitative_offset_result=qualitative_offset(offset_result)#对偏离程度进行定性判断
	fluc_ratiolist=["%.5f"%(n) for n in list(fluc_ratio)]
	fluc_ratio_historylist=["%.5f"%(n) for n in list(fluc_ratio_history)]
	contentVO['fieldname_ch']=xasis_fieldname_ch
	contentVO['fieldname_en']=xasis_fieldname
	# contentVO['ana_result']=ana_result
	# contentVO['ana_describe']=ana_describe
	# contentVO['ana_result_history']=ana_result_history
	# contentVO['ana_describe_history']=ana_describe_history
	contentVO['fluc_ratio']=fluc_ratiolist#标准偏差，即变异系数
	contentVO['fluc_ratio_history']=fluc_ratio_historylist#标准偏差，即变异系数
	contentVO['qualitative_offset_result']=qualitative_offset_result#偏离程度的定性判断
	contentVO['offset_result']=offset_result#偏离程度（小数）
	contentVO['offset_result_cent']=offset_resultlist#偏离程度(百分数)

	contentVO['sentence_select']=sentence_select
	contentVO['sentence_selecthistory']=sentence_selecthistory
	print("contentVO",contentVO)

	#time_test='2015/11/30 22:45:45'
	#string转datetime
	#d= datetime.datetime.strptime(time1,'%Y-%m-%d')
	#d1= datetime.datetime.strptime(time_test,'%Y/%m/%d %H:%M:%S')
	#datetime转string
	#str_time=d.strftime('%Y-%m-%d %H:%M:%S')
	#print(d)
	#print(d1)
	#print(d<d1)
	#print(str_time)
	return HttpResponse(json.dumps(contentVO),content_type='application/json')


#对偏离程度进行定性判断：高，偏高，正常范围，偏低，低，极端异常
def qualitative_offset(offset_result):
	#偏离程度定性标准，例如-10%~10%为正常，10%~20%为偏高，20%~40%为高，40%以上为数据异常/极端数据
	qualitative_standard=[0.1,0.3,0.4]
	qualitative_offset_result=[]
	for i in range(len(offset_result)):
		if abs(float(offset_result[i]))<=qualitative_standard[0]:
			qualitative_offset_result.append('正常范围')
		elif abs(float(offset_result[i]))<=qualitative_standard[1]:
			if float(offset_result[i])>0:#偏高
				qualitative_offset_result.append('偏高')
			else:#偏低
				qualitative_offset_result.append('偏低')
		# elif  abs(float(offset_result[i]))<=qualitative_standard[2]:
		# 	if float(offset_result[i])>0:#高
		# 		qualitative_offset_result.append('高')
		# 	else:#低
		# 		qualitative_offset_result.append('低')
		# else:#极端情况
		# 	qualitative_offset_result.append('极端异常')
		else:#取消数据异常情况
			if float(offset_result[i])>0:#高
				qualitative_offset_result.append('高')
			else:
				qualitative_offset_result.append('低')		
	return  qualitative_offset_result

#进行五数分析法
def Wushu(x):
    L=np.percentile(x,25)-1.5*(np.percentile(x,75)-np.percentile(x,25))
    U=np.percentile(x,75)+1.5*(np.percentile(x,75)-np.percentile(x,25))
    result=x[(x<U)&(x>L)]
    wushu_clean={}
    wushu_clean["minbook"]=L
    wushu_clean["maxbook"]=U
    wushu_clean["result"]=result
    return wushu_clean


#判断有效小数位数
def ivalue_num(num):
    a=str(num)
    if(a.isdigit()):
        ivalue_valid=0
    else:
        ivalue_valid=len(a.split('.')[1])
    return  ivalue_valid   

#取有效位数
def vaild(lis,ivalue_valid,data):
    for i in range(len(lis)):
        shu=lis[i]
        if ivalue_valid==0:
            shua=int(float(shu))
            data.append(shua)
        else:    
            shua=float(shu)
            shub=round(shua,ivalue_valid)
            data.append(shub)
    return data 

#波动率影响因素追溯
from . import zhuanlu
def fluc_influence(request):
	print("Enter fluc_influence")
	field=request.POST.get("field");#字段英文名
	offset_value=request.POST.get("offset_value");#一定时间范围波动率的偏离程度，
	sentence_select=request.POST.get("sentence_select");
	sentence_selecthistory=request.POST.get("sentence_selecthistory");
	print(field)
	#将待匹配的字段名设置为参数
	#field='MIRON_WGT'
	result=[]

	#从数据库读取回归系数文件
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT * FROM pro_bof_his_REGRESSION_COF where MIDFIELD='"+field +"' and INFIELD != 'BIAS' order by abs(COF) desc"
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	print(scrapy_records)
	length_result1=len(scrapy_records)

	xasis_fieldname=[]#字段英文名字数组
	regression_coefficient=[]#字段回归系数值数组
	str_sql=''
	for i in range(length_result1):
		xasis_fieldname.append(scrapy_records[i].get('INFIELD', None).upper())
		regression_coefficient.append(scrapy_records[i].get('COF', None))
		str_sql=str_sql+','+scrapy_records[i].get('INFIELD', None)
	# print(len(scrapy_records))
	# print(xasis_fieldname)
	# print(regression_coefficient)

	# #从csv文件读取回归系数文件
	# with open('data_import/regression_all_EN1.csv','r') as csvfile:
	# # with open('data_import/test.csv','r') as csvfile:
	#     reader = csv.reader(csvfile)
	#     rows= [row for row in reader]
	# aa = np.array(rows)
	# aa = sorted(aa, key=lambda d:abs(float(d[2])),reverse=True)
	# for aaa in aa:
	# 	if(aaa[0]==field):
	# 		result.append(aaa)
	# result1 = np.array(result)#转变为numpy数组格式
	# length_result1=len(result1)
	# print("长度"+str(length_result1))
	# print(result1)#根据回归系数大小排序结果
	# print("------------------")
	# xasis_fieldname=[]#字段英文名字数组
	# regression_coefficient=[]#字段回归系数值数组
	# str_sql=''
	# for i in range(length_result1):
	# 	xasis_fieldname.append(result1[i][1])
	# 	regression_coefficient.append(result1[i][2])
	# 	str_sql=str_sql+','+result1[i][1]
	# # print(str_sql)


	contentVO={
		'title':'测试',
		'state':'success'
	}

	#计算当前时间区间的字段波动率-------------------------------------------------------------------------------------------------
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT HEAT_NO" +str_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no>'150000'"+sentence_select
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	print('len(scrapy_records)',len(scrapy_records))

	# try:#对于查询结果无数据的情况
	ana_describe=calaulate_describe(scrapy_records,xasis_fieldname)
	# except:
	# 	contentVO['state']='failure_current'
		# return HttpResponse(json.dumps(contentVO),content_type='application/json')

	# print('-----------------------ana_describe',ana_describe)

	fluc_ratio=[]#存储各相关性字段的在当前的波动率
	for i in range(length_result1):
		if ana_describe['state'][xasis_fieldname[i]]=='wrong':
			fluc_ratio.append('wrong')
			continue
		describe=[ele for ele in ana_describe[xasis_fieldname[i]]]
		#value接受计算完成的字段波动率值
		value=describe[2]/describe[1]
		fluc_ratio.append(value)
	print("-------------------------fluc_ratio",fluc_ratio)


	#计算历史时间区间的字段波动率-------------------------------------------------------------------------------------------------
	sqlVO_history={}
	sqlVO_history["db_name"]="l2own"
	sqlVO_history["sql"]="SELECT HEAT_NO" +str_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no>'150000' "+sentence_selecthistory
	print(sqlVO_history["sql"])
	scrapy_records_history=models.BaseManage().direct_select_query_sqlVO(sqlVO_history)

	# try:
	ana_describe_history=calaulate_describe(scrapy_records_history,xasis_fieldname)
	# except:
	# 	contentVO['state']='failure_history'
		# return HttpResponse(json.dumps(contentVO),content_type='application/json')

	# print('----------------------------ana_describe_history',ana_describe_history)

	fluc_ratio_history=[]#存储各相关性字段的在当前的波动率
	for i in range(length_result1):
		if ana_describe_history['state'][xasis_fieldname[i]]=='wrong':
			fluc_ratio_history.append('wrong')
			continue
		describe=[ele for ele in ana_describe_history[xasis_fieldname[i]]]
		#value接收计算完成的字段波动率值：标准差/期望
		value=describe[2]/describe[1]
		fluc_ratio_history.append(value)
	print("--------------------------fluc_ratio_history",fluc_ratio_history)


	#计算偏离程度
	offset_result=[]
	for i in range(length_result1):
		if fluc_ratio[i]=='wrong' or fluc_ratio_history[i]=='wrong':
			offset_result.append('wrong')
			continue
		try:
			#当fluc_ratio_history[i]=0时，计算公式将会报错，此时表明历史数据是没有波动率的，因此偏离程度相当于无穷
			temp=(fluc_ratio[i]-fluc_ratio_history[i])/fluc_ratio_history[i]
		except:
			temp=99999999
		offset_result.append(temp)

	print(xasis_fieldname)
	print("偏离程度")
	print(offset_result)

	xasis_fieldname_result=[]#字段英文名字数组
	regression_coefficient_result=[]#字段回归系数值数组
	offset_result_final=[]#偏离程度值
	#即字段偏离高，则正相关应对应偏高，负相关应对应偏低
	if float(offset_value)>=0:#读取偏离程度的值，如果前端偏离程度表示为百分比，例如12.6%。则需要截取12.6来判断其正负：offset_value[0:-1]
		for i in range(length_result1):
			if offset_result[i]==None  or offset_result[i]=='wrong':#由于数据清洗的问题，暂且将NB字段如此处理，因为NB字段的所有数据均相同，导致数据清洗时将所有数据都清除了
				continue
			if float(regression_coefficient[i]) * float(offset_result[i]) >=0:
				xasis_fieldname_result.append(xasis_fieldname[i])
				regression_coefficient_result.append(regression_coefficient[i])
				offset_result_final.append(offset_result[i])
	else:
		for i in range(length_result1):
			if offset_result[i]==None  or offset_result[i]=='wrong':
				continue
			if float(regression_coefficient[i]) * float(offset_result[i]) <=0:
				xasis_fieldname_result.append(xasis_fieldname[i])
				regression_coefficient_result.append(regression_coefficient[i])
				offset_result_final.append(offset_result[i])
				
	contentVO['xasis_fieldname']=xasis_fieldname_result#回归系数因素英文字段名
	contentVO['regression_coefficient']=regression_coefficient_result#字段回归系数值
	contentVO['offset_result']=offset_result_final#回归系数因素字段偏离值
	contentVO['offset_result_cent']=["%.2f%%"%(n*100) for n in list(offset_result_final)]
	contentVO['offset_number']=len(xasis_fieldname_result)#回归系数最大因素所取字段个数
	print("字段名字")
	print(xasis_fieldname_result)
	print("回归系数")
	print(regression_coefficient_result)
	print("偏离程度")
	print(offset_result_final)

	#查询转炉工序字段名中英文对照
	ana_result={}
	ana_result=zhuanlu.PRO_BOF_HIS_ALLFIELDS
	En_to_Ch_result=[]
	for i in range(len(xasis_fieldname_result)):
		En_to_Ch_result.append(ana_result[xasis_fieldname_result[i]])
	print(En_to_Ch_result)
	contentVO['En_to_Ch_result']=En_to_Ch_result#回归系数最大因素中文字段名字
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#仅进行数据清洗，并计算describe参数（可以是任意个字段），不计算概率分布和正态分布
def calaulate_describe(scrapy_records,fieldname):
	# print(scrapy_records[1:5])
	ana_describe={}
	ana_describe['shuxing']=['count','mean','std','min','25%','50%','75%','max']
	state={}#存储各个字段的状态
	sign=0#标志位，表示是否出现无数据状态
	print('fieldname',fieldname)
	for bookno in fieldname:
		print('计算字段：',bookno)
		state[bookno]='normal'#初始为正常
		ivalue_i=[]
		# print('len(scrapy_records)',len(scrapy_records))
		for n in range(len(scrapy_records)):
			ivalue = scrapy_records[n].get(bookno,None)
			if ivalue !=None and ivalue !=0:
				 ivalue=ivalue
				 ivalue_b=str(ivalue)
				 ivalue_valid=ivalue_num(ivalue_b)#小数位数
				 ivalue_i.append(ivalue_valid)
				 ivalue_i.sort(reverse=True)
		if ivalue_i==[]:#若字段为空，表示该字段没有数据
			state[bookno]='wrong'#若出现问题，将状态改为wrong
			sign=1
			continue
		ivalue_valid=ivalue_i[0]#取所有有效位数的最大个数
		# print(ivalue_valid)		
		for i in range(len(scrapy_records)):
			value = scrapy_records[i].get(bookno,None)
			if value != None :
				scrapy_records[i][bookno] = float(value)			
		frame=DataFrame(scrapy_records)	
		df_single=frame[['HEAT_NO',bookno]]
		# print('df_single',df_single)
		df=df_single.sort_values(by=bookno)
		dfr=df[df>0].dropna(how='any')
		# print('清洗前的字段',dfr[bookno])

		cleanbook=Wushu(dfr[bookno])
		# print('清洗后的字段',cleanbook)
		minbook=cleanbook["minbook"]
		maxbook=cleanbook["maxbook"]	
		if(minbook==maxbook):#不符合正态分布规律，不进行五数分析
			print("no")
			clean=dfr[bookno]		
		else:
			print("yes")
			clean=cleanbook["result"]				
		# print("minbook")
		# print(minbook)
		# print("maxbook")
		# print(maxbook)
		# print(type(clean))
		# if bookno=='SCRAP_16040101':
		# 	print(clean)
		if len(clean)<5:#如果数据个数小于5，则跳过这个字段的计算
			state[bookno]='wrong'#若出现问题，将状态改为wrong
			sign=1
			continue

		describe=clean.describe()

		# print(describe)

		# desx=[ele for ele in describe.index]
		desy=[ele for ele in describe]

		d4_data=[]
		desy1=vaild(desy,ivalue_valid,d4_data)

		#desy1内容依次为count、mean、std、min、25%、50%、75%、max
		#计算波动率：标准差/期望

		# ana_describe['scopeb']=desx
		ana_describe[bookno]=desy1
	ana_describe['state']=state#用于详细表示各个字段的数据情况，筛选条件下的无数据表示为wrong，正常情况表示为normal
	ana_describe['sign']=sign#用于表征是否出现了字段的无数据现象
	# print('state',state)
	return ana_describe