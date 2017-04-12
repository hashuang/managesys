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

#总体波动率分析(fluctuation.html)

def fluc_produce(request):
	print("enter whole_analy!")
	# fieldname=request.POST.get("fieldname").upper();#字段名
	SPECIFICATION=request.POST.get("SPECIFICATION");#钢种
	OPERATESHIFT=request.POST.get("OPERATESHIFT");#班次
	OPERATECREW=request.POST.get("OPERATECREW");#班别
	station=request.POST.get("station");#工位
	time1=request.POST.get("time1");
	time2=request.POST.get("time2");
	history_time1=request.POST.get("history_time1");
	history_time2=request.POST.get("history_time2");
	#为测试方便暂时将数据写死
	# time1='2016-01-22';
	# time2='2016-04-14';
	# history_time1='2016-01-01';
	# history_time2='2017-03-09';
	
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
	#计算波动率的时间范围的sql
	# sentence="SELECT HEAT_NO,"+fieldname+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_time
	sentence="SELECT HEAT_NO,nvl(C,0) as C,nvl(SI,0) as SI ,nvl(MN,0) as MN,nvl(P,0) as P ,nvl(S,0) as S, nvl(STEELWGT,0)as STEELWGT,nvl(FINAL_TEMP_VALUE,0)as FINAL_TEMP_VALUE  FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_time
	# sentence="SELECT HEAT_NO,nvl(MIRON_WGT,0) as MIRON_WGT FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_time
	sentence_select=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_time
	#对比历史波动率的时间范围的sql
	# sentence_history="SELECT HEAT_NO,"+fieldname+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_historytime
	sentence_history="SELECT HEAT_NO,nvl(C,0) as C,nvl(SI,0) as SI ,nvl(MN,0) as MN,nvl(P,0) as P ,nvl(S,0) as S, nvl(STEELWGT,0)as STEELWGT,nvl(FINAL_TEMP_VALUE,0)as FINAL_TEMP_VALUE  FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_historytime
	sentence_selecthistory=sentence_SPECIFICATION+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station+sentence_historytime
	
	time={
		'time1':time1,
		'time2':time2,
		'history_time1':history_time1,
		'history_time2':history_time2
	}
	contentVO={
		'title':'测试',
		'state':'success',
		'time1':time1,
		'time2':time2,
		'history_time1':history_time1,
		'history_time2':history_time2,
		'time':time
	}
	xasis_fieldname_ch=['C含量','SI含量','MN含量','P含量','S含量','FE含量','重量','温度']
	xasis_fieldname=['C','SI','MN','P','S','FE','STEELWGT','FINAL_TEMP_VALUE']
	# for i in range(len(fieldname_en)):
	# 	#ana_describe的numb参数顺序为count、mean、std/min、25%/50%/75%/max
	# 	ana_result_temp,ana_describe_temp=calaulate_describe(scrapy_records,fieldname_en[i])#主动计算波动率
	# 	ana_result_history_temp,ana_describe_history_temp=num_describe(scrapy_records_history,fieldname_en[i])#被对比的历史数据
	# 	std_dev_temp=ana_describe_temp['numb'][2]/ana_describe_temp['numb'][1]
	# 	std_dev_history_temp=ana_describe_history_temp['numb'][2]/ana_describe_history_temp['numb'][1]#标准偏差，即变异系数
	# 	offset_result_temp=(std_dev_temp-std_dev_history_temp)/std_dev_history_temp#偏离程度

	# 	# ana_result.append(ana_result_temp)#概率分布
	# 	ana_describe.append(ana_describe_temp)#最大最小值、期望标准差等参数统计结果
	# 	# ana_result_history.append(ana_result_history_temp)#历史数据概率分布
	# 	ana_describe_history.append(ana_describe_history_temp)#历史数据最大最小值、期望标准差等参数统计结果
	# 	offset_result.append(offset_result_temp)#波动率（标准差）的偏离程度
	# 	std_dev.append(std_dev_temp)
	# 	std_dev_history.append(std_dev_history_temp)

	length_result1=len(xasis_fieldname)
	#计算当前时间区间的字段波动率-------------------------------------------------------------------------------------------------
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]=sentence
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	# print('len(scrapy_records)',len(scrapy_records))
	ana_describe=calaulate_describe(scrapy_records,xasis_fieldname)
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
	fluc_ratiolist=["%.4f"%(n) for n in list(fluc_ratio)]
	fluc_ratio_historylist=["%.4f"%(n) for n in list(fluc_ratio_history)]
	contentVO['fieldname_ch']=xasis_fieldname_ch
	contentVO['fieldname_en']=xasis_fieldname
	# contentVO['ana_result']=ana_result
	# contentVO['ana_describe']=ana_describe
	# contentVO['ana_result_history']=ana_result_history
	# contentVO['ana_describe_history']=ana_describe_history
	contentVO['fluc_ratio']=fluc_ratiolist#标准偏差，即变异系数(波动率)
	contentVO['fluc_ratio_history']=fluc_ratio_historylist#标准偏差，即变异系数
	contentVO['offset_result']=offset_result#偏离程度（小数）
	contentVO['offset_result_cent']=offset_resultlist#偏离程度(百分数)
	contentVO['qualitative_offset_result']=qualitative_offset_result#偏离程度的定性判断

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

