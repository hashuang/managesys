# -*- coding: utf-8 -*
import json

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404

from data_import.ironstonepriceTools.data_cleaning import get_history_price
from data_import.ironstonepriceTools.predict_day import predict_day
from data_import.ironstonepriceTools.predict_yue import predict_yue
from data_import.ironstonepriceTools.pre_config import iron_type,predict_method,time_scale,yinsu_type

'''
预测相关方法在ironstonepriceTools文件夹中
'''

media_root = settings.MEDIA_ROOT
data_root = media_root + '/files/data/'

def ironstoneprice(request):
	if not request.user.is_authenticated():	
		return HttpResponseRedirect("/login")
	print(media_root)
	'''
	加载铁矿石种类，及可选的预测方法
	'''
	print(iron_type)
	print(predict_method)
	contentVO={
		'title':'铁矿石价格预测',
		'state':'success'
	}
	contentVO["yinsu_type"] = yinsu_type
	contentVO["iron_type"] = iron_type
	contentVO["predict_method"] = predict_method
	contentVO['time_scale'] = time_scale
	return render(request,'data_import/ironstoneprice.html',contentVO)



def price_history(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		history_begin =	request.POST.get('history_begin', '')
		history_end =	request.POST.get('history_end', '')
		yinsu_type =	request.POST.get('yinsu_type', '')
	path = data_root + 'tkszs_yinsu.csv'
	# path = data_root + 'tegang.csv'
	prices = get_history_price(path,history_begin,history_end,yinsu_type)
	# prices['timeline'] = []
	# prices['price'] = []
	# print(type(prices.get('price',None)[0]))

	contentVO={
		'title':'铁矿石历史价格',
		'state':'success'
	}
	contentVO['timeline'] = prices.get('timeline',None)
	contentVO['price'] = prices.get('price',None)
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def price_predict(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		'''
		获取对应参数
		'''
		steelType =	request.POST.get('steelType', '')
		# print(steelType)
		timeScale =	request.POST.get('timeScale', '')
		typestr =	request.POST.get('typestr', '')
		if typestr != "":
			types = typestr.split(',')
			print(types)
	if steelType=='tkszs':
		print('this is tkszs')
	'''
	根据参数选择模型
	结果返回预测数据时间跨度，预测值，真实值，score值
	对应不同的模型，每个模型存放在一张字典表中
	外层是由模型名为key的字典表result={"ELM":{"timeline":xxx,"predict_value":xxxx,\
	"true_value":xxxx,"score":xxxx},"SVM":{},"LR":{}}
	'''
	# path = data_root + 'tegang.csv'
	path_iron = data_root + 'tkszs_yinsu.csv'
	path_iron_yue = data_root + 'qdg_time.csv'
	# PRE_DAYS = [5]
	# models_data = create_single_model(path,PRE_DAYS)
	# print(len(models_data))
	models_result = {}
	if timeScale == "day":	
		for i in range(len(types)):
			# print(types[i])
			if types[i] == "elm":
				print(types[i])
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result
			if types[i] == "logistic_regression":
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result 
			if types[i] == "svm":
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result 
			if types[i] == "random_forest":
				result = predict_day(path_iron,types[i])
				models_result["zhi"] = result 
	if timeScale == "month":	
		for i in range(len(types)):
			# print(types[i])
			if types[i] == "elm":
				print(types[i])
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result
			if types[i] == "logistic_regression":
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result 
			if types[i] == "svm":
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result 
			if types[i] == "random_forest":
				result = predict_yue(path_iron_yue,types[i])
				models_result["zhi"] = result 
	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	contentVO["result"] = models_result
	return HttpResponse(json.dumps(contentVO), content_type='application/json')