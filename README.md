# managesys
##使用Django搭建的数据管理系统
###提供数据整合，分析，以及分析结果展示

###项目启动之前需要安装oracle client以连接oracle数据库，需要下载相应的basic和sdk，之后pip install cx_Oracle
###http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html

###Setting up Django and your web server with uWSGI and nginx
###https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
```
pip install uwsgi  
将项目配置写入mysite_uwsgi.ini中，本项目参考uwsgi.ini  
uwsgi --ini mysite_uwsgi.ini  

网站的配置文件与nginx的配置文件连接，使nginx可以读取到相关配置  
sudo ln -s /home/maksim/venv/qinggang/managesys/managesys_nginx.conf  /etc/nginx/sites-enabled/  
Restart nginx:  
sudo /etc/init.d/nginx restart  
```

##fork代码并更新
```
git  remote -v  
git remote add upstream  (rpo you fork from)  

git fetch upstream   
git checkout master  
git merge upstream/master  
```