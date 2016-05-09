from django.db import models,connection,connections
from . import util


class BaseManage(models.Manager):
	#根据传入属性dict生成增删改查的sql，使用raw方法进行查询，针对绑定了model的情况
	#如果没有绑定model，也可以使用direct_xxxx_query_sqlVO传入得到的sqlVO进行查询
	def raw_query_sqlVO(self,sqlVO):
		return self.raw(sqlVO.get('sql'),sqlVO.get('vars'))

	def add_rows(self,attrs,model):
		sqlVO= util.create_insert_sql(model,attrs)
		return self.raw_query_sqlVO(sqlVO)
	def select_rows(self,attrs,model):
		sqlVO= util.create_insert_sqlVO(model,attrs)
		return  self.raw_query_sqlVO(sqlVO)
	def update_rows(self,attrs,model):
		sqlVO= util.create_update_sqlVO(model,attrs)
		return self.raw_query_sqlVO(sqlVO)
	def delete_rows(self,attrs,model):
		sqlVO= util.create_delete_sqlVO(model,attrs)
		return self.raw_query_sqlVO(sqlVO)
	'''
	queries that don’t map cleanly to models, or directly execute UPDATE, INSERT, or DELETE queries.
	'''
	#将结果返回为dict
	def dictfetchall(seff,cursor):
		columns = [col[0] for col in cursor.description]
		print(columns)
		return [
	        dict(zip(columns, row))
	        for row in cursor.fetchall()
    	]

	def direct_select_query_sqlVO(self,sqlVO):
		#如果是多数据库
		#cursor = connections['my_db_alias'].cursor()
		db_name=sqlVO.get('db_name')
		if sqlVO.get('db_name')!=None:
			cursor = connections[db_name].cursor()
		else:
			cursor = connection.cursor()
		cursor.execute(sqlVO.get('sql'),sqlVO.get('vars'))
		return self.dictfetchall(cursor)

	def direct_execute_query_sqlVO(self,sqlVO):
		#如果是多数据库
		#cursor = connections['my_db_alias'].cursor()
		db_name=sqlVO.get('db_name')
		if sqlVO.get('db_name')!=None:
			cursor = connections[db_name].cursor()
		else:
			cursor = connection.cursor()
		cursor.execute(sqlVO.get('sql'),sqlVO.get('vars'))


# Create your models here.
class TransRelationManage(BaseManage):
	def get_all_tr(self):
		return self.all()





class TransRelation(models.Model):
	own_uid = models.CharField(max_length=200,blank=True)
	classification = models.CharField(max_length=200,blank=True)
	real_meaning = models.CharField(max_length=200,blank=True)
	own_table = models.CharField(max_length=200,blank=True)
	own_col = models.CharField(max_length=200,blank=True)
	from_uid = models.CharField(max_length=200)
	from_system = models.CharField(max_length=200,blank=True)
	from_dept = models.CharField(max_length=200,blank=True)
	from_table = models.CharField(max_length=200,blank=True)
	from_col = models.CharField(max_length=200,blank=True)
	remarks = models.CharField(max_length=200,blank=True)
 	
	def set_attr(self,**kwargs):
		#print(kwargs.items())
		for item in kwargs.items():
			for each in item[1].items():
				#print('{0}:{1}'.format(each[0],each[1]))
				setattr(self,each[0],each[1])

	def __unicode__(self):
		return u'{uid}{own_col}{from_col}'.format(uid=self.uid,own_col=self.own_col,from_col=self.from_col)

	objects = TransRelationManage()


class steel_price(models.Model):
	own_uid = models.CharField(max_length=200,blank=True) 
	final_price = models.FloatField(blank=True)
	highest_price = models.FloatField(blank=True)
	lowest_price =models.FloatField(blank=True)
	count = models.FloatField(blank=True)
	count_price = models.FloatField(blank=True)



