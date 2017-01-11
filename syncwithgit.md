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
  
##git教程——整理by chyulia
###一、git的配置教程
**1、  注册github帐户**
登录http://github.com，拥有一个自己的帐号和密码 。
**2、安装Git客户端。 (例如：Git-2.10.0-64-bit.exe)**
安装完成。 
**3、绑定你的github帐户和邮件。**
打开git Bash，弹出一个命令行shell（或在git环境下），输入：  
```     
 git config --global user.name "yourname"  （这里的yourname相当于你的一个签名，而非github的登录名。以后你提交的文档都会有这个签名） 
```
回车后继续输入：
```
git config --global user.email "youremail@xx.xxx" （这里输入的是你github的帐户邮箱）
```
**4、设置SSH** 
要在新电脑上使用git时，需要在本地创建SSH key，然后将生成的SSH key文件内容添加到github帐号上去。  
  
SSH是一种连接方式，一方面免于你总是在连接时输入用户和密码，另一方面增加安全性。简单理解是，ssh是两段很长的字符串，一段是锁，另一段是钥匙。你把锁放在你的github帐户上，而电脑上留有你的钥匙，每当连接时，git会自动用钥匙去开锁。  

使用流程 ：
第一步：生成钥匙和锁   
在命令行输入：  
```
ssh-keygen -t rsa -C  “your_email@youremail.com “
```
然后回车，期间会问你生成的文件名和passphrase，对于我这种菜鸟，我一路点回车。 （passphrase 可以设置密码）（即连续敲三次回车即可，生成的SSH key文件保存在中～/.ssh/id_rsa.pub）  
第二步：将锁放到github的帐户里   
上一步生成的文件放在了C:/Users/用户名（你的windows用户）/.ssh/文件夹中，用记事本打开其中的id_rsa.pub文件，全部内容复制。登录github网站，找到account setting。  
接着拷贝.ssh/id_rsa.pub文件内的所以内容，将它粘帖到github帐号管理中的添加SSH key界面中。
打开github帐号管理中的添加SSH key界面的步骤如下：  
```
1. 登录github
2. 点击右上方的Accounting settings图标
3. 选择 SSH key
4. 点击 Add SSH key
在出现的界面中填写SSH key的名称，填一个你自己喜欢的名称即可，然后将上面拷贝的~/.ssh/id_rsa.pub文件内容粘帖到key一栏，在点击“add key”按钮就可以了。
添加过程github会提示你输入一次你的github密码
```
第三步：测试一下该SSH key  
在git Bash 中输入以下代码:
```
$ ssh -T git@github.com
```
当你输入以上代码时，会有一段警告代码，如：  
```
The authenticity of host 'github.com (207.97.227.239)' can't be established.
# RSA key fingerprint is 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48.
# Are you sure you want to continue connecting (yes/no)?
```
这是正常的，你输入 yes 回车既可。如果你创建 SSH key 的时候设置了密码，接下来就会提示你输入密码，如：  
```
Enter passphrase for key '/c/Users/Administrator/.ssh/id_rsa':
```
当然如果你密码输错了，会再要求你输入，知道对了为止。  
注意：输入密码时如果输错一个字就会不正确，使用删除键是无法更正的。  
密码正确后你会看到下面这段话，如：  
```
Hi username! You've successfully authenticated, but GitHub does not
# provide shell access.
```
如果用户名是正确的,你已经成功设置SSH密钥。如果你看到 “access denied” ，者表示拒绝访问，那么你就需要使用 https 去访问，而不是 SSH 。  
###二、使用git同步代码的步骤及代码：
**查看状态**
```
E:\managesys>git status
--查看状态
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   data_import/chyulia.py
        modified:   data_import/static/data_import/js/loadChart_chen.js
        modified:   data_import/templates/data_import/chen.html

no changes added to commit (use "git add" and/or "git commit -a")
```
**选择要上传的自己改动过的文件**
```
E:\managesys>git add  data_import/chyulia.py  data_import/static/data_import/js/loadChart_chen.js  data_import/templates/data_import/chen.html
--选择要上传的自己改动过的文件 
```
**将不需要上传的文件取消掉**
```
E:\managesys>git checkout -- data_import/templates/data_import/hashuang.html
--将不需要上传的文件取消掉（可选，非必须）
```
**更准确来说checkout -- filename的是撤销修改，即add还未commit的文件，回退到上一次的add状态,还未add的文件则回退到上一次commit的状态**
  
**提交时必须添加注释**
```
E:\managesys>git commit -m "实现echarts图表的联动，点击第一个输入或产出图中的柱状，联动产生第二个图中该炉次指定字段的正态分布趋势及所在位置点"
--添加注释，尽量写清自己的改动内容（注意commit与-m之间是有空格的）
[master 1894f34] 实现echarts图表的联动，点击第一个输入或产出图中的柱状，联动产生第二个图中该炉次指定字段的正态分布趋势及所在位置点
 3 files changed, 409 insertions(+), 47 deletions(-)
```
**从管理员的github里面获取最新的程序**
```
E:\managesys>git fetch upstream master
-- 从管理员的github里面获取最新的程序
remote: Counting objects: 100, done.
remote: Compressing objects: 100% (37/37), done.
remote: Total 100 (delta 68), reused 86 (delta 54), pack-reused 0
Receiving objects: 100% (100/100), 11.36 KiB | 0 bytes/s, done.
Resolving deltas: 100% (68/68), completed with 14 local objects.
From github.com:ccxysfh/managesys
 * branch            master     -> FETCH_HEAD
   adc2197..1561299  master     -> upstream/master
```
**在本地仓库和远程主仓库合并**
```
E:\managesys>git merge upstream/master
-将自己的程序上传到自己的github账户
Already up-to-date.
```
**再次查看状态**
```
E:\managesys>git status
--再次查看状态
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)
nothing to commit, working tree clean  
```
**将修改上传到自己的github**
```
E:\managesys>git push origin master
--将修改上传到自己的github
Counting objects: 11, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (9/9), done.
Writing objects: 100% (11/11), 6.50 KiB | 0 bytes/s, done.
Total 11 (delta 7), reused 0 (delta 0)
remote: Resolving deltas: 100% (7/7), completed with 7 local objects.
To https://github.com/chyulia/managesys.git
   0880f6c..1894f34  master -> master
--到此提交至自己的github账户已完成，可在github网页中可向总管理员发起提交请求
```
-------------------------------------------------------------------------------
###三、一些附加功能
**为冗长的仓库ssh url添加别称**
```
E:\managesys>git remote add qinggang git@github.com:chyulia/managesys.git
--修改我的github的文件夹的名字，在下次使用时，就可以用qinggang这个名字来代替整个网址。
(目前项目中我的github账户分支为默认的origin)
  
E:\managesys>git remote add upstream git@github.com:ccxysfh/managesys.git
---将远程的这个github地址在本地取名为upstream，下次使用时，直接使用upstream这个名字即可代表这个地址
```
**查看提交（commit）记录**
```
E:\managesys>git log
--查看提交（commit）记录
```
**查看远程git的所有配置**
```
E:\managesys>git remote –v
--查看远程git的所有配置
origin  https://github.com/chyulia/managesys.git (fetch)
origin  https://github.com/chyulia/managesys.git (push)
upstream        git@github.com:ccxysfh/managesys.git (fetch)
upstream        git@github.com:ccxysfh/managesys.git (push)
```
