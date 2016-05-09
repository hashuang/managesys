from django.shortcuts import render
import os
from . import models
from . import forms
from django.http import HttpResponse,HttpResponseRedirect
from . import util
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth

# Create your views here.
def home(req):
	sqlVO = util.create_ora_select_sqlVO(models.TransRelation,{'own_uid':'changxin'})
	# sqlVO={}
	# sqlVO['sql']='select * from db.tbaa011b t where rownum<=20'#'select * from qg_ift_user.if_bf1_l2l2_bfthroattemp t where rownum<=20'
	#'select * from db.tbaa011b t where rownum<=20'#'SELECT * FROM data_import_transrelation WHERE rownum<=200';
	# sqlVO['db_name']='mes'
	print(sqlVO)
	rs=models.BaseManage().direct_select_query_sqlVO(sqlVO)
	print(rs)
	#util.get_primary_key(models.TransRelation)
	return render(req,'index.html',{'title':"青特钢大数据项目组数据管理"})


def search(req):

	return render(req,'index.html',{'title':"青特钢大数据项目组数据管理--检索结果"})

def about(req):

	return render(req,'about.html',{'title':"关于项目"})


def data_import(req):
	filepath = 'F:\\development\\python\\data_exchange\\数据迁移中间表1.xlsx'
	util.batch_import_data(filepath,models.TransRelation)
	records=models.TransRelation.objects.direct_select_query_sqlVO({'sql':'select * from {0}'.format(models.TransRelation._meta.db_table)})

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
		util.BaseManage.generic_query(sql_select)
		#先通过uid获取元素
		sql_insert= 'INSERT INTO {0} (own_col) values({1})'.format(each.own_table,each.own_col)

def contact(req):
	cform = forms.ContactForm()
	return render(req,'contact_form.html', {'form': cform})


def process_contact(req):
    if req.method == 'POST':
        form = forms.ContactForm(req.POST)
        if form.is_valid():
            print('收到并通过验证')
            form = forms.ContactForm(
           		initial={'subject': 'I love your site!'}
        	)
    else:
        form = forms.ContactForm(
           initial={'subject': 'I love your site!'}
        )
    return render(req,'contact_form.html', {'form': form})


def file(req):
	fform = forms.UploadFileForm()
	return render(req,'form.html', {'form': fform})   

def upload_file(req):
	print(os.path.abspath('/'))
	print(req.path)
	if req.method == 'POST':
		form = forms.UploadFileForm(req.POST, req.FILES)
		if form.is_valid():
			# print(req.FILES['file'].content_type)
			# handle_uploaded_file(req.FILES['file'])
			print(form.__dict__)
			return HttpResponseRedirect('/success')
	else:
		form = forms.UploadFileForm()
	return render(req,'form.html', {'form': form})

def handle_uploaded_file(f):
    destination = open(os.path.abspath('.')+'\\name.txt', 'wb+')
    print(os.path.abspath('.')+'\\name.txt')
    print('begin')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def success(req):
	return render(req,'success.html')




def process_user_register(req):
	print("进行注册处理")
	if req.method == 'POST':
		form = UserCreationForm(req.POST)
		if form.is_valid():
			print(form)
			new_user = form.save()
			print(new_user)
			return HttpResponseRedirect("/success/")
	else:
		print('here2')
		form = UserCreationForm()
	return render(req,'form.html', {'form': form})


def user_register(req):
	print('here_user_register')
	#urForm=forms.RegisterForm()
	form=UserCreationForm()

	return render(req,'form.html', {'form': form})


def user_login(req):
	print('user_login')
	form = forms.LoginForm()
	return render(req,'form.html', {'form': form})


def process_user_login(req):
	print('process_user_login')
	username = req.POST.get('username', '')
	password = req.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	print(user.__dict__)
	print(user.is_active)
	if user is not None and user.is_active:
		# Correct password, and the user is marked "active"
		auth.login(req, user)
		# Redirect to a success page.
		return HttpResponseRedirect("/success")
	else:
		# Show an error page
		return HttpResponseRedirect("/accounts/login")
	