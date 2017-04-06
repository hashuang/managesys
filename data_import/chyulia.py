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
#from . import hashuang

#计算投入/输出产品分布
def cost_produce(request):
	print("enter cost_produce")
	heat_no=request.POST.get("heat_no");
	# print(heat_no)
	nature=request.POST.get("nature");#区别是cost还是produce
	# print('nature',nature)
	contentVO={
		'title':'测试',
		'state':'success'
	}
	if nature=='cost':
		xaxis=['铁水重量','耗氧量','废钢总和','生铁']
		xasis_fieldname=['MIRON_WGT','SUM_BO_CSM','SCRAPWGT_COUNT','COLDPIGWGT']
		danwei=['Kg','NM3','Kg','Kg']
	else:
		xaxis=['钢水','LDG','钢渣']
		xasis_fieldname=['TOTAL_SLAB_WGT','LDG_TOTAL_SLAB_WGT','STEEL_SLAG']
		danwei=['Kg','NM3','Kg']
	

#对任意个数字段进行字符串拼接
	field_sql=''
	for i in range(len(xasis_fieldname)):
		field_sql=field_sql+',nvl('+xasis_fieldname[i]+',0) as '+xasis_fieldname[i]

	sqlVO={}
	sqlVO["db_name"]="l2own"
	# sqlVO["sql"]="SELECT HEAT_NO,nvl(TOTAL_SLAB_WGT,0) as TOTAL_SLAB_WGT,nvl(LDG_TOTAL_SLAB_WGT,0) as LDG_TOTAL_SLAB_WGT ,nvl(STEEL_SLAG,0) as STEEL_SLAG FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no='"+heat_no+"'";
	sqlVO["sql"]="SELECT HEAT_NO "+field_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO='"+heat_no+"'";
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	
	# for i in range(len(xasis_fieldname)):
	# 	value = scrapy_records[0].get(xasis_fieldname[i],None)
	# 	if value != None :
	# 		scrapy_records[0][xasis_fieldname[i]] = float(value)
	# frame=DataFrame(scrapy_records)
	# yaxis=[frame.TOTAL_SLAB_WGT[0],frame.LDG_TOTAL_SLAB_WGT[0],frame.STEEL_SLAG[0]]

	yaxis=[]#存放单炉次的字段值
	for i in range(len(xasis_fieldname)):
		value = scrapy_records[0].get(xasis_fieldname[i],None)
		if value != None :
			yaxis.append(float(value))
		else:
			yaxis.append(value)

	print('xasis_fieldname',xasis_fieldname)
	print('yaxis',yaxis)
	offset_result=offset(xasis_fieldname,yaxis)#计算偏离程度函数的返回值
	qualitative_offset_result=qualitative_offset(offset_result)#对偏离程度进行定性判断
	offset_resultlist=["%.2f%%"%(n*100) for n in list(offset_result)]
	print('offset_result',offset_result)
	print('offset_resultlist',offset_resultlist)
	ana_result={}
	ana_result['heat_no']=heat_no#炉次号
	ana_result['xname']=xaxis#字段中文名字
	ana_result['xEnglishname']=xasis_fieldname#字段英文名字
	ana_result['danwei']=danwei#字段的数值单位
	ana_result['yvalue']=yaxis#该炉次字段的实际值
	if nature=='cost':
		ana_result['attribute']='成本投入量'
	else:
		ana_result['attribute']='输出产品量'
	ana_result['offset_result']=offset_resultlist#各字段的偏离程度值
	ana_result['qualitative_offset_result']=qualitative_offset_result#各字段的偏离程度定性判断结果
	contentVO['result']=ana_result
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#通过从数据库中查询期望等参数来输入/产出图中的偏离程度
def offset(xasis_fieldname,yaxis):
	offset_result=[]
	sqlVO={}
	sqlVO["db_name"]="l2own"
	print('len(xasis_fieldname)',len(xasis_fieldname))
	parameters=["MAX_VALUE","MIN_VALUE","DESIRED_VALUE","STANDARD_DEVIATION"]
	for i in range (0,len(xasis_fieldname)):#实际计算范围为从0到len(xasis_fieldname)-1
		# if yaxis[i]==0 or yaxis[i] is None:
		# 	offset_result.append(None)
		# 	continue;
		sqlVO["sql"]="SELECT MAX_VALUE,MIN_VALUE,DESIRED_VALUE,STANDARD_DEVIATION FROM qg_user.PRO_BOF_HIS_ALLSTRUCTURE where DATA_ITEM_EN = \'"+xasis_fieldname[i]+"\'"
		print(sqlVO["sql"])
		scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
		print(scrapy_records)
		# print(temp_array)
		# print(yaxis[i])
		# print(isinstance(yaxis[i],float))#判断数据类型
		for j in range (len(parameters)):
			value = scrapy_records[0].get(parameters[j],None)
			if value != None :
				scrapy_records[0][parameters[j]] = float(value)

		try:
			temp_value=(float(yaxis[i])-scrapy_records[0]['DESIRED_VALUE'])/(scrapy_records[0]['MAX_VALUE']-scrapy_records[0]['MIN_VALUE'])
		except:
			temp_value=None
		offset_result.append(temp_value)
	print('offset_result',offset_result)
	return offset_result


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


