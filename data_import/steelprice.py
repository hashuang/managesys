import json

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404

from data_import.steelpriceTools.data_cleaning import get_history_price


media_root = settings.MEDIA_ROOT
data_root = media_root + '/files/data/'

def steelprice(request):
	print(media_root)
	contentVO={
		'title':'price_history请求结果',
		'state':'success'
	}
	return render(request,'data_import/steelprice.html',contentVO)



def price_history(request):
	print(media_root)
	contentVO={
		'title':'price_history请求结果',
		'state':'success'
	}
	path = data_root + 'tegang.csv'
	prices = get_history_price(path)
	print(type(prices.get('price',None)[0]))
	contentVO['timeline'] = prices.get('timeline',None)
	contentVO['price'] = prices.get('price',None)
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

