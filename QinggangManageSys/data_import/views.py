import os
import json

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import F

from . import models
from data_import.forms import UploadFileForm
from . import util
from . import const



def home(request):
	print('请求主页')
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")
	#sqlVO = util.create_select_sqlVO(models.TransRelation,{'own_uid':'changxin'})
	# sqlVO={}
	# sqlVO['sql']='select * from db.tbaa011b t where rownum<=20'#'select * from qg_ift_user.if_bf1_l2l2_bfthroattemp t where rownum<=20'
	#'select * from db.tbaa011b t where rownum<=20'#'SELECT * FROM data_import_transrelation WHERE rownum<=200';
	# sqlVO['db_name']='mes'
	#print(sqlVO)
	#{'vars': {'slagWgt': 0}, 'sql': 'UODATE data_import_converter SET slagWgt=:slagWgt WHERE heat_no=1530501'}
	#rs=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	#print("records:{records}".format(records=rs))
	#util.get_primary_key(models.TransRelation)
	return render(request,'index.html',{'title':"青特钢大数据项目组数据管理"})

def data_import(request):
	print('导入中间表')
	filepath = 'F:\\development\\python\\data_exchange\\数据迁移中间表终极样式初稿.xlsx'
	util.batch_import_data(filepath,models.TransRelation)
	records=models.TransRelation.objects.direct_select_query_sqlVO({'sql':'select * from {0}'.format(models.TransRelation._meta.db_table)})
	print("records:{records}".format(records=records))
	#records=None
	model=None
	if records !=None:
		#通过表名反射相应的对象
		i=1
		for record in records:
			sqlVO={}
			class_name = record['own_table']
			print(class_name)
			model = getattr(models,class_name)
			table_name=model._meta.db_table
			print(model)
			#select所有的关联字段,获取所有的关联字段
			if i==1:
				sqlVO=util.get_all_uid_sqlVO(record)
				#取所有的own-col
				print(sqlVO)
				uids=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				print(uids)
				for uid in uids:
					attrdict={}
					attrdict[record['own_uid']]=uid[record['from_uid'].upper()]
					real_model=model()
					real_model.set_attr(attrdict=attrdict)
					real_model.save()
					#real_model.save()
				#print(type(uids))
				i=i+1
			#sql = 'SELECT '+record['FROM_COL']+' FROM '+record['FROM_TABLE']+' WHERE '+record['FROM_UID']
			#取出所有的关联字段
			print(table_name)
			select_uid_sql = 'SELECT ' +record['own_uid'] +' FROM ' +table_name
			sqlVO={'sql':select_uid_sql}
			print(sqlVO)
			own_uids=models.BaseManage().direct_select_query_sqlVO(sqlVO)
			for uid in own_uids:
				own_uid_col=record['own_uid'].lower()
				own_id=uid[own_uid_col]
				sqlVO=util.get_value_by_uid_sqlVO(record,own_id)
				value=models.BaseManage().direct_select_query_sqlVO(sqlVO)
				insert_value=util.change_value_2_insert(value)
				dictVO={'record':record,'value':insert_value,'table_name':table_name,'own_id':own_id}
				sqlVO=util.create_update_by_uid_sqlVO(dictVO)
				print(sqlVO)
				models.BaseManage().direct_execute_query_sqlVO(sqlVO)
			print(sqlVO)

				#model.objects.filter(F(own_uid_col)=own_id).update(F(own_col)=insert_value)
				#print(sqlVO)
			print('################################################3')
		return render(request,'index.html',{'title':"导入结果",'records':records})
	else:
		return HttpResponseRedirect("/index")
'''
{'FROM_TABLE': 'db.tboj202', 'OWN_UID': 'heat_no', 'FROM_UID': 'heat_no', 'FRES', 'REAL_MEANING': '出钢量(t)', 
'FROM_COL': 'steelWgt', 'FROM_DEPT': '炼钢转炉', 'OWN_TABLE': 'CONVERTER
'OWN_COL': 'steelWgt', 'CLASSIFICATION': '出钢量', 'REMARKS': '0', 'FROM_SYSTEM': 'MES',}
'''
#用户登录
def user_login(request):
	print('用户登录')
	contentVO={
		'title':'用户登录',
		'state':None
	}
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	print("username:{0},password:{1}".format(username,password))
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		print(user.__dict__)
		print(user.is_active)
		# Correct password, and the user is marked "active"
		auth.login(request, user)
		# Redirect to a success page.
		contentVO['state']='success'
		return HttpResponseRedirect("/index")
	print(contentVO['state'])
	return render(request,'login.html',contentVO)

