from pandas import DataFrame
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
#from . import hashuang

#带单炉次因素偏高偏低的不分钢种字段分析
def ch_num2(request):
	print("success_num2")
	heat_no=request.POST.get("heat");
	bookno=request.POST.get("bookno").upper();
	typee=int(request.POST.get("typee"))
	print(heat_no,bookno,typee)
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT HEAT_NO,"+bookno+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS"
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	#print(bookno)
	#print(scrapy_records[:5])
	contentVO={
		'title':'测试',
		'state':'success',
	}
	ana_result,ana_describe=num_describe(scrapy_records,bookno)
	#print("ana_result1",ana_result)
	vvalue=0
	print("vvalue1:",vvalue)
	if typee==1:
		print("typee=1")
		vvalue=float(single_heat(heat_no,bookno))
	print("vvalue2:",vvalue)
	#------判断value值属于哪个区间--------------------
	final=ana_result['scope'][0]
	for ele in ana_result['scope']:
		strr=ele[1:-1].split(',')
		data1=float(strr[0])
		data2=float(strr[1])
		if (vvalue>data1)&(vvalue<=data2):
			final=ele
			break;
	print("final",final)
	#-------------------------------------------------
	ana_result['vvalue_x']=final
	ana_result['vvalue_y']=vvalue
	contentVO['result']=ana_result
	contentVO['describe']=ana_describe
	print("ana_result",ana_result)
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#可自由选择要进行筛选的条件
def multi_analy(request):
	print("multi_analy")
	bookno=request.POST.get("bookno").upper();
	gk_no=request.POST.get("gk_no");
	OPERATESHIFT=request.POST.get("OPERATESHIFT");
	OPERATECREW=request.POST.get("OPERATECREW");
	station=request.POST.get("station");
	if gk_no !='blank':
		sentence_gk_no= " and gk_no='"+gk_no+"'"
	else:
		sentence_gk_no=''
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
	sentence="SELECT HEAT_NO,"+bookno+" FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO>'1500000'"+sentence_gk_no+sentence_OPERATESHIFT+sentence_OPERATECREW+sentence_station
	#print(sentence)
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]=sentence
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	print(scrapy_records[:5])
	contentVO={
		'title':'测试',
		'state':'success',
	}
	ana_result,ana_describe=num_describe(scrapy_records,bookno)
	contentVO['result']=ana_result
	contentVO['describe']=ana_describe
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#计算投入料分布
def cost(request):
	print("success")
	prime_cost=request.POST.get("prime_cost");
	print(prime_cost)
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT HEAT_NO,nvl(MIRON_WGT,0) as MIRON_WGT,nvl(SUM_BO_CSM,0) as SUM_BO_CSM ,nvl(COLDPIGWGT,0) as COLDPIGWGT,nvl(SCRAPWGT_COUNT,0) as SCRAPWGT_COUNT FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no='"+prime_cost+"'";
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	value = scrapy_records[0].get('MIRON_WGT',None)
	if value != None :
		scrapy_records[0]['MIRON_WGT'] = float(value)
	value1 = scrapy_records[0].get('SUM_BO_CSM',None)
	if value1 != None :
		scrapy_records[0]['SUM_BO_CSM'] = float(value1)	
	value2 = scrapy_records[0].get('COLDPIGWGT',None)
	if value2 != None :
		scrapy_records[0]['COLDPIGWGT'] = float(value2)	
	value3 = scrapy_records[0].get('SCRAPWGT_COUNT',None)
	if value3 != None :
		scrapy_records[0]['SCRAPWGT_COUNT'] = float(value3)	
	frame=DataFrame(scrapy_records)
	#heat_no=[ele for ele in frame.HEAT_NO]
	#miron_wgt=[ele for ele in frame['MIRON_WGT']]
	#desx=[ele for ele in describe.index]
	#desy=[ele for ele in describe]
	contentVO={
		'title':'测试',
		'state':'success'
	}
	#ana_result={}
	#ana_result['heat_no']=frame.HEAT_NO[0]
	#ana_result['miron_wgt']=frame.MIRON_WGT[0]
	#contentVO['result']=ana_result
	#print('ana_result',ana_result)
	#xaxis=['MIRON_WGT','SCRAP_96053101','SCRAP_96052200','SCRAP_16010101','SCRAP_16020101','SCRAP_16030101','COLDPIGWGT','SCRAPWGT_COUNT']
	xaxis=['铁水','耗氧量','生铁','废钢总和']
	yaxis=[frame.MIRON_WGT[0],frame.SUM_BO_CSM[0],frame.COLDPIGWGT[0],frame.SCRAPWGT_COUNT[0]]
	ana_result={}
	ana_result['heat_no']=frame.HEAT_NO[0]
	ana_result['xname']=xaxis
	ana_result['yvalue']=yaxis
	ana_result['attribute']='成本投入量'
	contentVO['result']=ana_result
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#计算输出产品分布
def produce(request):
	print("success")
	prime_produce=request.POST.get("prime_produce");
	print(prime_produce)
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="SELECT HEAT_NO,nvl(TOTAL_SLAB_WGT,0) as TOTAL_SLAB_WGT,nvl(LDG_TOTAL_SLAB_WGT,0) as LDG_TOTAL_SLAB_WGT ,nvl(STEEL_SLAG,0) as STEEL_SLAG FROM qg_user.PRO_BOF_HIS_ALLFIELDS where heat_no='"+prime_produce+"'";
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	value = scrapy_records[0].get('TOTAL_SLAB_WGT',None)
	if value != None :
		scrapy_records[0]['TOTAL_SLAB_WGT'] = float(value)
	value1 = scrapy_records[0].get('LDG_TOTAL_SLAB_WGT',None)
	if value1 != None :
		scrapy_records[0]['LDG_TOTAL_SLAB_WGT'] = float(value1)	
	value2 = scrapy_records[0].get('STEEL_SLAG',None)
	if value2 != None :
		scrapy_records[0]['STEEL_SLAG'] = float(value2)	
	frame=DataFrame(scrapy_records)
	contentVO={
		'title':'测试',
		'state':'success'
	}
	xaxis=['钢水','LDG','钢渣']
	yaxis=[frame.TOTAL_SLAB_WGT[0],frame.LDG_TOTAL_SLAB_WGT[0],frame.STEEL_SLAG[0]]
	ana_result={}
	ana_result['heat_no']=frame.HEAT_NO[0]
	ana_result['xname']=xaxis
	ana_result['yvalue']=yaxis
	ana_result['attribute']='输出产品量'
	contentVO['result']=ana_result
	return HttpResponse(json.dumps(contentVO),content_type='application/json')

