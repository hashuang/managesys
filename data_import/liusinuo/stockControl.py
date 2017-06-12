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

	
def main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space,space_detail,module_unit_key):
	#========================【 输 入 】===========================





if __name__ == '__main__':

	dictionary,conclusionPrint,module_name,aspect_name,unite,maxValue = main(module,aspect,dateChoose,sql_date1,sql_date2,sql_cust,tradeNo,space)
	#print (module,tradeNo)








