#使用git进行代码更新同步
##使用git维护自己的代码
我们普通文件夹就是一个工作区，git init，在本地创建一个版本库，对工作区内容进行版本控制，版本库中有一个暂存区，add文件就将文件暂时缓存在暂存区，知道commit提交才会真正保存到版本库中。
###下载git，安装过程中勾选git bash
[下载地址](https://git-scm.com/downloads)
###参照廖雪峰教程配置ssh连接github，不然每次提交输入用户名和密码很麻烦
[配置ssh说明](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001374385852170d9c7adf13c30429b9660d0eb689dd43a000)
###几个关键指令
1.  git add filename //将文件暂存入缓存区
2.  git commit -m '本次提交的相关说明' //此时已经把代码同步到
3.  git push remote branch //提交到某一远程仓库的某一分支

##结合github进行协同工作
###fork
github的fork是将别人的代码库（标记为origin）克隆到自己github的代码库（标记为clone-own），可以直接对自己账号的此仓库clone-own进行修改，但是此时的修改只影响自己账号下的clone-own，origin不发生改变；我们需要做3件事情. 
1. 保持与origin仓库的同步
2. 同步后将自己的修改添加到clone-own
3. 向origin提交pull request,等待origin审核

###网站基本框架的初始代码
[网站基本框架的初始代码](https://github.com/ccxysfh/managesys)