#同时计算概率分布和正态分布
from scipy.stats import norm
def probability_normal(request):
	print("同时计算概率直方图和正态分布图！")

	#获取信息
	heat_no=request.POST.get("heat_no");#炉次号
	bookno=request.POST.get("fieldname_english").upper();#字段英文名
	fieldname_chinese=request.POST.get("fieldname_chinese")#字段中文名
	offset_value=request.POST.get("offset_value");#偏离值
	# offset_value=float(offset_value_temp[1:-1])/100
	actual_value=float(request.POST.get("actual_value"))#实际值
	coloum_number=int(request.POST.get("coloum_number"))#定义概率直方图的柱状个数
	print(heat_no,bookno,actual_value);
	# print(scrapy_records[1:5])

	#进行数据库查询
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT HEAT_NO,"+bookno+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS"
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)

	#进行数据清洗
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
			bc=(clean.max()-clean.min())/coloum_number
		bcq=math.ceil(bc*1000)/1000
		print(bcq)
		try:
			#计算概率直方分布
			section=pd.cut(clean,math.ceil((clean.max()-clean.min())/bcq))
			end=pd.value_counts(section,sort=False)/clean.count()
			describe=clean.describe()#参数统计信息
		except ValueError as e:
		 	print(e)
	numx=[ele for ele in end.index]
	#numy=[ele for ele in end]
	desx=[ele for ele in describe.index]
	desy=[ele for ele in describe]
	print(numx)
	print(describe)

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
	print("x轴:")
	print(numx3)
	print("y轴:")
	print(numy1)
	desy1=vaild(desy,ivalue_valid,d4_data)

	#计算正态分布起始--------------------------------------------------
	#desy1内容依次为count、mean、std、min、25%、50%、75%、max
	aa=(desy1[7]-desy1[3])/50
	normx_array = np.arange(desy1[3],desy1[7],aa)  
	normy_array = norm.pdf(normx_array,desy1[1],desy1[2])
	#转换格式，限制小数位数
	normx=["%.4f"%(n) for n in list(normx_array)]
	normy=["%.7f"%(n) for n in list(normy_array)]
	#计算正态分布结束---------------------------------------------------------

	ana_result={}
	#概率分布：x轴：scope,y轴：num
	ana_result['scope']=numx3#区间数组
	ana_result['num']=numy1#区间对应值

	#正态分布：x轴：normx,y轴：numy
	ana_result['normx']=normx
	ana_result['normy']=normy

	#统计参数：内容依次为count、mean、std、min、25%、50%、75%、max
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy1
	


	#---------判断该炉次该字段在历史正态分布曲线中距离最近的取样点-----------
	temp=float(normx[0])
	temp_index=0
	for i in range (0,len(normx)-1):
		former=float(normx[i])
		latter=float(normx[i+1])
		#print(former,latter)
		if (actual_value>former) & (actual_value<=latter):
			temp_index=i
			if abs(actual_value-former)<abs(actual_value-latter):
				temp=former
			else:
				temp=latter
			break;
	print(temp_index,temp)

	#单炉次的一些信息
	base_result={}
	base_result['fieldname']=bookno#字段英文名
	base_result['fieldname_chinese']=fieldname_chinese#字段中文名
	base_result['actual_value']=actual_value#自身值
	# base_result['offset_value']="%.2f%%"%(offset_value*100)#偏离程度(当offset_value为小数形式时可用此行代码)
	base_result['offset_value']=offset_value#偏离程度(当offset_value已经为百分号形式时可用此行代码)
	# return base_result
	base_result['match_index']=temp_index#对应序号
	base_result['match_value']=str("%.4f"%(temp))#距离最近的值,由于在之前将其转化为float类型进行过数据对比，例如，123.0000被默认识别为123，当再次转化为str类型时，则也成了‘123’，因此就与normx的值对不上了
	
	#返回计算结果
	contentVO={
	'title':'测试',
	'state':'success'
	}
	contentVO['ana_result']=ana_result#概率分布及正态分布
	contentVO['ana_describe']=ana_describe#统计数据的描述
	contentVO['base_result']=base_result#该炉次的相关信息
	print('contentVO',contentVO)
	return HttpResponse(json.dumps(contentVO),content_type='application/json')
	
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

