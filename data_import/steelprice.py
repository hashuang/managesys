# -*- coding: utf-8 -*
import json

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404

from data_import.steelpriceTools.data_cleaning import get_history_price


media_root = settings.MEDIA_ROOT
data_root = media_root + '/files/data/'

def steelprice(request):
	if not request.user.is_authenticated():	
		return HttpResponseRedirect("/login")
	print(media_root)
	contentVO={
		'title':'钢材价格预测',
		'state':'success'
	}
	return render(request,'data_import/steelprice.html',contentVO)



def price_history(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	if request.method == 'POST':
		history_begin =	request.POST.get('history_begin', '')
		history_end =	request.POST.get('history_end', '')
	path = data_root + 'tegang.csv'
	prices = get_history_price(path,history_begin,history_end)

	print(type(prices.get('price',None)[0]))

	contentVO={
		'title':'钢材历史价格',
		'state':'success'
	}
	contentVO['timeline'] = prices.get('timeline',None)
	contentVO['price'] = prices.get('price',None)
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

