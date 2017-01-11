from time import time
import csv
from sklearn.cluster import k_means
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from sklearn import preprocessing

from elm import ELMClassifier, ELMRegressor, GenELMClassifier, GenELMRegressor
from random_layer import RandomLayer, MLPRandomLayer, RBFRandomLayer, GRBFRandomLayer
from math import sqrt

def draw(y_test_true,y_predict_true,y_predict):
	plt.figure()
	plt.plot(np.arange(len(y_predict)),y_test_true,'go-',label='TV')
	plt.plot(np.arange(len(y_predict)),y_predict_true,'ro-',label='PV')
	plt.title('score: %f'%error)
	plt.legend()
	plt.show()


def predict_mes(y_test,y_predict):
	row_num = y_predict.shape[0]
	
	y_test_np = np.array(y_test)
	y_test_true = y_test_np.copy()
	y_predict_true = y_predict.copy()
	error_true = y_predict.copy()
	error_rate = y_predict.copy()
	
	for xi in range(row_num):
	    y_predict_true[xi] = y_predict[xi] * origal_std + origal_mean
	    y_test_true[xi] = y_test_np[xi] * origal_std + origal_mean       
	    error_true[xi] = y_predict_true[xi] -  y_test_true[xi]
	    error_rate[xi] = math.fabs(error_true[xi]) / y_test_true[xi]
	
	draw(y_test_true,y_predict_true,y_predict)

	message= {}
	message['score'] = score
	message['error'] = error_true
	message['rate'] = error_rate

	return message
	

def elm_(model_data,exnum):

	cols_all = list(model_data.columns)
	col_len = len(cols_all)
	out = cols_all[col_len-1]
	feature = cols_all[2:col_len-1]

	X = model_data[feature]
	Y = model_data[out]
	Y_array = np.array(Y)
	data_scale_num = len(model_data.index)
	extension_num = data_scale_num - exnum
	'''
	数据处理有没有更好的方式,暂时使用标准化
	'''
	origal_mean = Y_array.mean(axis=0)#很奇怪的在这里axis=0求列平均，1求行平均
	origal_std = Y_array.std(axis=0)
    print(model_data[cols_all[2:]])
	data_scale = preprocessing.scale(np.array(model_data[cols_all[2:]]))
	# print(type(data_scale))
	data_scale_df = pd.DataFrame(data_scale,columns=cols_all[2:])
	# print(data_scale_df)

	X_scale = data_scale_df[feature][:extension_num]
	Y_scale = data_scale_df[out][:extension_num]

	X_extension = data_scale_df[feature][extension_num:data_scale_num]
	Y_extension = data_scale_df[out][extension_num:data_scale_num]

	'''
	暂时还是随机划分训练集和测试集
	'''
	X_train, X_test, y_train, y_test = train_test_split(X_scale,Y_scale,test_size=0.2,random_state=1)

	elmr = ELMRegressor(activation_func='inv_tribas', random_state=0)
	elm_model = elmr.fit(X_train, y_train)

	y_predict = elmr.predict(X_test)

	score=elmr.score( X_test, y_test)
	print(score)

	message= {}
	test_mes = predict_mes(y_test,y_predict)
	#extention_mes = predict_mes(X_extension,Y_extension)
	message['test_mes'] = test_mes
	#message['extention_mes'] = extention_mes
	
	return elm_model