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

	return dictionary,conclusionPrint


if __name__ == '__main__':

	dictionary,conclusionPrint = main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space)
	print (module,tradeNo)

	'''
		#=====================【 结 果 存 储 】==================================
		#将结果存储在txt文本中
		save_txt.write(dictionary,filename,conclusion)

	'''








