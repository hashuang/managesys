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

def main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space,space_detail):
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
		space,sql_ctry_prov_cty,space_name,space_dict = input_.select_space(module,space,space_detail) #地点选择


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
		
		if space == 1:
			if aspect == 1 or aspect == 2:
				dictionary2 = {'Afghanistan': 0,'Angola': 0,'Albania': 0,'United Arab Emirates':0,'Argentina': 0,
				'Armenia':0,'French Southern and Antarctic Lands':0,'Australia':0,'Austria':0,
				'Azerbaijan':0,'Burundi':0,'Belgium':0,'Benin':0,'Burkina Faso':0,'Bangladesh':0,
				'Bulgaria':0,'The Bahamas':0,'Bosnia and Herzegovina':0,'Belarus':0,'Belize':0,
				'Bermuda':0,'Bolivia':0,'Brazil':0,'Brunei':0,'Bhutan':0,'Botswana':0,
				'Central African Republic':0,'Canada':0,'Switzerland':0,'Chile':0,'China':0,'Ivory Coast':0,
				'Cameroon':0,'Democratic Republic of the Congo':0,'Republic of the Congo':0,'Colombia':0,
				'Costa Rica':0, 'Cuba':0,'Northern Cyprus':0,'Cyprus':0,'Czech Republic':0,
				'Germany':0,'Djibouti':0,'Denmark':0,'Dominican Republic':0,'Algeria':0,'Ecuador':0,
				'Egypt':0,'Eritrea':0,'Spain':0,'Estonia':0,'Ethiopia':0,'Finland':0,'Fiji':0,
				'Falkland Islands':0,'France':0,'Gabon':0,'United Kingdom':0,'Georgia':0,'Ghana':0,
				'Guinea':0,'Gambia':0,'Guinea Bissau':0,'Equatorial Guinea':0,'Greece':0,'Greenland':0,
				'Guatemala':0,'French Guiana':0,'Guyana':0,'Honduras':0,'Croatia':0,'Haiti':0,
				'Hungary':0,'Indonesia':0,'India':0,'Ireland':0,'Iran':0,'Iraq':0,'Iceland':0,
				'Israel':0,'Italy':0,'Jamaica':0,'Jordan':0,'Japan':0,'Kazakhstan':0,'Kenya':0,
				'Kyrgyzstan':0,'Cambodia':0,'South Korea':0,'Kosovo':0,'Kuwait':0,'Laos':0,'Lebanon':0,
				'Liberia':0,'Libya':0,'Sri Lanka':0,'Lesotho':0,'Lithuania':0,'Luxembourg':0,'Latvia':0,
				'Morocco':0,'Moldova':0,'Madagascar':0,'Mexico':0,'Macedonia':0,'Mali':0,'Myanmar':0,
				'Montenegro':0,'Mongolia':0,'Mozambique':0,'Mauritania':0,'Malawi':0,'Malaysia':0,
				'Namibia':0,'New Caledonia':0,'Niger':0,'Nigeria':0,'Nicaragua':0,'Netherlands':0,
				'Norway':0,'Nepal':0,'New Zealand':0,'Oman':0,'Pakistan':0,'Panama':0,'Peru':0,
				'Philippines':0,'Papua New Guinea':0,'Poland':0,'Puerto Rico':0,'North Korea':0,'Portugal':0,
				'Paraguay':0,'Qatar':0,'Romania':0,'Russia':0,'Rwanda':0,'Western Sahara':0,'Saudi Arabia':0,
				'Sudan':0,'South Sudan':0,'Senegal':0,'Solomon Islands':0,'Sierra Leone':0,'El Salvador':0,
				'Somaliland':0,'Somalia':0,'Republic of Serbia':0,'Suriname':0,'Slovakia':0,'Slovenia':0,
				'Sweden':0,'Swaziland':0,'Syria':0,'Chad':0,'Togo':0,'Thailand':0,'Tajikistan':0,
				'Turkmenistan':0,'East Timor':0,'Trinidad and Tobago':0,'Tunisia':0,'Turkey':0,
				'United Republic of Tanzania':0,'Uganda':0,'Ukraine':0,'Uruguay':0,'United States of America':0,
				'Uzbekistan':0,'Venezuela':0,'Vietnam':0,'Vanuatu':0,'West Bank':0,'Yemen':0,'South Africa':0,
				'Zambia':0,'Zimbabwe':0}
			else :
				dictionary2 = {'Afghanistan': '总销量为0，无法计算退货率！','Angola': '总销量为0，无法计算退货率！','Albania': '总销量为0，无法计算退货率！','United Arab Emirates':'总销量为0，无法计算退货率！','Argentina': '总销量为0，无法计算退货率！',
				'Armenia':'总销量为0，无法计算退货率！','French Southern and Antarctic Lands':'总销量为0，无法计算退货率！','Australia':'总销量为0，无法计算退货率！','Austria':'总销量为0，无法计算退货率！',
				'Azerbaijan':'总销量为0，无法计算退货率！','Burundi':'总销量为0，无法计算退货率！','Belgium':'总销量为0，无法计算退货率！','Benin':'总销量为0，无法计算退货率！','Burkina Faso':'总销量为0，无法计算退货率！','Bangladesh':'总销量为0，无法计算退货率！',
				'Bulgaria':'总销量为0，无法计算退货率！','The Bahamas':'总销量为0，无法计算退货率！','Bosnia and Herzegovina':'总销量为0，无法计算退货率！','Belarus':'总销量为0，无法计算退货率！','Belize':'总销量为0，无法计算退货率！',
				'Bermuda':'总销量为0，无法计算退货率！','Bolivia':'总销量为0，无法计算退货率！','Brazil':'总销量为0，无法计算退货率！','Brunei':'总销量为0，无法计算退货率！','Bhutan':'总销量为0，无法计算退货率！','Botswana':'总销量为0，无法计算退货率！',
				'Central African Republic':'总销量为0，无法计算退货率！','Canada':'总销量为0，无法计算退货率！','Switzerland':'总销量为0，无法计算退货率！','Chile':'总销量为0，无法计算退货率！','China':'总销量为0，无法计算退货率！','Ivory Coast':'总销量为0，无法计算退货率！',
				'Cameroon':'总销量为0，无法计算退货率！','Democratic Republic of the Congo':'总销量为0，无法计算退货率！','Republic of the Congo':'总销量为0，无法计算退货率！','Colombia':'总销量为0，无法计算退货率！',
				'Costa Rica':'总销量为0，无法计算退货率！', 'Cuba':'总销量为0，无法计算退货率！','Northern Cyprus':'总销量为0，无法计算退货率！','Cyprus':'总销量为0，无法计算退货率！','Czech Republic':'总销量为0，无法计算退货率！',
				'Germany':'总销量为0，无法计算退货率！','Djibouti':'总销量为0，无法计算退货率！','Denmark':'总销量为0，无法计算退货率！','Dominican Republic':'总销量为0，无法计算退货率！','Algeria':'总销量为0，无法计算退货率！','Ecuador':'总销量为0，无法计算退货率！',
				'Egypt':'总销量为0，无法计算退货率！','Eritrea':'总销量为0，无法计算退货率！','Spain':'总销量为0，无法计算退货率！','Estonia':'总销量为0，无法计算退货率！','Ethiopia':'总销量为0，无法计算退货率！','Finland':'总销量为0，无法计算退货率！','Fiji':'总销量为0，无法计算退货率！',
				'Falkland Islands':'总销量为0，无法计算退货率！','France':'总销量为0，无法计算退货率！','Gabon':'总销量为0，无法计算退货率！','United Kingdom':'总销量为0，无法计算退货率！','Georgia':'总销量为0，无法计算退货率！','Ghana':'总销量为0，无法计算退货率！',
				'Guinea':'总销量为0，无法计算退货率！','Gambia':'总销量为0，无法计算退货率！','Guinea Bissau':'总销量为0，无法计算退货率！','Equatorial Guinea':'总销量为0，无法计算退货率！','Greece':'总销量为0，无法计算退货率！','Greenland':'总销量为0，无法计算退货率！',
				'Guatemala':'总销量为0，无法计算退货率！','French Guiana':'总销量为0，无法计算退货率！','Guyana':'总销量为0，无法计算退货率！','Honduras':'总销量为0，无法计算退货率！','Croatia':'总销量为0，无法计算退货率！','Haiti':'总销量为0，无法计算退货率！',
				'Hungary':'总销量为0，无法计算退货率！','Indonesia':'总销量为0，无法计算退货率！','India':'总销量为0，无法计算退货率！','Ireland':'总销量为0，无法计算退货率！','Iran':'总销量为0，无法计算退货率！','Iraq':'总销量为0，无法计算退货率！','Iceland':'总销量为0，无法计算退货率！',
				'Israel':'总销量为0，无法计算退货率！','Italy':'总销量为0，无法计算退货率！','Jamaica':'总销量为0，无法计算退货率！','Jordan':'总销量为0，无法计算退货率！','Japan':'总销量为0，无法计算退货率！','Kazakhstan':'总销量为0，无法计算退货率！','Kenya':'总销量为0，无法计算退货率！',
				'Kyrgyzstan':'总销量为0，无法计算退货率！','Cambodia':'总销量为0，无法计算退货率！','South Korea':'总销量为0，无法计算退货率！','Kosovo':'总销量为0，无法计算退货率！','Kuwait':'总销量为0，无法计算退货率！','Laos':'总销量为0，无法计算退货率！','Lebanon':'总销量为0，无法计算退货率！',
				'Liberia':'总销量为0，无法计算退货率！','Libya':'总销量为0，无法计算退货率！','Sri Lanka':'总销量为0，无法计算退货率！','Lesotho':'总销量为0，无法计算退货率！','Lithuania':'总销量为0，无法计算退货率！','Luxembourg':'总销量为0，无法计算退货率！','Latvia':'总销量为0，无法计算退货率！',
				'Morocco':'总销量为0，无法计算退货率！','Moldova':'总销量为0，无法计算退货率！','Madagascar':'总销量为0，无法计算退货率！','Mexico':'总销量为0，无法计算退货率！','Macedonia':'总销量为0，无法计算退货率！','Mali':'总销量为0，无法计算退货率！','Myanmar':'总销量为0，无法计算退货率！',
				'Montenegro':'总销量为0，无法计算退货率！','Mongolia':'总销量为0，无法计算退货率！','Mozambique':'总销量为0，无法计算退货率！','Mauritania':'总销量为0，无法计算退货率！','Malawi':'总销量为0，无法计算退货率！','Malaysia':'总销量为0，无法计算退货率！',
				'Namibia':'总销量为0，无法计算退货率！','New Caledonia':'总销量为0，无法计算退货率！','Niger':'总销量为0，无法计算退货率！','Nigeria':'总销量为0，无法计算退货率！','Nicaragua':'总销量为0，无法计算退货率！','Netherlands':'总销量为0，无法计算退货率！',
				'Norway':'总销量为0，无法计算退货率！','Nepal':'总销量为0，无法计算退货率！','New Zealand':'总销量为0，无法计算退货率！','Oman':'总销量为0，无法计算退货率！','Pakistan':'总销量为0，无法计算退货率！','Panama':'总销量为0，无法计算退货率！','Peru':'总销量为0，无法计算退货率！',
				'Philippines':'总销量为0，无法计算退货率！','Papua New Guinea':'总销量为0，无法计算退货率！','Poland':'总销量为0，无法计算退货率！','Puerto Rico':'总销量为0，无法计算退货率！','North Korea':'总销量为0，无法计算退货率！','Portugal':'总销量为0，无法计算退货率！',
				'Paraguay':'总销量为0，无法计算退货率！','Qatar':'总销量为0，无法计算退货率！','Romania':'总销量为0，无法计算退货率！','Russia':'总销量为0，无法计算退货率！','Rwanda':'总销量为0，无法计算退货率！','Western Sahara':'总销量为0，无法计算退货率！','Saudi Arabia':'总销量为0，无法计算退货率！',
				'Sudan':'总销量为0，无法计算退货率！','South Sudan':'总销量为0，无法计算退货率！','Senegal':'总销量为0，无法计算退货率！','Solomon Islands':'总销量为0，无法计算退货率！','Sierra Leone':'总销量为0，无法计算退货率！','El Salvador':'总销量为0，无法计算退货率！',
				'Somaliland':'总销量为0，无法计算退货率！','Somalia':'总销量为0，无法计算退货率！','Republic of Serbia':'总销量为0，无法计算退货率！','Suriname':'总销量为0，无法计算退货率！','Slovakia':'总销量为0，无法计算退货率！','Slovenia':'总销量为0，无法计算退货率！',
				'Sweden':'总销量为0，无法计算退货率！','Swaziland':'总销量为0，无法计算退货率！','Syria':'总销量为0，无法计算退货率！','Chad':'总销量为0，无法计算退货率！','Togo':'总销量为0，无法计算退货率！','Thailand':'总销量为0，无法计算退货率！','Tajikistan':'总销量为0，无法计算退货率！',
				'Turkmenistan':'总销量为0，无法计算退货率！','East Timor':'总销量为0，无法计算退货率！','Trinidad and Tobago':'总销量为0，无法计算退货率！','Tunisia':'总销量为0，无法计算退货率！','Turkey':'总销量为0，无法计算退货率！',
				'United Republic of Tanzania':'总销量为0，无法计算退货率！','Uganda':'总销量为0，无法计算退货率！','Ukraine':'总销量为0，无法计算退货率！','Uruguay':'总销量为0，无法计算退货率！','United States of America':'总销量为0，无法计算退货率！',
				'Uzbekistan':'总销量为0，无法计算退货率！','Venezuela':'总销量为0，无法计算退货率！','Vietnam':'总销量为0，无法计算退货率！','Vanuatu':'总销量为0，无法计算退货率！','West Bank':'总销量为0，无法计算退货率！','Yemen':'总销量为0，无法计算退货率！','South Africa':'总销量为0，无法计算退货率！',
				'Zambia':'总销量为0，无法计算退货率！','Zimbabwe':'总销量为0，无法计算退货率！'}
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


	elif module == 2:  #时间分析
		time_dict,passOrNot,tradeNo_rtn_reason_print = sql_time.time_sql(sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect)
		dictionary = time_dict
		# 【 结 论 总 结 】 最大、最小、平均、比例等
		maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason = max_min_average.max_min_ave_sum(dictionary,aspect,module_unit)
		# 【 结 论 输 出 】
		conclusionPrint = conclusion.final_conclusion(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module)
		#print (dictionary)

		dictionaryToList = [(key,dictionary[key]) for key in sorted(dictionary.keys())] #按key的大小排序
		timeline = []
		timelineValue = []
		for key,value in dictionaryToList:
			timeline.append(key)
			timelineValue.append(value)
		dictionary2 = {}
		dictionary2['timeline'] = timeline
		dictionary2['timelineValue'] = timelineValue
		print (dictionary2)
		#print (dictionary2)
		
		return dictionary2,conclusionPrint,module_name,aspect_name,unite,maxValue


	elif module == 3:  #钢种分析
		trade_dict,passOrNot,tradeNo_rtn_reason_print,chooseTrade_sum,allTrade_sum = sql_trade.trade_sql(sql_date1,sql_date2,sql_ctry_prov_cty,tradeNo_list,space_name,aspect_name,dateChoose,aspect)
		dictionary = trade_dict

		# 【 结 论 总 结 】 最大、最小、平均、比例等   #【 占 全 部 钢 种 比 例 】
		maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason,tradeNo_rate_dict = max_min_average.max_min_ave_sum_trade(dictionary,aspect,module_unit,allTrade_sum)
		# 【 结 论 输 出 】 #与前两个不一样
		conclusionPrint = conclusion.final_conclusion_trade(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,tradeNo_rate_dict,module)
		return dictionary,conclusionPrint,module_name,aspect_name,unite,maxValue
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
		return dictionary,conclusionPrint,module_name,aspect_name,unite,maxValue




if __name__ == '__main__':

	dictionary,conclusionPrint,module_name,aspect_name,unite,maxValue = main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space)
	#print (module,tradeNo)


	'''
		#=====================【 结 果 存 储 】==================================
		#将结果存储在txt文本中
		save_txt.write(dictionary,filename,conclusion)

	'''








