from collections import OrderedDict
PRO_BOF_HIS_ALLFIELDS_S=OrderedDict([
								
								('FURNACESEQ','炉龄'),
								('SPRAYGUNSEQ','枪龄'),
                                ('MIRON_WGT','铁水重量'),
								('MIRON_TEMP','铁水温度'),
								('MIRON_C','铁水C含量'),
								('MIRON_SI','铁水SI含量'),
								('MIRON_MN','铁水MN含量'),
								('MIRON_P','铁水P含量'),
								('MIRON_S','铁水S含量'),
								('SCRAP_NUM','废钢数量'),
								('scrap_96053101','大渣钢'),
								('scrap_96052200','自产废钢'),
								('scrap_16010101','重型废钢'),
								('scrap_16020101','中型废钢'),
								('scrap_16030101','未知废钢'),
								#('scrap_16040101','破碎废钢'),
								#('scrap_96052501','小渣钢'),		
								('COLDPIGWGT','生铁装入量'),
								('SCRAPWGT','废钢装入量'),
								('SCRAPWGT_COUNT','废钢装入计算量'),
								#('RETURNSTEELWEIGHT','回炉钢液量'),
								#('LADLESTATUS','包况'),
								#('LADLEAGE','包龄'),
								
								('L96020400','1#烧结矿'),
								#('L12010301','石灰石_15-40mm'),
								('L12010302','石灰石_40-70mm'),
								('L12010601','萤石_FL80'),
								#('L12010701','硅灰石'),
								('L12020201','增碳剂'),
								('L12020301','低氮增碳剂'),
								('L96040100','石灰'),
								('L96040200','轻烧白云石'),
								('L96053601','钢渣'),
								('L1602010074','未知料'),
								('HEAT_WGT','炉重(KG)'),
								('BEFARTEMP','氩前温度'),
								('N2CONSUME','氮气耗量'),
								('TOTALOXYGENCONSUME','总供氧耗量'),
								('SUM_BO_CSM','总吹氧消耗'),
								('FIRSTCATCHOXYGENCONSUME','一倒氧气耗量'),
								('CARBONTEMPERATURE','一倒温度(℃)'),
								('FIRSTCATCHCARBONC','一倒C%'),
								('FIRSTCATCHCARBONP','一倒P%'),
								('DOWNFURNACETIMES','倒炉次数'),
								('SUBLANCE_AGE','副枪枪龄'),
								('SUBLANCE_INDEPTH','副枪插入深度'),
								('O_CONT','定氧'),
								#('C_CONT','定碳'),
								('LEQHEIGH','液面高度'),
								('D1_BO_CSM','第一次吹氧消耗'),
								('D2_BO_CSM ','第二次吹氧消耗'),
								('D3_BO_CSM','第三次吹氧消耗'),
								('D4_BO_CSM ','第四次吹氧消耗'),
								('D5_BO_CSM ','第五次吹氧消耗'),
								('D6_BO_CSM','第六次吹氧消耗'),
								('D1_TEMP_VALUE','第一次测温值'),
								('D2_TEMP_VALUE','第二次测温值'),
								('D3_TEMP_VALUE','第三次测温值'),
								('D4_TEMP_VALUE','第四次测温值'),								
								
								('STEELWGT_COUNT','出钢量1'),
								('TOTAL_SLAB_WGT','出钢量2'),
								('LDG_STEELWGT_COUNT','煤气发生量1'),
								('LDG_TOTAL_SLAB_WGT','煤气发生量2'),
								('STEEL_SLAG','钢渣量'),
								('C','C'),
								('Si','Si'),
								('Mn','Mn'),
								('P','P'),
								('S','S'),
								('Al_T','Al_T'),
								('"AS"','AS'),
								('Ni','Ni'),
								('Cr','Cr'),
								('Cu ','Cu'),
								('Mo','Mo'),
								('V','V'),
								('Ti','Ti'),
								('Nb','Nb'),
								('W','W'),
								('Pb','Pb'),
								('Sn','Sn'),
								('Bi','Bi'),
								('B','B'),
								('Ca','Ca'),
								('N','N'),
								('Co','Co'),
								('Zr','Zr'),
								('Ce','Ce'),
								('Fe','Fe'),
										
								('L13010101','硅铁_Si72-80%、AL≤2%(粒度10-60mm)'),
								('L13010301','微铝硅铁_Si 72-80%、AL≤0.1%、Ti≤0.1%'),
								('L13020101','硅锰合金_Mn 65-72%、Si 17-20%'),
								('L13020201','高硅硅锰_Mn ≥60%、Si ≥27%'),
								('L13040400','中碳铬铁'),							
								#('SLAGTHICK','渣层厚度'),#1,8
								#('SCRAPSTEEL','调温废钢'),#2,7
								#('INSULATIONAGENT','保温剂(包)'),
								#('TEMPOFARRIVE','进站温度(℃)'),#数据量少
								#'TEMPOFDEPARTURE','出站温度(℃)'),
							
	
                       ])

