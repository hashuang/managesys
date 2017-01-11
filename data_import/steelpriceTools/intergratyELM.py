from data_cleaning import create_models

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
    elmr.fit(X_train, y_train)

    y_predict = elmr.predict(X_test)

    score=elmr.score( X_test, y_test)
    print(score)

    message= {}
    test_mes = predict_mes(y_test,y_predict)
#     extention_mes = predict_mes(X_extension,Y_extension)
    message['test_mes'] = test_mes
#     message['extention_mes'] = extention_mes

    return elmr

def true_value(origal_mean,origal_std,y_predict):
	row_num = y_predict.shape[0]
	y_predict_true = y_predict.copy()
	for xi in range(row_num):
	    y_predict_true[xi] = y_predict[xi] * origal_std + origal_mean
	return y_predict_true

def stard_mean(model_data,rate):
    cols_all = list(model_data.columns)
    col_len = len(cols_all)
    out = cols_all[col_len-1]
    feature = cols_all[:col_len-1]

    X = model_data[feature]
    Y = model_data[out]
    Y_array = np.array(Y)

    data_scale_num = len(model_data.index)
    exnum = math.ceil(data_scale_num*rate)
    extension_num = data_scale_num - exnum
    '''
    数据处理有没有更好的方式,暂时使用标准化
    '''
    origal_mean = Y_array.mean(axis=0)#很奇怪的在这里axis=0求列平均，1求行平均
    origal_std = Y_array.std(axis=0)

    data_scale = preprocessing.scale(np.array(model_data))
    # print(type(data_scale))
    data_scale_df = pd.DataFrame(data_scale,columns=cols_all)
    # print(data_scale_df)

    X_scale = data_scale_df[feature][:extension_num]
    Y_scale = data_scale_df[out][:extension_num]

    X_extension = data_scale_df[feature][extension_num:data_scale_num]
    Y_extension = data_scale_df[out][extension_num:data_scale_num]

    rs={}
    rs['allx']= data_scale_df[feature].copy(deep=True)
    rs['mean']= origal_mean
    rs['std']= origal_std
    #     rs['X_extension']= X_extension
    #     rs['Y_extension']= Y_extension
    #     rs['X_scale']= X_scale
    #     rs['Y_scale']= Y_scale
    return rs

if __name__ == '__main__':

	PRE_DAYS = [10]#,4,5,10,15,20,30,40,60

	pre_model_data, models, dataset_scale = create_models(PRE_DAYS)

	exnum = math.ceil(dataset_scale*0.4)

	ELMmodels = []
	for i in range(len(models)):
		print(PRE_DAYS[i])
		ELMmodels.append(elm_(models[i],exnum))

	'''
	集成二次训练所需数据，数量dataset_scale*0.4，并根据天数截取每个每个模型的数据集
	'''
	
	pre_model_data_train = pre_model_data[dataset_scale-exnum:dataset_scale]
	merge_cols = list(pre_model_data_train.columns)
	begin =2
	datas = []
	for day in PRE_DAYS:
		end = begin + day + 1
		data = pre_model_data_train[merge_cols[begin: begin + day + 1]]
		begin = end
		datas.append(data)

	second_model = pd.DataFrame()
	second_model[merge_cols[:2]] = pre_model_data_train[merge_cols[:2]] 

    #拼接预测值
	for i,day in enumerate(PRE_DAYS):
	    cols_data = [x for x in datas[i].columns]
	    rs = stard_mean(datas[i],0.25) 
	    y_predict = ELMmodels[i].predict(rs.get('allx'))
	    '''
    	以day为列记录模型预测的数据
    	'''
	    second_model[str(day)] = true_value(rs.get('std'),rs.get('mean'),y_predict)