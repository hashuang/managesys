'''

2016-10-21

对应 space.py 代码

将此大程序拆分成几个小程序

'''

#=====================【 结 论 输 出 】==================================
def basical_info(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,module_unit):
	#基本信息
	print ("\n在",sql_date1,"至",sql_date2,"内，钢种",tradeNoList,"在",space_name,"范围内的",aspect_name,"分布如上图。")
	conclusion = "\n在" + sql_date1 + "至" + sql_date2 + "内，钢种" + tradeNoList + "在" + space_name + "范围内的" + aspect_name + "分布如上图。"
	return conclusion

def basical_info_cust(sql_date1,sql_date2,tradeNoList,sql_cust,aspect_name,module_unit):
	#基本信息
	print ("\n对于客户",sql_cust,"，在",sql_date1,"至",sql_date2,"时间内，钢种",tradeNoList,"的",aspect_name,"分布如上图。")
	conclusion = "\n对于客户" + sql_cust + "，在" + sql_date1 + "至" + sql_date2 + "内，钢种" + tradeNoList + "的" + aspect_name + "分布如上图。"
	return conclusion

def basical_info_cust2(sql_date1,sql_date2,sql_cust,aspect_name,module_unit):
	#基本信息
	print ("\n对于客户",sql_cust,"，在",sql_date1,"至",sql_date2,"时间内，全部销售钢种的",aspect_name,"分布如上图。")
	conclusion = "\n对于客户" + sql_cust + "，在" + sql_date1 + "至" + sql_date2 + "内，全部销售钢种的" + aspect_name + "分布如上图。"
	return conclusion

def conclusion_info(conclusion,printMax,maxRateReason,aspect_name,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,module_unit,noMin,aspect,module):
	#列出 最大值、最小值
	if module == 3:
		suoyou = "所选"
	else:
		suoyou = "所有"

	if printMax == 0: #如果sum等于零，则最大值与最小值无意义
		print (maxRateReason)
		conclusion = conclusion + maxRateReason
	else:
		if aspect != 3: #退货率不求总和与最大值
			#总量与平均值
			print ("\n其中，",suoyou,module_unit,"的",aspect_name,"为",sumValue,unite,"，平均值为",averageValue,unite,"。")
			conclusion = conclusion + "\n" + "其中，" + suoyou + module_unit + "的" + aspect_name + "为" + str(sumValue) + unite + "，平均值为" + str(averageValue)  + unite + "。"
		else:
			pass

		#列出最大值
		print ("最大值出现在",maxKey,module_unit,"，值为",maxValue,unite,"；")
		conclusion = conclusion + "最大值出现在" + maxKey + module_unit + "，值为" + str(maxValue) + unite + "；" 
		#如果出了中国剩下的都无意义，则不显示最小值这一结论
		if noMin != 0:
			print ("最小值出现在",minKey,module_unit,"，值为",minValue,unite,"。")
			conclusion = conclusion + "最小值出现在" + minKey + module_unit + "，值为" + str(minValue) + unite + "。"
		else:
			print("除最大值外，其他值均无意义，不存在最小值。")
			conclusion = conclusion + "除最大值外，其他值均无意义，不存在最小值。"

		#除退货率意向外，其他项目进需求出最大值的占比
		if aspect != 3 :
			print ("最大值占比",maxRate100,"%。")
			conclusion = conclusion + "最大值占比" + str(maxRate100) + "%。"	
		else:
			pass
	return conclusion

def trade_rate_choose_info(conclusion,tradeNo_rate_choose_dict,aspect):

	if aspect == 1 or aspect == 2:
		tem_clnclusion = "\n\n对于所选钢种，各钢种所占比例为：\n"
		for tradeNo in tradeNo_rate_choose_dict:
			tem_clnclusion = tem_clnclusion + tradeNo + ":" + str(tradeNo_rate_choose_dict[tradeNo]) + "% \n"
		print (tem_clnclusion)
		conclusion = conclusion + tem_clnclusion
		return conclusion
	else:
		return conclusion