#数据清洗+计算概率分布（画概率直方图）
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
			bc=(clean.max()-clean.min())/7
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
	ana_result={}
	ana_result['scope']=numx3
	#print(ana_result['scope'])
	ana_result['num']=numy1
	#contentVO['result']=ana_result
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy1
	#contentVO['describe']=ana_describe
	return ana_result,ana_describe



#数据清洗+计算正态分布（画正态分布图）
#与num_describe的区别是，进行数据清洗并计算正态分布，而不进行概率直方图区间计算
from scipy.stats import norm
def data_clean(scrapy_records,bookno):
	print("data_clean:"+bookno);
	if bookno=='"AS"':
		bookno=bookno.split('"')[1]
	for i in range(len(scrapy_records)):
		value = scrapy_records[i].get(bookno,None)
		if value != None :
			scrapy_records[i][bookno] = float(value)
	frame=DataFrame(scrapy_records)	#可能有多列数据
	frame_formal=frame[['HEAT_NO',bookno]]
	#print(frame[bookno])
	df=frame.sort_values(by=bookno)
	dfr=df[df>0].dropna(how='any')
	#print(dfr[bookno].dtype)
	clean=Wushu(dfr[bookno])
	if bookno=="NB":
		print(clean)
	#print("clean",clean)
	#平均值/期望值
	dataclean_result={}
	avg_value=np.mean(clean)
	print("期望值",avg_value)
	#标准差
	std_value=np.std(clean)
	print("标准差",std_value)
	#方差
	var_value=np.var(clean)
	print("方差",var_value)
	#normx,normy=Norm_dist(avg_value,var_value)
	print("min",clean.min())
	print("max",clean.max())
	aa=(clean.max()-clean.min())/50
	normx = np.arange(clean.min(),clean.max(),aa)  
	normy = norm.pdf(normx,avg_value,std_value)
	dataclean_result['clean_min']=clean.min()
	dataclean_result['clean_max']=clean.max()
	dataclean_result['avg_value']=avg_value#期望值
	dataclean_result['std_value']=std_value#标准差
	dataclean_result['normx']=normx#x轴取样点
	dataclean_result['normy']=normy#正态分布取样点对应的Y轴取值
	return dataclean_result


