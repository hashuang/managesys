import time

import openpyxl

from . import mysql 
from . import config 


dir_root="F:/desktop"
table_name="DATA_IMPORT_TRANSRELATION"


def table_colsname(description):
    col_list = []
    for col in description:
        col_list.append(col[0]+'^'+col[1].__name__+'^'+str(col[2]))
    print(col_list)
    return col_list


def save_file(conn_oracle,table_name):
	start = time.clock()
	print("save_file:%s"%dir_root)
	wb = openpyxl.Workbook()
	ws = wb.active
	table_name= table_name.upper()
	table_name = table_name.strip("\n")
	print(table_name)
	sql = "SELECT * FROM "+ table_name+ " WHERE ROWNUM<="+str(config.row_num) #
	# + " WHERE ROWNUM<=200"
	rs_cur = conn_oracle.select(sql)

	if rs_cur==False:	
		return False
	else:
		col_name =table_colsname(rs_cur.description)
		print(rs_cur.description)
		print(rs_cur)
		try:
			ws.append(col_name)
		except Exception:
			
			return False
		try:
			rs= rs_cur.fetchall()
			for r in rs:
				try:
					ws.append(r)
				except Exception:
					
					return False
		except Exception:
			return False
		
		path = config.dir_root+"\\"+config.table_name+ ".xlsx"
		print(path)
		wb.save(path)
		end=time.clock()
		end_time = end-start
		end_time=round(end_time,5)
		time.sleep(2)


def begin():
	conn_oracle = mysql.MySQL()
	path = config.dir_root+"\\"+config.table_name+ ".xlsx"
	print(path)
	save_file(conn_oracle,table_name)


if __name__ == "__main__":
	begin()
	#file_name=["L2系统_高炉1.txt","L2系统_高炉2.txt","L2系统_焦化.txt","L2系统_炼钢.txt","L2系统_烧结.txt","L2系统_轧钢.txt"]