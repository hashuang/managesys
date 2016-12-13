#使用git进行代码更新同步
##使用git维护自己的代码
我们普通文件夹就是一个工作区，git init(ls -a 查看隐藏目录)，在本地创建一个版本库，对工作区内容进行版本控制，版本库中有一个暂存区，add文件就将文件暂时缓存在暂存区，直到commit提交才会真正保存到版本库中。
###下载git，安装过程中勾选git bash
[下载地址](https://git-scm.com/downloads)
###参照廖雪峰教程配置ssh连接github，不然每次提交输入用户名和密码很麻烦
[配置ssh说明](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001374385852170d9c7adf13c30429b9660d0eb689dd43a000)

###git配置
git有3个级别的配置，当前目录，global（用户主目录），system（系统级配置文件），优先级以版本库的配置最高，依次向下。

1. git config --global user.name "xxxx xxx"  
2. git config --global user.email ccx@gmail.com
3. git config --system alias.st stauts //设置指令别名，简化指令
4. git config --system alias.ci commit
5. git config --system alias.co checkout
6. git config --system alias.br branch
7. git config --global color.ui true
8. git config -e [xxx] //打开相应级别的配置文件

###几个关键指令
1.  git add filename //将文件暂存入缓存区
2.  git commit -m '本次提交的相关说明' //此时已经把代码同步到
3.  git push remote branch //提交到某一远程仓库的某一分支
4.  git checkout -- filename  //（文件回到最后一次 git commit 或者 git add 的状态即修改后还未add，则撤销到上一次commit的状态，及add之后继续做出修改，撤销到上一次add的状态）
5.  git pull remote branch   //仅指定分枝
6.  git clone remote  //完整复制所有分支  

###其他指令
1. git grep "meg" //搜索文件内容  
2. git rev-parse --git-dir //工作区根目录  
3. git rev-parse --show-prefix //当前目录相对根目录的相对路径
4. git rev-parse --show-cdup //从当前目录会退到根目录的深度
5. git log [--stat] //查看提交日志，--stat查看文件变更详情
6. git diff [cached | staged | master | HEAD](不加参数工作区与提交任务（提交暂存区stage）的差异，添加参数显示暂存区与版本库的差异,工作区与版本库的差异)
7. git reset HEAD  //暂存区与版本库同步
8. git checkout . 或 git checkout -- //用暂存区的全部文件或指定文件替换工作区的文件，这个操作很危险，会清除工作区中未添加到暂存区的改动
9. git cheeckout HEAD. //则是一个更危险的动作，它会把工作区和暂存区的文件用版本库文件替换，所有的未提交改动都会清除。
10. git stash //保存当前工作进度
 
##结合github进行协同工作
###fork
github的fork是将别人的代码库（标记为origin）克隆到自己github的代码库（标记为clone-own），可以直接对自己账号的此仓库clone-own进行修改，但是此时的修改只影响自己账号下的clone-own，origin不发生改变；我们需要做3件事  
1. 保持与origin仓库的同步
```
git  remote -v  
git remote add upstream  (rpo you fork from)  

git fetch upstream   
git checkout master  
git merge upstream/master  
```
2. 同步后将自己的修改添加到clone-own
3. 向origin提交pull request,等待origin审核

###网站基本框架的初始代码
[网站基本框架的初始代码](https://github.com/ccxysfh/managesys)  
##操作流程，未测试
1. 在本地新建空文件夹，作为本地代码库
2. 从[网站基本框架的初始代码](https://github.com/ccxysfh/managesys)fork仓库到自己账号，获取http或ssh地址rpourl
3. 添加一个远程仓库qinggang,即自己github下fork的仓库
```
git remote add qinggang rpourl
```
4. 添加总库upstream 
```
git remote add upstream git@github.com:ccxysfh/managesys.git
```
5. 设置与远程仓库的同步
```
git fetch upstream   
git checkout master  
git merge upstream/master 
```
6. 提交到本地仓库
```
git push qinggang
```

