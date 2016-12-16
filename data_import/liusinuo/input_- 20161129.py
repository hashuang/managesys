'''

2016-10-21

对应 space.py 代码

控制输入

'''

from datetime import datetime
#=====================【 分 析 模 块 选 项 】==================================
def select_module():
	module = 0
	while module!=1 and module!=2 and module!=3 and module!=4:
		module = int(input('\n【模块】：\n\t1.空间分析 \n\t2.时间分析 \n\t3.钢种分析 \n\t4.客户分析\n >>> '))

		if module == 1:
			module_name = "空间分析"
			module_unit = "地区"
			break
		if module == 2:
			module_name = "时间分析"
			module_unit = "时间"
			break
		if module == 3:
			module_name = "钢种分析"
			module_unit = "钢种"
			break
		if module == 4:
			module_name = "客户分析"
			module_unit = select_cust_unit(module)
			#module_unit = "客户"			
			#module_unit1 = "时间"
			#module_unit2 = "客户"
			break
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
def select_aspect():
	aspect = 0
	while aspect!=1 and aspect!=2 and aspect!=3 and aspect!=4:
		aspect = int(input('\n【分析内容】：\n\t1.总销量 \n\t2.总销售额 \n\t3.退货率 \n\t4.主要质量问题\n >>> '))

		if aspect == 1:
			aspect_name = "总销量"
			unite = "吨"
			break
		if aspect == 2:
			aspect_name = "总销售额"
			unite = "元"
			break
		if aspect == 3:
			aspect_name = "退货率"
			unite = "%"
			break
		if aspect == 4:
			aspect_name = "主要质量问题"
			unite = "个"
			break
		else:
			print ('ERROR 时间选项 非法输入！')
	return aspect,aspect_name,unite

#=====================【 时 间 选 项 】==================================
def select_datechoose():
	dateChoose = 0
	while dateChoose!=1 and dateChoose!=2 and dateChoose!=3 and dateChoose!=4 and dateChoose!=5 and dateChoose!=6 and dateChoose!=7 and dateChoose!=8:
		dateChoose = int(input('\n【时间选取依据】：\n\t1.订单时间\n\t2.发货时间\n\t3.派车履运时间（出货销账日期）\n\t4.派车履运时间（结算日期）\n\t5.装车通知时间\n\t6.订单存货档建立时间\n\t7.质保书时间\n\t8.外库接收时间\n >>> '))
	return dateChoose

#=====================【 时 间 选 项 】==================================
def select_date():	
	date = 0
	now = datetime.now()
	while date!=1 and date!=2 and date!=3 and date!=4:
		date = int(input('\n【时间范围】：\n\t1.近一月\n\t2.近三月\n\t3.近一年\n\t4.自定义\n >>> '))

		if date == 1:
			if int(now.strftime('%m')) == 1:#起始时间
				sql_date1 = str(int(now.strftime('20%y')) - 1) * 10000 + 12 * 100 + int(now.strftime('%d'))
			else:#起始时间
				sql_date1 = str(int(now.strftime('20%y%m%d')) - 100) #起始时间 
			sql_date2 = str(int(now.strftime('20%y%m%d'))) #终止时间
		elif date == 2:
			if int(now.strftime('%m')) == 1:#起始时间
				sql_date1 = str((int(now.strftime('20%y')) - 1) * 10000 + 10 * 100 + int(now.strftime('%d')))
			if int(now.strftime('%m')) == 2:#起始时间
				sql_date1 = str((int(now.strftime('20%y')) - 1) * 10000 + 11 * 100 + int(now.strftime('%d')))
			if int(now.strftime('%m')) == 3:#起始时间
				sql_date1 = str((int(now.strftime('20%y')) - 1) * 10000 + 12 * 100 + int(now.strftime('%d')))
			else:#起始时间
				sql_date1 = str(int(now.strftime('20%y%m%d')) - 300)
			sql_date2 = sre(int(now.strftime('20%y%m%d'))) #终止时间
		elif date == 3:
			sql_date1 = str(int(now.strftime('20%y%m%d')) - 10000) #起始时间 
			sql_date2 = str(int(now.strftime('20%y%m%d'))) #终止时间
		elif date == 4:
			sql_date1 = input('请输入起始时间：\n\t形如20160101\n >>> ') #起始时间 
			sql_date2 = input('请输入中止时间：\n\t形如20160101\n >>> ') #中止时间
		else:
			print ('ERROR 时间选项 非法输入！')
		#print ( sql_date1,sql_date2)
	return sql_date1,sql_date2

