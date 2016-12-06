from pandas import DataFrame
from pandas import DataFrame
import pandas as pd
import numpy as np
import math
from . import views
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
import os

def Wushu(x):
    L=np.percentile(x,25)-1.5*(np.percentile(x,75)-np.percentile(x,25))
    U=np.percentile(x,75)+1.5*(np.percentile(x,75)-np.percentile(x,25))
    return x[(x<U)&(x>L)]	
def num_describe(scrapy_records,bookno):
	print("hello");
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
	df=frame.sort_values(by=bookno)
	dfr=df[df>0].dropna(how='any')
	#print(dfr[bookno].dtype)
	clean=Wushu(dfr[bookno])
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
	numy1=["%.2f%%"%(n*100) for n in numy]
	#contentVO={
		#'title':'测试',
		#'state':'success'
	#}
	ana_result={}
	ana_result['scope']=numx
	ana_result['num']=numy
	#contentVO['result']=ana_result
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy
	#contentVO['describe']=ana_describe
	return ana_result,ana_describe