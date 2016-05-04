from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^index', views.home),
    url(r'^search', views.search),
    url(r'^about', views.about),
	url(r'^data_import', views.data_import),
    
]