#=====================【 钢 种 选 项 】==================================
def select_trade():	
	tradeNo = input('\n【钢种选择】：\n\t以逗号隔开，形如 C86D2,80 \n >>> ')

	#if tradeNo == 'ALL':
	#	allTrade = 1
	#	tradeNo_list = ['All trade']
	#else:
	allTrade = 0
	tradeNo_list = tradeNo.split(",") #英文逗号！
	print (tradeNo_list)
	tradeNoList = ""
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
def select_space(module):	
	space = 0
	while space!=1 and space!=2 and space!=3:
		if module == 1:
			space = int(input('\n【空间范围】：\n\t1.世界级：展示世界所有国家 \n\t2.国家级：展示国家所有省 \n\t3.省级：展示省内所有市\n >>> '))
		else:
			space = int(input('\n【空间范围】：\n\t1.某国家 \n\t2.某省 \n\t3.某城市\n >>> '))

		space_dict = {}
		space_name = ""
		if space == 1:
			sql_ctry_prov_cty = "country"
			if module == 1:
				space_name = '世界'
				space_dict = {'"中东"':0,'"中国"':0,'"马来西亚"':0,'"韩国"':0,'"英国"':0,'"美国"':0,'"日本"':0,'"泰国"':0,
				'"沙特"':0,'"新西兰"':0,'"新加坡"':0,'"德国"':0,'"土耳其"':0,'"墨西哥"':0,'"印度"':0,'"印尼"':0,'"其他"':0}
			else:
				space_name = '"' + input("\n请输入国家名\n >>>") + '"'
		elif space == 2:
			sql_ctry_prov_cty = "province"
			if module == 1:
				space_name = '中国'
				space_dict = {'"河北"':0,'"山东"':0,'"辽宁"':0,'"黑龙江"':0,
				'"吉林"':0,'"甘肃"':0,'"青海"':0,'"河南"':0,'"江苏"':0,'"湖北"':0,
				'"湖南"':0,'"江西"':0,'"浙江"':0,'"广东"':0,'"云南"':0,'"福建"':0,
				'"台湾"':0,'"海南"':0,'"山西"':0,'"四川"':0,'"陕西"':0,'"贵州"':0,
				'"安徽"':0,'"重庆"':0,'"北京"':0,'"上海"':0,'"天津"':0,'"广西"':0,
				'"内蒙古"':0,'"西藏"':0,'"新疆"':0,'"宁夏"':0,'"澳门"':0,'"香港"':0}
			else:
				space_name = '"' + input("\n请输入省名\n >>>") + '"'
		elif space == 3:
			sql_ctry_prov_cty = "city"
			if module == 1:
				space_name =input('请输入省名：\n\t') #地点
				if space_name == "山东":
					space_dict = {'"济南"':0,'"青岛"':0,'"淄博"':0,'"枣庄"':0,'"东营"':0,
					'"烟台"':0,'"潍坊"':0,'"济宁"':0,'"泰安"':0,'"威海"':0,'"日照"':0,
					'"滨州"':0,'"德州"':0,'"聊城"':0,'"临沂"':0,'"菏泽"':0,'"莱芜"':0}
					
				elif space_name == "江苏": 
					pass
					#space_dict = {'""':0,'""':0,'""':0,'""':0,'""':0,0..
					#'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,xa
					#'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'""':0,'"2."':0,'""':0}
				else:
					pass
			else:
				space_name = '"' + input("\n请输入城市名\n >>>") + '"'

		else:
			print("ERROR 地区选项 非法输入！")
	return space,sql_ctry_prov_cty,space_name,space_dict

#=====================【 客 户 选 项 】==================================
def select_cust():	
	sql_cust = input('\n【客户选择】：\n\t请输入客户编号 \n >>> ')
	return sql_cust