#影响因素追溯
from . import zhuanlu
def max_influence(request):
	print("Enter max_influence")
	heat_no=request.POST.get("heat_no");
	field=request.POST.get("field");
	offset_value=request.POST.get("offset_value");#炉次字段的偏离程度，
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
	# print(str_sql)

	sqlVO={}
	sqlVO["db_name"]="l2own"
	# sqlVO["sql"]="SELECT HEAT_NO,nvl("+xasis_fieldname[0]+",0) as "+xasis_fieldname[0]+",nvl("+xasis_fieldname[1]+",0) as "+xasis_fieldname[1]+",nvl("+xasis_fieldname[2]+",0) as "+xasis_fieldname[2]+",nvl("+xasis_fieldname[3]+",0) as "+xasis_fieldname[3]+",nvl("+xasis_fieldname[4]+",0) as "+xasis_fieldname[4]+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no='"+prime_cost+"'";
	sqlVO["sql"]="SELECT HEAT_NO" +str_sql+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no='"+heat_no+"'";
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	#将查询所得值全部转变为float格式（动态，适用于不同个数的xasis_fieldname长度）
	yaxis=[]#各相关性字段的实际值
	for i in range(length_result1):
		value = scrapy_records[0].get(xasis_fieldname[i],None)
		if value != None :
			scrapy_records[0][xasis_fieldname[i]] = Decimal(value)
		else:
			scrapy_records[0][xasis_fieldname[i]] = 0#将空值None暂时以0填充
		yaxis.append(value)
	# frame=DataFrame(scrapy_records)
	# print("frame",frame)
	# for i in range(length_result1):
	# 	yaxis.append(frame[xasis_fieldname[i]][0])
	# yaxis=[frame[xasis_fieldname[0]][0],frame[xasis_fieldname[1]][0],frame[xasis_fieldname[2]][0],frame[xasis_fieldname[3]][0],frame[xasis_fieldname[4]][0]]
	print("yaxis",yaxis)
	contentVO={
		'title':'测试',
		'state':'success'
	}
	offset_result=offset(xasis_fieldname,yaxis)
	print(xasis_fieldname)
	print("偏离程度")
	print(offset_result)
	xasis_fieldname_result=[]#字段英文名字数组
	regression_coefficient_result=[]#字段回归系数值数组
	offset_result_final=[]#偏离程度值
	#即字段偏离高，则正相关应对应偏高，负相关应对应偏低
	if float(offset_value[0:-1])>=0:#读取隐藏域的值，由于隐藏域的偏离表示为百分比，例如12.6%。因此截取12.6来判断其正负
		for i in range(length_result1):
			if offset_result[i]==None or xasis_fieldname[i]=='NB':#由于数据清洗的问题，暂且将NB字段如此处理，因为NB字段的所有数据均相同，导致数据清洗时将所有数据都清除了
				continue
			if float(regression_coefficient[i]) * float(offset_result[i]) >=0:
				xasis_fieldname_result.append(xasis_fieldname[i])
				regression_coefficient_result.append(regression_coefficient[i])
				offset_result_final.append(offset_result[i])
	else:
		for i in range(length_result1):
			if offset_result[i]==None or xasis_fieldname[i]=='NB':
				continue
			if float(regression_coefficient[i]) * float(offset_result[i]) <=0:
				xasis_fieldname_result.append(xasis_fieldname[i])
				regression_coefficient_result.append(regression_coefficient[i])
				offset_result_final.append(offset_result[i])
	contentVO['xasis_fieldname']=xasis_fieldname_result#回归系数因素英文字段名
	contentVO['regression_coefficient']=regression_coefficient_result#字段回归系数值
	contentVO['offset_result']=offset_result_final#回归系数因素字段偏离值
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
	
#计算单炉次字段值
def single_heat(heat_no,fieldname):
	print("success")
	print(heat_no,fieldname)
	sqlVO1={}
	sqlVO1["db_name"]="l2own"
	sqlVO1["sql"]="SELECT HEAT_NO,nvl("+fieldname+",0) as field FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no='"+heat_no+"'";
	print(sqlVO1["sql"])
	scrapy_records1=models.BaseManage().direct_select_query_sqlVO(sqlVO1)
	value = scrapy_records1[0].get('field',None)
	if value != None :
		scrapy_records1[0]['field'] = float(value)
	frame1=DataFrame(scrapy_records1)
	yaxis=frame1.FIELD[0]
	return yaxis