#计算因素偏高偏低影响
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

#根据时间段查询数据
def time(request):
	print("success")
	time1=request.POST.get("time1");
	time2=request.POST.get("time2");
	fieldname=request.POST.get("field").upper();
	print(time1)
	print(time2)
	sqlVO1={}
	sqlVO1["db_name"]="l2own"
	sqlVO1["sql"]="SELECT HEAT_NO,"+fieldname+",MSG_DATE_PLAN FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE to_char(MSG_DATE_PLAN,'yyyy-mm-dd')>'"+time1+"' and to_char(MSG_DATE_PLAN,'yyyy-mm-dd')<'"+time2+"'";
	#sqlVO1["sql"]="SELECT HEAT_NO,"+fieldname+",MSG_DATE_PLAN FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE to_char(MSG_DATE_PLAN,'yyyy-mm-dd')>'"+time1+"'";
	print(sqlVO1["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO1)
	print(scrapy_records[:5])
	contentVO={
		'title':'测试',
		'state':'success'
	}
	ana_result,ana_describe=num_describe(scrapy_records,fieldname)
	contentVO['result']=ana_result
	contentVO['describe']=ana_describe
	#if(time1)<(time2):
	#	contentVO['compare']='xiaoyu'
	#else:
	#	contentVO['compare']='dayu'
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


#请求chen.html页面
def chen(request):
	#print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/chen.html',{'title':"青特钢大数据项目组数据管理"})

#跳转波动率fluctuation.html页面
def fluctuation(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	return render(request,'data_import/fluctuation.html')

#从数据库动态加载钢种
def getGrape(request):
	sqlVO={}
	sqlVO["db_name"]="l2own"
	sqlVO["sql"]="select distinct gk_no from qg_user.PRO_BOF_HIS_ALLFIELDS order by gk_no";
	print(sqlVO["sql"])
	scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	frame=DataFrame(scrapy_records)
	#print(frame['GK_NO'])
	contentVO={
		'title':'测试',
		'state':'success'
	}
	grape=[ele for ele in frame['GK_NO']]
	#print(grape)
	contentVO['result']=grape
	return HttpResponse(json.dumps(contentVO),content_type='application/json')



def Wushu(x):
    L=np.percentile(x,25)-1.5*(np.percentile(x,75)-np.percentile(x,25))
    U=np.percentile(x,75)+1.5*(np.percentile(x,75)-np.percentile(x,25))
    return x[(x<U)&(x>L)]	
def num_describe(scrapy_records,bookno):
	print("helloo");
	if bookno=='"AS"':
		bookno=bookno.split('"')[1]
	#value=bookno.split('"')
	#for i in range(len(value)):
		#value=value[i]
		#if value!='"':
			#print(value)
			#bookno=value
	#print(bookno)
	for i in range(len(scrapy_records)):
		value = scrapy_records[i].get(bookno,None)
		if value != None :
			scrapy_records[i][bookno] = float(value)
	frame=DataFrame(scrapy_records)	
	print(frame[bookno])
	df=frame.sort_values(by=bookno)
	dfr=df[df>0].dropna(how='any')
	#print(dfr[bookno].dtype)
	clean=Wushu(dfr[bookno])
	#标准差
	std_value=np.std(clean)
	print("标准差",std_value)
	if clean is not None:
		bc=(clean.max()-clean.min())/10
		bcq=math.ceil(bc*1000)/1000
		try:
			section=pd.cut(clean,math.ceil((clean.max()-clean.min())/bcq+1))
			end=pd.value_counts(section,sort=False)/clean.count()
			describe=clean.describe()
		except ValueError as e:
		 	print(e)
	numx=[ele for ele in end.index]
	numy=[ele for ele in end]
	desx=[ele for ele in describe.index]
	desy=[ele for ele in describe]
	#保留两位小数并以%形式展示
	numy1=["%.2f%%"%(n*100) for n in numy]
	#保留四位小数
	numy2=["%.4f"%(n) for n in numy]
	print("numx:",numx)
	#print("numy:",numy)
	#print("numy1:",numy1)
	print("numy2:",numy2)
	#contentVO={
		#'title':'测试',
		#'state':'success'
	#}
	ana_result={}
	ana_result['scope']=numx
	ana_result['num']=numy2
	ana_result['std_value']=std_value
	ana_result['bookno']=bookno
	#contentVO['result']=ana_result
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy
	#contentVO['describe']=ana_describe
	return ana_result,ana_describe