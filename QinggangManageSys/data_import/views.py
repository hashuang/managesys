from django.shortcuts import render
from . import models
from django.http import HttpResponse
from . import util
# Create your views here.
def home(req):
	TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
	# print('here')
	# print("{0}{1}{2}{3}{4}".format(req.get_host(),req.is_secure(),req.path,req.get_full_path(),req.META))
	# rs=TransRelation.objects.get_all_tr()
	# print(rs)
	# for r in rs:
	# 	TransRelation.objects.filter(uid=r.uid).update(own_col=r.uid)
	attrs=util.get_model_attrs(models.TransRelation)
	print(attrs)
	
	return render(req,'index.html',{'title':"青特钢大数据项目组数据管理"})


def search(req):

	return render(req,'index.html',{'title':"青特钢大数据项目组数据管理--检索结果"})

def about(req):

	return render(req,'about.html',{'title':"关于项目"})


def data_import(req):
	filepath = 'F:\\development\\python\\data_exchange\\数据迁移中间表1.xlsx'
	util.batch_import_data(filepath,models.TransRelation)
	records=models.TransRelation.objects.generic_query('select * from {0}'.format(models.TransRelation._meta.db_table))

	# for record in records:
	# 	print(record.own_col)
	# print(records)
	# for r in records:
	# 	print(r.from_uid)
	return render(req,'index.html',{'title':"导入结果",'records':records})


def transfer():
	tr = models.TransRelation.objects.all()
	for each  in tr:
		db_name = each.from_system
		sql_select= 'SELECT {0} FROM TABLE {1} WHERE uid={2}'.format(each.from_col,each.from_table,each.uid)

		#先通过uid获取元素
		sql_insert= 'INSERT INTO {0} (own_col) values({1})'.format(each.own_table,each.own_col)