#请求chen.html页面
def chen(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/chen.html',{'title':"青特钢大数据项目组数据管理"})

#请求test.html页面
def test(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/test")
	return render(request,'data_import/test.html',{'title':"青特钢大数据项目组数据管理"})

#跳转波动率fluctuation.html页面
def fluctuation(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/fluctuation.html')

#analysis_tool.html页面
def analysis_tool(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/analysis_tool.html',{'title':"青特钢大数据项目组数据管理"})

#从数据库动态加载钢种
def getGrape(request):
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="select SPECIFICATION  from pro_bof_his_allfields group by SPECIFICATION order by count(*) DESC";
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	frame=DataFrame(scrapy_records)
	#print(frame['GK_NO'])
	contentVO={
		'title':'测试',
		'state':'success'
	}
	grape=[ele for ele in frame['SPECIFICATION']]
	#print(grape)
	contentVO['result']=grape
	return HttpResponse(json.dumps(contentVO),content_type='application/json')



#更新数据库转炉表结构期望等参数：updatevalue+Calculation_Parameters-----------------------------------------------------------------------------------------------------------------
import cx_Oracle
#定期更新数据库转炉字段统计值
def updatevalue(request):
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="select DATA_ITEM_EN,IF_ANALYSE,IF_FIVENUMBERSUMMARY from PRO_BOF_HIS_ALLSTRUCTURE"#读取字段列表,三个字段分别为字段名，是否用于分析，是否进行五值计算
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	print(len(scrapy_records))
	tns=cx_Oracle.makedsn('202.204.54.75',1521,'orcl')
	db=cx_Oracle.connect('qg_user','123456',tns)
	cur = db.cursor()#创建cursor
	# sql_str="select DATA_ITEM_EN,IF_ANALYSE,IF_FIVENUMBERSUMMARY from PRO_BOF_HIS_ALLSTRUCTURE"#读取字段列表,三个字段分别为字段名，是否用于分析，是否进行五值计算
	# cur.execute(sql_str)
	# rs=cur.fetchall()  #一次返回所有结果集
	for rs in scrapy_records:
		print(rs);
		# print(rs["DATA_ITEM_EN"],rs["IF_ANALYSE"],rs["IF_FIVENUMBERSUMMARY"])
		#符合分析条件则进行极值及期望标准差计算
		if rs["IF_ANALYSE"] != '1':
			continue;
		#计算参数
		dataclean_result=Calculation_Parameters(rs["DATA_ITEM_EN"],rs["IF_FIVENUMBERSUMMARY"]);
		min_value=str(dataclean_result["clean_min"])#最小值
		max_value=str(dataclean_result["clean_max"])#最大值
		average_value=str(dataclean_result['avg_value'])#期望值
		standard_value=str(dataclean_result['std_value'])#标准差

		#更新数据库
		sql_str="UPDATE PRO_BOF_HIS_ALLSTRUCTURE SET MAX_VALUE ="+max_value+", MIN_VALUE="+min_value+", DESIRED_VALUE="+average_value+", STANDARD_DEVIATION="+standard_value+" WHERE DATA_ITEM_EN = \'"+rs["DATA_ITEM_EN"]+"\'";
		print(sql_str)
		try:
			cur.execute(sql_str)
		except:
			print(rs["DATA_ITEM_EN"]+"update failed!")
			pass
		db.commit()

	cur.close()
	# db.commit()
	db.close()
	contentVO={
		'title':'测试',
		'state':'success'
	}
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#计算极值、期望和标准差
from scipy.stats import norm
def Calculation_Parameters(fieldname,IF_FIVENUMBERSUMMARY):
	# print("enter Calculation_Parameters!")
	#对字段AS的特殊情况进行处理
	if fieldname=='AS':
		fieldname='"AS"'
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT HEAT_NO,"+fieldname+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS"
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	#print(fieldname)
	#print(scrapy_records[:5])
	contentVO={
		'title':'测试',
		'state':'success',
	}
	print("data_clean:"+fieldname);
	if fieldname=='"AS"':
		fieldname=fieldname.split('"')[1]

	for i in range(len(scrapy_records)):
		value = scrapy_records[i].get(fieldname,None)
		if value != None :
			scrapy_records[i][fieldname] = float(value)
	frame=DataFrame(scrapy_records) #可能有多列数据
	# frame_formal=frame[['HEAT_NO',fieldname]]
	#print(frame[fieldname])
	#字段NB的所有数据都相同，因此列为特殊情况，不对其进行清洗处理
	df=frame.sort_values(by=fieldname)
	dfr=df[df>0].dropna(how='any')
	#print(dfr[fieldname].dtype)
	if IF_FIVENUMBERSUMMARY=='1':#是否进行五数分析
		print("进行五值分析:",fieldname)
		clean=Wushu(dfr[fieldname])["result"]
	else:
		clean=dfr[fieldname]

	#print("clean",clean)
	#平均值/期望值
	dataclean_result={}
	avg_value=np.mean(clean)
	print("期望值",avg_value)
	#标准差
	std_value=np.std(clean)
	print("标准差",std_value)
	#方差
	var_value=np.var(clean)
	print("方差",var_value)
	#normx,normy=Norm_dist(avg_value,var_value)
	print("min",clean.min())
	print("max",clean.max())

	dataclean_result['clean_min']=clean.min()
	dataclean_result['clean_max']=clean.max()
	dataclean_result['avg_value']=avg_value#期望值
	dataclean_result['std_value']=std_value#标准差

	return dataclean_result