#用户注册
def user_register(request):
	print("进行注册处理")
	contentVO={
		'title':'用户注册',
		'state':None
	}
	if request.method == 'POST':
		password = request.POST.get('password', '')
		repeat_password = request.POST.get('repeat_password', '')
		if password == '' or repeat_password == '':
			contentVO['state'] = 'empty'
		elif password != repeat_password:
			contentVO['state'] = 'repeat_error'
		else:
			username = request.POST.get('username', '')
			if User.objects.filter(username=username):
				contentVO['state'] = 'user_exist'
			else:
				new_user = User.objects.create_user(username=username, password=password,email=request.POST.get('email', ''))
				new_user.save()
				contentVO['state'] = 'success'
				return HttpResponseRedirect('/login')
	print(contentVO['state'])
	return render(request,'register.html',contentVO)

#用户登出
def user_logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')

#修改密码
@login_required()
def modify_password(request):
	print("修改密码")
	contentVO={
		'title':'修改密码',
		'state':None
	}
	user=request.user
	print('用户名：{0}'.format(user.username))
	oldpassword = request.POST.get('oldpassword','')
	if user.check_password(oldpassword):
		newpassword = request.POST.get('newpassword', '')
		repeat_newpassword = request.POST.get('repeat_newpassword', '')
		if newpassword == '' or repeat_newpassword == '':
			contentVO['state']='empty'
		elif newpassword != repeat_newpassword:
			contentVO['state'] = 'repeat_error'
		else:
			user.set_password(newpassword)
			user.save()
			contentVO['state'] = 'success'
	print(contentVO['state'])
	return render(request,'modify_password.html',contentVO)


#重置密码
def reset_password(request):
	return HttpResponseRedirect("/index")


def transfer():
	tr = models.TransRelation.objects.all()
	for each  in tr:
		db_name = each.from_system
		sql_select= 'SELECT {0} FROM TABLE {1} WHERE uid={2}'.format(each.from_col,each.from_table,each.uid)
		util.BaseManage.generic_query(sql_select)
		#先通过uid获取元素
		sql_insert= 'INSERT INTO {0} (own_col) values({1})'.format(each.own_table,each.own_col)
from QinggangManageSys.settings import BASE_DIR
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/success')
	else:
		form = UploadFileForm()
		print(form.__dict__)
	return render(request,'form.html', {'form': form})

def handle_uploaded_file(f):
	filename=f._name
	filetype=filename.split('.')[-1]
	print(filetype)
	filepath=BASE_DIR +"\\data_import\\media\\upload\\"+filename
	with open(filepath, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


def success(request):
	return render(request,'success.html')

from django.core.mail import send_mail
def ajaxtest(request):
	filepath=BASE_DIR +"\\data_import\\static\\libs\\echarts\\map\\"
	print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	contentVO={
		'title':'ajaxtest请求结果',
		'state':'success'
	}
	#send_mail('Subject here', 'Here is the message.', '525794244@qq.com',
    #['525794244@qq.com'], fail_silently=False)
	with open(filepath+'world.json','r')as f:
		data=json.load(f)
	contentVO['greet']="hello world"
	print(type(data.get("features")))
	return HttpResponse(json.dumps(contentVO), content_type='application/json')

def loadjson(request):
	filepath=BASE_DIR +"\\data_import\\static\\libs\\echarts\\map\\"
	contentVO={

		'title':'json请求结果',
		'state':'success'
	}
	with open(filepath+'china.json','r',encoding='utf-8')as f:
		data=json.load(f)
	contentVO['data']=data
	return HttpResponse(json.dumps(contentVO), content_type='application/json')






	