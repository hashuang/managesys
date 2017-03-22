# -*- coding: utf-8 -*
import json
import logging

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404

from data_import.steelpriceTools.data_cleaning import get_history_price,create_single_model
from data_import.steelpriceTools.ExtremeLM import elm_
from data_import.steelpriceTools.pre_config import steel_type,predict_method,time_scale

'''
预测相关方法在steelpriceTools文件夹中
'''
logger = logging.getLogger('django')

media_root = settings.MEDIA_ROOT
data_root = media_root + '/files/data/'

def steelprice(request):
	if not request.user.is_authenticated():	
		return HttpResponseRedirect("/login")
	logger.debug(media_root)
	'''
	加载钢材种类，及可选的预测方法
	'''
	logger.debug(steel_type)
	logger.debug(predict_method)
	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	contentVO["steel_type"] = steel_type
	contentVO["predict_method"] = predict_method
	contentVO['time_scale'] = time_scale
	return render(request,'data_import/steelprice.html',contentVO)



def price_history(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		history_begin =	request.POST.get('history_begin', '')
		history_end =	request.POST.get('history_end', '')
	path = data_root + 'tegang.csv'
	prices = get_history_price(path,history_begin,history_end)

	logger.debug(type(prices.get('price',None)[0]))

	contentVO={
		'title':'钢材历史价格',
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
		timeScale =	request.POST.get('timeScale', '')
		typestr =	request.POST.get('typestr', '')
		if typestr != "":
			types = typestr.split(',')
			logger.debug(types)
	'''
	根据参数选择模型
	结果返回预测数据时间跨度，预测值，真实值，score值
	对应不同的模型，每个模型存放在一张字典表中
	外层是由模型名为key的字典表result={"ELM":{"timeline":xxx,"predict_value":xxxx,\
	"true_value":xxxx,"score":xxxx},"SVM":{},"LR":{}}
	'''
	path = data_root + 'tegang.csv'
	PRE_DAYS = [5]
	models_data = create_single_model(path,PRE_DAYS)
	logger.debug(len(models_data))
	models_result = {}
	for i in range(len(types)):
		if types[i] == "elm":
			logger.debug(types[i])
			result = elm_(models_data[0],0.4)
			models_result["elm"] = result
		elif types[i] == "svm":
			logger.debug(types[i])
			result = elm_(models_data[0],0.2)
			models_result["svm"] = result
		elif types[i] == "linear_regression":
			logger.debug(types[i])
			result = elm_(models_data[0],0.3)
			models_result["linear_regression"] = result
		elif types[i] == "BP":
			logger.debug(types[i])
			result = elm_(models_data[0],0.1)
			models_result["BP"] = result
		elif types[i] == "random_forest":
			logger.debug(types[i])
			result = elm_(models_data[0],0.15)
			models_result["random_forest"] = result
	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	contentVO["result"] = models_result
	return HttpResponse(json.dumps(contentVO), content_type='application/json')