from django.conf.urls import url
from . import views

urlpatterns = [
    #需要对相同业务的加载与处理写一个分发器
    url(r'^$', views.home),
    url(r'^index', views.home),
    #用户登录
    url(r'^login',views.user_login),
    #用户注册
    url(r'^register', views.user_register),
    #用户登出
    url(r'^logout',views.user_logout),
    #修改密码
    url(r'^modify_password', views.modify_password),
  
    url(r'^data_import', views.data_import),
    # url(r'^multikey_data_import', views.multikey_data_import),
    #文件
    url(r'^upload_file',views.upload_file),
    url(r'^load_procedure_name',views.load_procedure_name),
    url(r'^ana_data_lack',views.ana_data_lack),
    url(r'^download_file',views.download_file),
    
    #重置密码
    url(r'^reset_password',views.reset_password),
    url(r'^success',views.success),
    #
    url(r'^ajaxtest',views.ajaxtest),
    #功能测试
    url(r'^delete',views.delete_records),
    url(r'^functionDemo',views.functionDemo),

    #echarts展示示例
    url(r'^echarts',views.echarts),

    url(r'^ha', views.ha),
    url(r'^num',views.num),
    url(r'^lond_to',views.lond_to),
    url(r'^lond_to_B',views.lond_to_B)

    #钢铁价格预测
    url(r'^steelprice',views.steelprice)

]