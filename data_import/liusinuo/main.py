'''

2016-10-21

对应 v4_statistics.py 代码

将此大程序拆分成几个小程序

'''

#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
#======================================================================

#========== 1. 所 选 某 钢 种 占 全 部 钢 种 的 比 例 ============

#========== 2. 结 论 输 出 =======================================

#======================================================================
#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

#from sys import argv 
#script, filename = argv 

from . import input_
from . import sql_space
from . import sql_time
from . import sql_trade
from . import sql_customer
from . import sql_customer2
from . import max_min_average
from . import conclusion
from . import save_txt

def main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space):
	#========================【 输 入 】===========================
	module,module_name,module_unit = input_.select_module(module) #模块选择 
	aspect,aspect_name,unite = input_.select_aspect(aspect) #分析内容选择
	dateChoose = input_.select_datechoose(dateChoose) #时间选项选择
	sql_date1,sql_date2 = input_.select_date(sql_date1,sql_date2) #时间选择

	if module == 4:
		sql_cust = input_.select_cust(sql_cust) #客户选择
		if module_unit == "时间":
			tradeNo_list,tradeNoList = input_.select_trade(tradeNo) #钢种选择
		elif module_unit == "钢种":
			pass
		else:
			pass
	else:
		tradeNo_list,tradeNoList = input_.select_trade(tradeNo) #钢种选择
		space,sql_ctry_prov_cty,space_name,space_dict = input_.select_space(module,space) #地点选择


	#========================【 分 析 】============================
	# 【 SQL 语 句 查 询 】 得出一个dict
	# 为结论输出将dictionary统一命名为dictionary
	dictionary = None
	conclusionPrint = None
	if module == 1:  #空间分析	#前两个的 max_min_ave_sum 与 final_conclusion 是一样的
		space_dict,passOrNot,tradeNo_rtn_reason_print = sql_space.space_sql(space_dict,sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect)
		dictionary = space_dict
		# 【 结 论 总 结 】 最大、最小、平均、比例等
		maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason = max_min_average.max_min_ave_sum(dictionary,aspect,module_unit)
		# 【 结 论 输 出 】
		conclusionPrint = conclusion.final_conclusion(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module)

	elif module == 2:  #时间分析
		time_dict,passOrNot,tradeNo_rtn_reason_print = sql_time.time_sql(sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect)
		dictionary = time_dict
		# 【 结 论 总 结 】 最大、最小、平均、比例等
		maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason = max_min_average.max_min_ave_sum(dictionary,aspect,module_unit)
		# 【 结 论 输 出 】
		conclusionPrint = conclusion.final_conclusion(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module)

	elif module == 3:  #钢种分析
		trade_dict,passOrNot,tradeNo_rtn_reason_print,chooseTrade_sum,allTrade_sum = sql_trade.trade_sql(sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect)
		dictionary = trade_dict

		# 【 结 论 总 结 】 最大、最小、平均、比例等   #【 占 全 部 钢 种 比 例 】
		maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason,tradeNo_rate_dict = max_min_average.max_min_ave_sum_trade(dictionary,aspect,module_unit,allTrade_sum)
		# 【 结 论 输 出 】 #与前两个不一样
		conclusionPrint = conclusion.final_conclusion_trade(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,tradeNo_rate_dict,module)

	else:  #客户分析
		if module_unit == "时间":
			#得出每一天的，单一客户时间序列
			cust_dict,passOrNot,tradeNo_rtn_reason_print = sql_customer.cust_sql(sql_date1,sql_date2,tradeNo_list,aspect_name,dateChoose,aspect,sql_cust)
			dictionary = cust_dict
			# 【 结 论 总 结 】 最大、最小、平均、比例等
			maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason = max_min_average.max_min_ave_sum(dictionary,aspect,module_unit)
			# 【 结 论 输 出 】
			conclusionPrint = conclusion.final_conclusion_cust(sql_date1,sql_date2,tradeNoList,sql_cust,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module)
		elif module_unit == "钢种":
			cust_dict,passOrNot,tradeNo_rtn_reason_print = sql_customer2.cust_sql(sql_date1,sql_date2,aspect_name,dateChoose,aspect,sql_cust)
			dictionary = cust_dict
			# 【 结 论 总 结 】 最大、最小、平均、比例等
			maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason = max_min_average.max_min_ave_sum(dictionary,aspect,module_unit)
			# 【 结 论 输 出 】
			conclusionPrint = conclusion.final_conclusion_cust2(sql_date1,sql_date2,sql_cust,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module)
		else:
			pass

	

	if space == 1:
		dictionary2 = {'Afghanistan': 0,'Angola': 0,'Albania': 0,'United Arab Emirates':0,'Argentina': 0,
		'Armenia':0,'French Southern and Antarctic Lands':0,'Australia':0,'Austria':0,
		'Azerbaijan':0,'Burundi':0.0,'Belgium':0,'Benin':0,'Burkina Faso':0.0,'Bangladesh':0,
		'Bulgaria':0,'The Bahamas':0.0,'Bosnia and Herzegovina':0.0,'Belarus':0.0,'Belize':0,
		'Bermuda':0,'Bolivia':0.0,'Brazil':0.0,'Brunei':0,'Bhutan':0.0,'Botswana':0.0,
		'Central African Republic':0.0,'Canada':0.0,'Switzerland':0.0,'Chile':0.0,'China':0.0,'Ivory Coast':0.0,
		'Cameroon':0,'Democratic Republic of the Congo':0.0,'Republic of the Congo':0.0,'Colombia':0.0,
		'Costa Rica':0,	'Cuba':0.0,'Northern Cyprus':0.0,'Cyprus':0.0,'Czech Republic':0.0,
		'Germany':0,'Djibouti':0.0,'Denmark':0.0,'Dominican Republic':0.0,'Algeria':0.0,'Ecuador':0.0,
		'Egypt':0,'Eritrea':0.0,'Spain':0.0,'Estonia':0.0,'Ethiopia':0.0,'Finland':0.0,'Fiji':0.0,
		'Falkland Islands':0,'France':0.0,'Gabon':0.0,'United Kingdom':0.0,'Georgia':0.0,'Ghana':0.0,
		'Guinea':0,'Gambia':0.0,'Guinea Bissau':0,'Equatorial Guinea':0.0,'Greece':0.0,'Greenland':0.0,
		'Guatemala':0.0,'French Guiana':0.0,'Guyana':0.0,'Honduras':0.0,'Croatia':0.0,'Haiti':0.0,
		'Hungary':0.0,'Indonesia':0.0,'India':0.0,'Ireland':0.0,'Iran':0.0,'Iraq':0.0,'Iceland':0,
		'Israel':0.0,'Italy':0.0,'Jamaica':0.0,'Jordan':0.0,'Japan':0.0,'Kazakhstan':0.0,'Kenya':0,
		'Kyrgyzstan':0.0,'Cambodia':0.0,'South Korea':0.0,'Kosovo':0.0,'Kuwait':0.0,'Laos':0,'Lebanon':0,
		'Liberia':0.0,'Libya':0.0,'Sri Lanka':0.0,'Lesotho':0.0,'Lithuania':0.0,'Luxembourg':0,'Latvia':0,
		'Morocco':0.0,'Moldova':0.0,'Madagascar':0.0,'Mexico':0.0,'Macedonia':0.0,'Mali':0,'Myanmar':0,
		'Montenegro':0.0,'Mongolia':0.0,'Mozambique':0.0,'Mauritania':0.0,'Malawi':0.0,'Malaysia':0,
		'Namibia':0.0,'New Caledonia':0.0,'Niger':0.0,'Nigeria':0.0,'Nicaragua':0.0,'Netherlands':0,
		'Norway':0.0,'Nepal':0.0,'New Zealand':0.0,'Oman':0.0,'Pakistan':0.0,'Panama':0,'Peru':0,
		'Philippines':0.0,'Papua New Guinea':0.0,'Poland':0.0,'Puerto Rico':0.0,'North Korea':0,'Portugal':0,
		'Paraguay':0.0,'Qatar':0.0,'Romania':0.0,'Russia':0.0,'Rwanda':0.0,'Western Sahara':0,'Saudi Arabia':0,
		'Sudan':0.0,'South Sudan':0.0,'Senegal':0.0,'Solomon Islands':0.0,'Sierra Leone':0,'El Salvador':0,
		'Somaliland':0.0,'Somalia':0.0,'Republic of Serbia':0.0,'Suriname':0.00,'Slovakia':0,'Slovenia':0,
		'Sweden':0.0,'Swaziland':0.0,'Syria':0.0,'Chad':0.0,'Togo':0.0,'Thailand':0.0,'Tajikistan':0,
		'Turkmenistan':0.0,'East Timor':0.0,'Trinidad and Tobago':0.0,'Tunisia':0.0,'Turkey':0,
		'United Republic of Tanzania':0.0,'Uganda':0.0,'Ukraine':0.0,'Uruguay':0.0,'United States of America':0,
		'Uzbekistan':0.0,'Venezuela':0.0,'Vietnam':0.0,'Vanuatu':0.0,'West Bank':0.0,'Yemen':0.0,'South Africa':0.0,
		'Zambia':0.0,'Zimbabwe':0}
		dictionary2["China"] = dictionary["中国"]
		dictionary2["Malaysia"] = dictionary["马来西亚"]
		dictionary2["South Korea"] = dictionary["韩国"]
		dictionary2["United Kingdom"] = dictionary["英国"]
		dictionary2["United States of America"] = dictionary["美国"]
		dictionary2["Japan"] = dictionary["日本"]
		dictionary2["Thailand"] = dictionary["泰国"]
		dictionary2["Saudi Arabia"] = dictionary["沙特"]
		dictionary2["New Zealand"] = dictionary["新西兰"]
		dictionary2["singpore"] = dictionary["新加坡"]  #这个不在地图中
		dictionary2["Germany"] = dictionary["德国"]
		dictionary2["turkey"] = dictionary["土耳其"]
		dictionary2["Mexico"] = dictionary["墨西哥"]
		dictionary2["India"] = dictionary["印度"]
		dictionary2["Indonesia"] = dictionary["印尼"]
		dictionary2["others"] = dictionary["其他"]  #其他
		return dictionary2,conclusionPrint,module_name,aspect_name,unite,maxValue
	elif space == 3:
		dictionary2 ={ '烟台市':0, '临沂市':0, '潍坊市': 0, '青岛市':0,'菏泽市':0,'济宁市':0,'德州市':0,'滨州市':0,
		'聊城市':0,'东营市':0,'济南市':0,'泰安市':0,'威海市':0,'日照市':0,'淄博市':0,'枣庄市':0,'莱芜市':0}
		dictionary2['烟台市'] = dictionary['烟台']
		dictionary2['临沂市'] = dictionary['临沂']
		dictionary2['潍坊市'] = dictionary['潍坊']
		dictionary2['青岛市'] = dictionary['青岛']
		dictionary2['菏泽市'] = dictionary['菏泽']
		dictionary2['济宁市'] = dictionary['济宁']
		dictionary2['德州市'] = dictionary['德州']
		dictionary2['滨州市'] = dictionary['滨州']
		dictionary2['聊城市'] = dictionary['聊城']
		dictionary2['东营市'] = dictionary['东营']
		dictionary2['济南市'] = dictionary['济南']
		dictionary2['泰安市'] = dictionary['泰安']
		dictionary2['威海市'] = dictionary['威海']
		dictionary2['日照市'] = dictionary['日照']
		dictionary2['淄博市'] = dictionary['淄博']
		dictionary2['枣庄市'] = dictionary['枣庄']
		dictionary2['莱芜市'] = dictionary['莱芜']
		return dictionary2,conclusionPrint,module_name,aspect_name,unite,maxValue
	else:
		return dictionary,conclusionPrint,module_name,aspect_name,unite,maxValue


if __name__ == '__main__':

	dictionary,conclusionPrint,module_name,aspect_name,unite,maxValue = main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space)
	#print (module,tradeNo)


	'''
		#=====================【 结 果 存 储 】==================================
		#将结果存储在txt文本中
		save_txt.write(dictionary,filename,conclusion)

	'''








