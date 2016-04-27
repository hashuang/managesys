from django.db import models

# Create your models here.
class TRANSFORMATION_RELATION(models.Model):
	uid = models.CharField(max_length=200)
	classification = models.CharField(max_length=200)
	real_meaning = models.CharField(max_length=200)
	own_col = models.CharField(max_length=200)
	from_system = models.CharField(max_length=200)
	from_dept = models.CharField(max_length=200)
	from_table = models.CharField(max_length=200)
	from_col = models.CharField(max_length=200)
	remarks = models.CharField(max_length=200)
 	#models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		return self.own_col