#同时计算各类最大最小等参数及正态分布、概率分布
def num_describe(scrapy_records,bookno):
	print(scrapy_records[1:5])
	ivalue_i=[]
	for n in range(len(scrapy_records)):
		ivalue = scrapy_records[n].get(bookno,None)
		if ivalue !=None and ivalue !=0:
			 ivalue=ivalue
			 ivalue_b=str(ivalue)
			 ivalue_valid=ivalue_num(ivalue_b)#小数位数
			 ivalue_i.append(ivalue_valid)
			 ivalue_i.sort(reverse=True)
	ivalue_valid=ivalue_i[0]#取所有有效位数的最大个数
	print(ivalue_valid)		
	for i in range(len(scrapy_records)):
		value = scrapy_records[i].get(bookno,None)
		if value != None :
			scrapy_records[i][bookno] = float(value)			
	frame=DataFrame(scrapy_records)	
	df=frame.sort_values(by=bookno)
	dfr=df[df>0].dropna(how='any')
	#print(dfr['1622324'])
	#print(dfr[bookno].dtype)
	cleanbook=Wushu(dfr[bookno])
	minbook=cleanbook["minbook"]
	maxbook=cleanbook["maxbook"]	
	if(minbook==maxbook):#不符合正态分布规律
		print("no")
		clean=dfr[bookno]		
	else:
		print("yes")
		clean=cleanbook["result"]				
	print("minbook")
	print(minbook)
	print("maxbook")
	print(maxbook)
	print(type(clean))
	if clean is not None:
		if(clean.max==clean.min()):
			bc=1
		else:	
			bc=(clean.max()-clean.min())/50
		bcq=math.ceil(bc*1000)/1000
		print(bcq)
		try:
			section=pd.cut(clean,math.ceil((clean.max()-clean.min())/bcq))
			end=pd.value_counts(section,sort=False)/clean.count()
			describe=clean.describe()
		except ValueError as e:
		 	print(e)
	numx=[ele for ele in end.index]
	#numy=[ele for ele in end]
	desx=[ele for ele in describe.index]
	desy=[ele for ele in describe]
	print(numx)
	print(describe)
	#contentVO={
		#'title':'测试',
		#'state':'success'
	#}
	s1=pd.Series(numx)
	d1=getA(s1)
	d2=getB(s1)
	d1_data=[]
	d2_data=[]
	#d3_data=[]
	d4_data=[]
	d1_valid=vaild(d1,ivalue_valid,d1_data)
	for i in range(len(d1_valid)):
		if d1_valid[i]<0:
			d1_valid[i]=0
	d2_valid=vaild(d2,ivalue_valid,d2_data)
	numx1=list(set(d1_valid).union(set(d2_valid)))
	numx2=sorted(numx1)
	# print("numx2:")
	# print(numx2)
	sections=[]
	numx3=union_section(numx2,sections)
	cut1=pd.cut(clean,numx2)
	end1=pd.value_counts(cut1,sort=False)/clean.count()
	numy=[ele for ele in end1]
	# print("end1:")
	# print(end1)
	#numy1=vaild(numy,ivalue_valid,d3_data)
	numy1=["%.6f"%(n) for n in numy]
	desy1=vaild(desy,ivalue_valid,d4_data)
	print("x轴:")
	print(numx3)
	print("y轴:")
	print(numy1)
	#desy1内容依次为count、mean、std、min、25%、50%、75%、max
	aa=(desy1[7]-desy1[3])/50
	normx_array = np.arange(desy1[3],desy1[7],aa)  
	normy_array = norm.pdf(normx_array,desy1[1],desy1[2])
	#转换格式，限制小数位数
	normx=["%.4f"%(n) for n in list(normx_array)]
	normy=["%.7f"%(n) for n in list(normy_array)]


	ana_result={}
	ana_result['scope']=numx3
	ana_result['num']=numy1
	ana_result['normx']=normx
	ana_result['normy']=normy
	#contentVO['result']=ana_result
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy1
	#contentVO['describe']=ana_describe
	return ana_result,ana_describe

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
			# state[bookno]='wrong'		
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

#去括号取左侧的数（计算概率分布时需要用到）
def getA(s):
    s0 = list(s)
    data = []
    for a in s0:
        a1 = a.split(',')
        if len(a1)==1:
            data.append(a1[0][1:])
        else:
            data.append(a1[0][1:])
    return data

