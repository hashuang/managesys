from django.conf.urls import url
from . import views

urlpatterns = [
    #需要对相同业务的加载与处理写一个分发器
    url(r'^$', views.home),
    url(r'^index', views.home),
    #用户登录
    url(r'^login',views.user_login),
    url(r'^process_login',views.process_user_login),
    #用户注册
    url(r'^register', views.user_register),
    url(r'^process_register',views.process_user_register),
    #用户注册
    url(r'^logout',views.user_logout)
    url(r'^search', views.search),
    url(r'^about', views.about),
    url(r'^data_import', views.data_import),
    url(r'^contact', views.contact),
    url(r'^process_contact',views.process_contact),
    url(r'^file',views.file),
    url(r'^upload_file',views.upload_file),
    url(r'^success',views.success),
   
]