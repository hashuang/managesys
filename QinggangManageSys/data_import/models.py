from django.db import models,connection
from . import util
class BaseManage(models.Manager):

	def add_rows(self,attrs,model):
		sql= util.create_insert_sql(model,attrs)
		return self.raw(sql)

	def update_rows(self,attrs,model):
		sql= util.create_update_sql(model,attrs)
		return self.raw(sql)

	def delete_rows(self,attrs,model):
		sql= util.create_delete_sql(model,attrs)
		return self.raw(sql)

	def generic_query(self,sql):
		print(sql)
		return self.raw(sql)
	
	def direct_query(self,sql):
		cursor = connection.cursor()
		cursor.execute(sql)
		row = cursor.fetchone()
		return row

    #将结果返回为dict
	def dictfetchall(cursor):
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

# Create your models here.
class TransRelationManage(BaseManage):
	def get_all_tr(self):
		return self.all()


class BaseModel(models.Model):
	def set_attr(self,**kwargs):
		#print(kwargs.items())
		for item in kwargs.items():
			for each in item[1].items():
				#print('{0}:{1}'.format(each[0],each[1]))
				setattr(self,each[0],each[1])

class TransRelation(BaseModel):
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
 	
	def __unicode__(self):
		return u'{uid}{own_col}{from_col}'.format(uid=self.uid,own_col=self.own_col,from_col=self.from_col)

	objects = TransRelationManage()