#去括号取右侧的数（计算概率分布时需要用到）    
def getB(s):
    s0 = list(s)
    data = []
    for a in s0:
        a1 = a.split(',')
        if len(a1)==1:
            data.append(a1[1][:-1])
        else:
            data.append(a1[1][:-1])
    return data	

#拼接区间（计算概率分布时需要用到） 
def union_section(section_point,sections):
    for i in range(len(section_point)):
        section=None
        if i<len(section_point)-1:
            section='('+str(section_point[i])+','+str(section_point[i+1])+']'
            sections.append(section)
    return sections 

#判断有效位数
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
		xasis_fieldname.append(scrapy_records[i].get('INFIELD', None))
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
	offset_result_nature=simple_offset(offset_result_final)
	print("简单定性判断")
	print(offset_result_nature)
	contentVO['offset_result_nature']=offset_result_nature
	#查询转炉工序字段名中英文对照
	ana_result={}
	ana_result=zhuanlu.PRO_BOF_HIS_ALLFIELDS
	En_to_Ch_result=[]
	for i in range(len(xasis_fieldname_result)):
		En_to_Ch_result.append(ana_result[xasis_fieldname_result[i]])
	print(En_to_Ch_result)

	ana_result_score={}
	ana_result_score=zhuanlu.PRO_BOF_HIS_ALLFIELDS_SCORE
	En_to_Ch_result_score=[]
	for i in range(len(xasis_fieldname_result)):
		En_to_Ch_result_score.append(ana_result_score[xasis_fieldname_result[i]])
	print("带标记的中文字段")	
	print(En_to_Ch_result_score)

	#取前5个权重最大的字段按操作顺序（表结构）进行排序
	#中文字段与偏离程度合并，需联动排序
	offset_result_final_maxfive=offset_result_final[0:5]
	En_to_Ch_result_maxfive=En_to_Ch_result[0:5]
	dicty=dict(zip(En_to_Ch_result_maxfive,offset_result_final_maxfive))
	print('组合字段中文名和偏离程度')
	print(dicty)

	#按操作排序
	a=[]
	En_to_Ch_result_score=[]
	xasis_fieldname_result_maxfive=xasis_fieldname_result[0:5]
	for i in range(len(xasis_fieldname_result_maxfive)):
		a.append(ana_result_score[xasis_fieldname_result_maxfive[i]])
	# print('带标记的字段')
	# print(a)
	L=sorted(a,key=by_score)
	for i in range(len(xasis_fieldname_result_maxfive)):
		En_to_Ch_result_score.append(L[i][0])
	print('操作排序后中文名')
	print(En_to_Ch_result_score)

	#联动排序偏离程度
	offset_result_final_maxfive_order=[]
	for i in range(len(En_to_Ch_result_score)):
		offset_result_final_maxfive_order.append(dicty[En_to_Ch_result_score[i]])
	print('按操作排序后字段偏离程度')
	print(offset_result_final_maxfive_order)

	pos=map(lambda x:abs(x),offset_result_final_maxfive_order)
	posNum=["%.2f%%"%(n*100) for n in list(pos)]
	print("格式化")
	print(posNum)

	contentVO['En_to_Ch_result']=En_to_Ch_result#回归系数最大因素中文字段名字
	contentVO['En_to_Ch_result_score']=En_to_Ch_result_score#按操作排序后字段中文名
	contentVO['posNum']=posNum#按操作排序后偏离程度格式话
	return HttpResponse(json.dumps(contentVO),content_type='application/json')
def by_score(t):
    return t[1]	
def fluc_cost_pop(request):
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
	# fluc_nature=request.POST.get("nature");#判断是cost还是prodecu
	# print('fluc_nature',fluc_nature)
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
	# if fluc_nature=='cost':
	xasis_fieldname_ch=['钢水C含量','钢水SI含量','钢水MN含量','钢水P含量','钢水S含量','钢水重量','钢水温度']
	xasis_fieldname=['C','SI','MN','P','S','STEELWGT','FINAL_TEMP_VALUE']
	# else:
	# 	xasis_fieldname_ch=['钢水','LDG','钢渣']
	# 	xasis_fieldname=['TOTAL_SLAB_WGT','LDG_TOTAL_SLAB_WGT','STEEL_SLAG']

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
	#对相关性字段展示做简单定性分析	正数为偏高负数为偏低
def simple_offset(offset_result_final):
	#偏离程度定性标准，例如-10%~10%为正常，10%~20%为偏高，20%~40%为高，40%以上为数据异常/极端数据
	offset_result_nature=[]#相关字段定性分析
	for i in range(len(offset_result_final)):
		if float(offset_result_final[i]>0):
			offset_result_nature.append('偏高')
		else:
			offset_result_nature.append('偏低')	
	return  offset_result_nature	