def trade_rate_info(conclusion,tradeNo_rate_dict,aspect):

	# if aspect == 1 or aspect == 2:
	# 	tem_clnclusion = "\n对于全部钢种，各钢种所占比例为：\n"
	# 	for tradeNo in tradeNo_rate_dict:
	# 		tem_clnclusion = tem_clnclusion + tradeNo + ":" + str(tradeNo_rate_dict[tradeNo]) + "% \n"
	# 	print (tem_clnclusion)
	# 	conclusion = conclusion + tem_clnclusion
	# 	return conclusion
	# else:
	# 	return conclusion
	return conclusion


def return_info(aspect,passOrNot,tradeNo_rtn_reason_print,conclusion):
	#列出详细退货信息
	if aspect == 3 or aspect == 4: #如果是退货率或质量问题，列出详细清单
		if passOrNot == 1:
			pass
		else:
			#print ("退货与质量问题详细信息",tradeNo_rtn_reason_print)
			k = 0
			tradeNo_rtn_reason_conclusion = ""

			while k < len(tradeNo_rtn_reason_print) :
				tradeNo_rtn_reason_conclusion = tradeNo_rtn_reason_conclusion + "\n" + str(tradeNo_rtn_reason_print[k])############# 这 句 有 问 题 ##### tuple 不 能 转 化 为 str ########	
				#print (tradeNo_rtn_reason_print[k])
				#print (str(tradeNo_rtn_reason_print[k]))
				k += 1
			print (tradeNo_rtn_reason_conclusion)
			conclusion = conclusion + "\n退货与质量问题详细信息：\n" + tradeNo_rtn_reason_conclusion

	else:
		pass
	return conclusion

def final_conclusion(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module):
	conclusion = basical_info(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,module_unit)
	conclusion = conclusion_info(conclusion,printMax,maxRateReason,aspect_name,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,module_unit,noMin,aspect,module)
	conclusion = return_info(aspect,passOrNot,tradeNo_rtn_reason_print,conclusion)

	return conclusion

# 针 对 钢 种 分 析 另 加 一 个 占 全 部 钢 种 的 结 论
def final_conclusion_trade(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,tradeNo_rate_dict,module,tradeNo_rate_choose_dict):
	conclusion = basical_info(sql_date1,sql_date2,tradeNoList,space_name,aspect_name,module_unit)
	conclusion = conclusion_info(conclusion,printMax,maxRateReason,aspect_name,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,module_unit,noMin,aspect,module)
	conclusion = trade_rate_choose_info(conclusion,tradeNo_rate_choose_dict,aspect)
	conclusion = trade_rate_info(conclusion,tradeNo_rate_dict,aspect)
	conclusion = return_info(aspect,passOrNot,tradeNo_rtn_reason_print,conclusion)

	return conclusion

# 针 对 客 户 分 析
def final_conclusion_cust(sql_date1,sql_date2,tradeNoList,sql_cust,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module):
	conclusion = basical_info_cust(sql_date1,sql_date2,tradeNoList,sql_cust,aspect_name,module_unit)
	conclusion = conclusion_info(conclusion,printMax,maxRateReason,aspect_name,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,module_unit,noMin,aspect,module)
	conclusion = return_info(aspect,passOrNot,tradeNo_rtn_reason_print,conclusion)

	return conclusion

def final_conclusion_cust2(sql_date1,sql_date2,sql_cust,aspect_name,printMax,maxRateReason,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,aspect,passOrNot,tradeNo_rtn_reason_print,module_unit,noMin,module):
	conclusion = basical_info_cust2(sql_date1,sql_date2,sql_cust,aspect_name,module_unit)
	conclusion = conclusion_info(conclusion,printMax,maxRateReason,aspect_name,sumValue,unite,averageValue,maxKey,maxValue,minKey,minValue,maxRate100,module_unit,noMin,aspect,module)
	conclusion = return_info(aspect,passOrNot,tradeNo_rtn_reason_print,conclusion)

	return conclusion