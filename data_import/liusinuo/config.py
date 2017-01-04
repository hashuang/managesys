
#实验室
db_host = '202.204.54.215'
db_user = 'root'
db_password = '123456'
db_name = 'qinggang'
db_port = 3306

'''
#我的电脑
db_host = 'localhost'
db_user = 'root'
db_password = '123456'
db_name = 'qinggang'
db_port = 3306
'''

#MES
oralce_db_host = '10.30.0.17' #改为相关主机的ip地址
oralce_db_user = 'BD_query'
oralce_db_password = 'BD_query'
oralce_listener_name = 'mesdb'#询问监听器的名字
oralce_db_port = 1521

#二级
# oralce_db_host = '10.20.0.22' #改为相关主机的ip地址
# oralce_db_user = 'BD_query'
# oralce_db_password = 'BD_query'
# oralce_listener_name = 'qgil2db'#询问监听器的名字
# oralce_db_port = 1521

row_num=2000
dir_root="F:/desktop"
table_name="DATA_IMPORT_TRANSRELATION"



#sql所需变量

csql_prov="'江苏'" #地点
csql_date1=20160105 #起始时间
csql_date2=20160105 #中止时间
ctrade="C86D2" #单个钢种
ctradeNo_list = ["C86D2","80"] #多个钢种
