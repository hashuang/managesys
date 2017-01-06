'''

2016-10-21

对应 space.py 代码

控制输入

'''

from datetime import datetime
#=====================【 分 析 模 块 选 项 】==================================
def select_module(module):
	
	if module == 1:
		module_name = "空间分析"
		module_unit = "地区"
	elif module == 2:
		module_name = "时间分析"
		module_unit = "时间"
	elif module == 3:
		module_name = "钢种分析"
		module_unit = "钢种"
	elif module == 4:
		module_name = "客户分析"
		module_unit = select_cust_unit(module)		
	else:
		print ('ERROR 模块选项 非法输入！')

	return module,module_name,module_unit

def select_cust_unit(module):
	if module == 4:
		module_unit_key = 0
		while module_unit_key != 1 and module_unit_key != 2:
			module_unit_key = int(input("\n\t【客户分析具体选择】\n\t\t1.某一客户按时间分析\n\t\t2.某一客户按钢种分析\n\t >>>"))
			if module_unit_key == 1:
				module_unit = "时间"
			elif module_unit_key == 2:
				module_unit = "钢种"
			else:
				print ("ERROE  客户分析具体选项 非法输入！")
	return module_unit

#=====================【 分 析 内 容 选 项 】==================================
def select_aspect(aspect):
	
	if aspect == 1:
		aspect_name = "总销量"
		unite = "吨"
	elif aspect == 2:
		aspect_name = "总销售额"
		unite = "元"
	elif aspect == 3:
		aspect_name = "退货率"
	elif aspect == 4:
		aspect_name = "主要质量问题"
		unite = "个"
	else:
		print ('ERROR 分析内容选项 非法输入！')
		#print (aspect)
	return aspect,aspect_name,unite

#=====================【 时 间 选 项 】==================================
def select_datechoose(dateChoose):
	return dateChoose

#=====================【 时 间 选 项 】==================================
def select_date(sql_date1,sql_date2):	
	return sql_date1,sql_date2


#=====================【 钢 种 选 项 】==================================
def select_trade(tradeNo):	
	#allTrade = 0
	tradeNo_list = tradeNo.split(",") #英文逗号！
	print (tradeNo)
	print (tradeNo_list)
	tradeNoList = ""
	#tradeNo_list = tradeNo
	pause = "、"
	i = 0
	for tradeNo in tradeNo_list:
		if i == 0:
			tradeNoList = tradeNo
			i = i + 1
		else:
			tradeNoList = tradeNoList + pause +tradeNo
	return tradeNo_list,tradeNoList

#=====================【 地 点 选 项 】==================================
def select_space(module,space):	
	# space = 0
	# while space!=1 and space!=2 and space!=3:
		
	space_dict = {}
	space_name = ""
	if space == 1:
		sql_ctry_prov_cty = "country"
		if module == 1:
			space_name = '世界'
			space_dict = {"中东":0,"中国":0,"马来西亚":0,"韩国":0,"英国":0,"美国":0,"日本":0,"泰国":0,
			"沙特":0,"新西兰":0,"新加坡":0,"德国":0,"土耳其":0,"墨西哥":0,"印度":0,"印尼":0,"其他":0}
		else:
			space_name = '"' + input("\n请输入国家名\n >>>") + '"'
	elif space == 2:
		sql_ctry_prov_cty = "province"
		if module == 1:
			space_name = '中国'
			space_dict = {"河北":0,"山东":0,"辽宁":0,"黑龙江":0,
			"吉林":0,"甘肃":0,"青海":0,"河南":0,"江苏":0,"湖北":0,
			"湖南":0,"江西":0,"浙江":0,"广东":0,"云南":0,"福建":0,
			"台湾":0,"海南":0,"山西":0,"四川":0,"陕西":0,"贵州":0,
			"安徽":0,"重庆":0,"北京":0,"上海":0,"天津":0,"广西":0,
			"内蒙古":0,"西藏":0,"新疆":0,"宁夏":0,"澳门":0,"香港":0}
		else:
			space_name = '"' + input("\n请输入省名\n >>>") + '"'
	elif space == 3:
		sql_ctry_prov_cty = "city"
		if module == 1:
			space_name = '山东' #地点
			space_dict = {"济南":0,"青岛":0,"淄博":0,"枣庄":0,"东营":0,
			"烟台":0,"潍坊":0,"济宁":0,"泰安":0,"威海":0,"日照":0,
			"滨州":0,"德州":0,"聊城":0,"临沂":0,"菏泽":0,"莱芜":0}
		else:
			space_name = input("\n请输入城市名\n >>>")
	else:
		print("ERROR 地区选项 非法输入！")
	'''		
	elif space == 4:
	 	sql_ctry_prov_cty = "city"
	 	space_name == "江苏": 
	 	#space_dict = {'""':0,'""':0,'""':0,'""':0,'""':0,0..
	 	#'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,xa
	 	#'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'"2."':0,'""':0}
	'''	
	'''
	elif space == 3:
		sql_ctry_prov_cty = "city"
		if module == 1:
			space_name =input('请输入省名：\n\t') #地点
			if space_name == "山东":
				space_dict = {"济南":0,"青岛":0,"淄博":0,"枣庄":0,"东营":0,
				"烟台":0,"潍坊":0,"济宁":0,"泰安":0,"威海":0,"日照":0,
				"滨州":0,"德州":0,"聊城":0,"临沂":0,"菏泽":0,"莱芜":0}
				
			elif space_name == "江苏": 
				pass
				#space_dict = {'""':0,'""':0,'""':0,'""':0,'""':0,0..
				#'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,xa
				#'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'"2."':0,'""':0}
			else:
				pass
		else:
			#space_name = '"' + input("\n请输入城市名\n >>>") + '"'
			space_name = input("\n请输入城市名\n >>>")
	'''
	return space,sql_ctry_prov_cty,space_name,space_dict

#=====================【 客 户 选 项 】==================================
def select_cust(sql_cust):	
	
	return sql_cust
