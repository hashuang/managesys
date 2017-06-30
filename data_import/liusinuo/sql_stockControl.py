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
import math
from functools import reduce
import data_import.models as models

	
def sql_stockControl(module,tradeNo,module_unit_key):
	#========================【 输 入 】===========================
	print("开始执行stockControl.py文件中的函数\n\n")
	#按钢种查询数据库
	sqlVO={}
	sqlVO["db_name"]="l2own"
	# // sqlVO["sql"]="SELECT HEAT_NO,SPECIFICATION,OPERATECREW FROM qg_user.PRO_BOF_HIS_ALLFIELDS WHERE HEAT_NO='"+heat_no+"'";
	# // sqlVO["sql"]="查询语句";
	# // scrapy_records=models.BaseManage().direct_select_query_sqlVO(sqlVO)


	#港中名称/总重量/3月以上库存量，list
	#按钢种总重量大小顺序排列
	#按3月库存量大小排列
	#
	dictionary = {'1': 1,'2': 2,'3': 3,'4': 4}
	conclusionPrint = "这是结论"
	module_name = "这是模块名称，第二个参数"
	return dictionary,conclusionPrint,module_name





if __name__ == '__main__':

	dictionary,conclusionPrint,module_name = sql_stockControl(module,tradeNo,module_unit_key)
	print("stockControl.py文件中的函数执行完毕\n\n")
	#print (module,tradeNo)








