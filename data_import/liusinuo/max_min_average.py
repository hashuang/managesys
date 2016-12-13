'''

2016-10-21

对应 v4_statistics.py 代码

将此大程序拆分成几个小程序

'''


#=====================【 结 论 总 结 】==================================

def max_min_average(dictionary):
	i = 0#用于计算平均值
	jmax = 0#用于计数列举的地区数
	jmin = 0#用于计数列举的地区数
	maxKey = ""
	minKey = ""
	pause = "、"
	deng = "等"
	maxValue = -1
	minValue = 99999999999999999999
	sumValue = 0
	noMin = 0
	averageValue = 0

	for key in dictionary:
		value = dictionary[key]
		if isinstance(value,(str)) == True: # 如果退货率无法计算，则输出str，不进行此步骤
			pass
		else:
			#大于现有最大值
			if value > maxValue:
				maxValue = value
				maxKey = key
				jmax = 0
			#等于现有最大值
			elif value == maxValue: #如果地区过多，只列举三个
				jmax = jmax + 1
				if jmax > 3:
					pass
				elif jmax == 3 :
					maxKey = maxKey + deng
				else:
					maxKey = maxKey + pause + key
			else:
				pass

			#小于现有最小值
			if value < minValue:
				minValue = value
				minKey = key
				noMin = noMin + 1
				jmin = 0
			#等于现有最小值
			elif value == minValue: #如果地区过多，只列举三个
				jmin = jmin + 1
				noMin = noMin + 1
				if jmin > 3:
					pass
				elif jmin == 3 :
					minKey = minKey + deng
				else:
					minKey = minKey + pause + key
				#print ("看看最小值神马情况",minKey,value,minValue,jmin)
			#print ("再看看最小值神马情况",minKey,value,minValue,jmin)
			else:
				pass

			#求sum
			sumValue = sumValue + value
			i = i + 1
	if i != 0:
		averageValue = sumValue / i
	else:
		pass
	return maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue

def maxrate(sumValue,aspect,maxValue,module_unit):
	#初始化
	printMax = 1
	maxRateReason = ""
	maxRate = 0
	maxRate100 = 0

	#求出最大值的占比
	if sumValue != 0: #sum不等于0时才进行计算
		if aspect != 3:#如果是退货率，不用求出占比
			isinstance(maxValue,(float))

			maxRate = maxValue / sumValue
			maxRate100 = maxRate * 100
			if isinstance(maxRate100,(float)):
				maxRate100 =  "%.5f" %(maxRate100) 
			else:
				pass
		else:
			pass

	else:#如果sum为零，则占比没有意义
		#print ("总量为0，无法计算比例")
		printMax = 0
		if aspect != 3:
			maxRateReason = "所有" + module_unit + "的值均为0，无法计算比例。"
		else:
			maxRateReason = "所有" + module_unit + "的值均为0或无意义，无法计算比例。"
	return printMax,maxRate,maxRate100,maxRateReason

def float_format(maxValue,minValue,sumValue,averageValue):
	#保留小数点后5位
	if isinstance(maxValue,(float)):
		maxValue =  "%.5f" % (maxValue)
	else:
		pass
	if isinstance(minValue,(float)):
		minValue =  "%.5f" % (minValue)
	else:
		pass
	if isinstance(sumValue,(float)):
		sumValue =  "%.5f" % (sumValue)
	else:
		pass
	if isinstance(averageValue,(float)):
		averageValue =  "%.5f" %(averageValue) 
	else:
		pass
	return maxValue,minValue,sumValue,averageValue

def tradeNo_rate(dictionary,allTrade_sum,aspect,module_unit):
	tradeNo_rate_dict = {}
	for tradeNo in dictionary:
		printMax,maxRate,maxRate100,maxRateReason = maxrate(allTrade_sum,aspect,dictionary[tradeNo],module_unit)
		if maxRateReason == "":
			tradeNo_rate_dict[tradeNo] = maxRate100
		else:
			tradeNo_rate_dict[tradeNo] = maxRateReason
	return tradeNo_rate_dict
			


def max_min_ave_sum(dictionary,aspect,module_unit):
	maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue = max_min_average(dictionary)
	printMax,maxRate,maxRate100,maxRateReason = maxrate(sumValue,aspect,maxValue,module_unit)
	maxValue,minValue,sumValue,averageValue = float_format(maxValue,minValue,sumValue,averageValue)
	#print ("max",maxValue,"maxkey",maxKey,"\nmin",minValue,"minkey",minKey,"\nnomin",noMin,"sum",sumValue,"ave",averageValue,"\nprintmax",printMax,"maxrate",maxRate,"maxrate100",maxRate100,"\nmaxratereason",maxRateReason)
	#print (str(sumValue))
	return maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason

def max_min_ave_sum_trade(dictionary,aspect,module_unit,allTrade_sum):
	maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue = max_min_average(dictionary)
	printMax,maxRate,maxRate100,maxRateReason = maxrate(sumValue,aspect,maxValue,module_unit)
	maxValue,minValue,sumValue,averageValue = float_format(maxValue,minValue,sumValue,averageValue)
	#print ("max",maxValue,"maxkey",maxKey,"\nmin",minValue,"minkey",minKey,"\nnomin",noMin,"sum",sumValue,"ave",averageValue,"\nprintmax",printMax,"maxrate",maxRate,"maxrate100",maxRate100,"\nmaxratereason",maxRateReason)
	
	tradeNo_rate_dict = tradeNo_rate(dictionary,allTrade_sum,aspect,module_unit)

	return maxValue,maxKey,minValue,minKey,noMin,sumValue,averageValue,printMax,maxRate,maxRate100,maxRateReason,tradeNo_rate_dict