PRO_BOF_HIS_ALLFIELDS_C=OrderedDict([
								('scrap_16040101','破碎废钢'),
								('scrap_96052501','小渣钢'),
								('RETURNSTEELWEIGHT','回炉钢液量'),
								('LADLESTATUS','包况'),
								('LADLEAGE','包龄'),
								('L12010301','石灰石_15-40mm'),
								('L12010701','硅灰石'),
								('C_CONT','定碳'),
								('SLAGTHICK','渣层厚度'),#1,8
								('SCRAPSTEEL','调温废钢'),#2,7
								('INSULATIONAGENT','保温剂(包)'),
								('TEMPOFARRIVE','进站温度(℃)'),#数据量少
								('TEMPOFDEPARTURE','出站温度(℃)'),
								])
							

PRO_BOF_HIS_ALLFIELDS_B=OrderedDict([

								('Event_3003','兑铁时间'),
								('Event_3004','兑废钢时间'),
								('Event_3001','处理开始时间'),
								('PUTSPRAYGUNTIME','下枪时间'),
								('TOTALTIMEOFOXYGEN','总供氧时间'),
								('BOTTOMBLOWING','底吹模式'),
								('TIMEOFOXYGEN','一倒供氧时间'),
								('Event_3002','处理结束时间'),
								('PERIOD','冶炼周期'),
								('Event_4003','通电开始时间'),
								('Event_4004','通电结束时间'),
								('STOVEHEATSNUM','补炉炉次'),
								('PITPATCHINGKIND','补炉炉次项目'),
								('D1_CHRGD_TIME','第1批加料时间'),
								('D1_CHRGD_TYPE','第1批加料类型'),
								('D2_CHRGD_TIME','第2批加料时间'),
								('D2_CHRGD_TYPE','第2批加料类型'),
								('D3_CHRGD_TIME','第3批加料时间'),
								('D3_CHRGD_TYPE','第3批加料类型'),
								('D4_CHRGD_TIME','第4批加料时间'),
								('D4_CHRGD_TYPE','第4批加料类型'),
								('D5_CHRGD_TIME','第5批加料时间'),
								('D5_CHRGD_TYPE','第5批加料类型'),
								('D6_CHRGD_TIME','第6批加料时间'),
								('D6_CHRGD_TYPE','第6批加料类型'),
								('D7_CHRGD_TIME','第7批加料时间'),
								('D7_CHRGD_TYPE','第7批加料类型'),
								('D8_CHRGD_TIME','第8批加料时间'),
								('D8_CHRGD_TYPE','第8批加料类型'),
								('D9_CHRGD_TIME','第9批加料时间'),
								('D9_CHRGD_TYPE','第9批加料类型'),
								('D10_CHRGD_TIME','第10批加料时间'),
								('D10_CHRGD_TYPE','第10批加料类型'),
								('D11_CHRGD_TIME','第11批加料时间'),
								('D11_CHRGD_TYPE','第11批加料类型'),
								('D12_CHRGD_TIME','第12批加料时间'),
								('D12_CHRGD_TYPE','第12批加料类型'),
								('D13_CHRGD_TIME','第13批加料时间'),
								('D13_CHRGD_TYPE','第13批加料类型'),
								('D14_CHRGD_TIME','第14批加料时间'),
								('D14_CHRGD_TYPE','第14批加料类型'),
								('D15_CHRGD_TIME','第15批加料时间'),
								('D15_CHRGD_TYPE','第15批加料类型'),
								('D16_CHRGD_TIME','第16批加料时间'),
								('D16_CHRGD_TYPE','第16批加料类型'),
								('D17_CHRGD_TIME','第17批加料类型'),
								('D18_CHRGD_TIME','第18批加料时间'),
								('D18_CHRGD_TYPE','第18批加料类型'),
								('D19_CHRGD_TIME','第19批加料时间'),
								('D19_CHRGD_TYPE','第19批加料类型'),
								('D20_CHRGD_TIME','第20批加料类型'),
								('D21_CHRGD_TIME','第21批加料时间'),
								('D21_CHRGD_TYPE','第21批加料类型'),
								('D22_CHRGD_TIME','第22批加料时间'),
								('D22_CHRGD_TYPE','第22批加料类型'),
								('D23_CHRGD_TIME','第23批加料时间'),
								('D23_CHRGD_TYPE','第23批加料类型'),
								('D24_CHRGD_TIME','第24批加料时间'),
								('D24_CHRGD_TYPE','第24批加料类型'),
								('D25_CHRGD_TIME','第25批加料时间'),
								('D25_CHRGD_TYPE','第25批加料类型'),
								('D26_CHRGD_TIME','第26批加料时间'),
								('D26_CHRGD_TYPE','第26批加料类型'),
								('D27_CHRGD_TIME','第27批加料时间'),
								('D27_CHRGD_TYPE','第27批加料类型'),
								('D28_CHRGD_TIME','第28批加料时间'),
								('D28_CHRGD_TYPE','第28批加料类型'),
								('D29_CHRGD_TIME','第29批加料时间'),
								('D29_CHRGD_TYPE','第29批加料类型'),
								('D30_CHRGD_TIME','第30批加料时间'),
								('D30_CHRGD_TYPE','第30批加料类型'),
								('D1_BOSTRT_TIME','第一次吹氧开始时间'),
								('D1_BOEND_TIME','第一次吹氧结束时间'),
								('D1_BO_DUR','第一次吹氧时间'),
								('D2_BOSTRT_TIME','第二次吹氧开始时间'),
								('D2_BOEND_TIME ','第二次吹氧结束时间'),
								('D2_BO_DUR','第二次吹氧时间'),
								('D3_BOSTRT_TIME','第三次吹氧开始时间'),
								('D3_BOEND_TIME','第三次吹氧结束时间'),
								('D4_BOSTRT_TIME','第四次吹氧开始时间'),
								('D4_BOEND_TIME','第四次吹氧结束时间'),
								('D4_BO_DUR','第四次吹氧时间'),
								('D5_BOSTRT_TIME','第五次吹氧开始时间'),
								('D5_BOEND_TIME','第五次吹氧结束时间'),
								('D5_BO_DUR ','第五次吹氧时间'),
								('D6_BOSTRT_TIME','第六次吹氧开始时间'),
								('D6_BOEND_TIME','第六次吹氧结束时间'),
								('D6_BO_DUR','第六次吹氧时间'),
								('D1_TEMP_TIME','第一次测温时间'),
								('D1_TEMP_TYPE','第一次测温位置'),
								('D1_TEMP_ACQ','第一次测温操作方式'),
								('D2_TEMP_TIME','第二次测温时间'),
								('D2_TEMP_TYPE','第二次测温位置'),
								('D2_TEMP_ACQ','第二次测温操作方式'),
								('D3_TEMP_TIME','第三次测温时间'),
								('D3_TEMP_TYPE','第三次测温位置'),
								('D3_TEMP_ACQ','第三次测温操作方式'),
								('D4_TEMP_TIME','第四次测温时间'),
								('D4_TEMP_TYPE ','第四次测温位置'),
								('D4_TEMP_ACQ','第四次测温操作方式'),
								('D1_SAMP_TIME','第一次取样时间'),
								('D1_SAMP_TYPE','第一次取样类型'),
								('D2_SAMP_TIME','第二次取样时间'),
								('D2_SAMP_TYPE','第二次取样类型'),
								('D3_SAMP_TIME','第三次取样时间'),
								('D3_SAMP_TYPE','第三次取样类型'),
								('D4_SAMP_TIME','第四次取样时间'),
								('D4_SAMP_TYPE','第四次取样类型'),
								('D5_SAMP_TIME','第五次取样时间'),
								('D5_SAMP_TYPE','第五次取样类型'),
								
								('final_TEMP_NO','最后一次测温的序号'),
								('final_TEMP_TIME','最后一次测温时间'),
								('final_TEMP_VALUE','最终测温值'),
								('final_TEMP_TYPE','最后一次测温位置'),
								('final_TEMP_ACQ','最后一次测温操作方式'),
								
								('Event_3010','出钢开始'),
								('Event_3011','出钢结束'),
								('TIMEOFSLAGSPLISHING','溅渣护炉时间'),
								('Event_3012','溅渣开始'),
								('Event_3013','溅渣结束'),
								('OPERATETIME','吹氩时间(min)'),
								('ARRIVEDATE','进吹氩站日期'),
								('ARRIVETIME','进吹氩站时刻'),
								('DEPARTUREDATE','出吹氩站日期'),
								('DEPARTURETIME','出吹氩站时刻'),
						])

