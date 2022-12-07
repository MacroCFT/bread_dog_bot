# 一个简陋的云黑服务器
配置文件为`config.json`
> host:str 绑定IP，一般`0.0.0.0`

> port:int 端口，默认是`5432`，建议不要改动

> token:list 可以使用的云黑token

数据库为`black_list.db`
表名:black_list
> qq 云黑用户QQ

> group 加入云黑的群组

> reason 云黑此人的理由

使用方法:
运行main.py即可(你可能需要配置Python3并安装Flask `pip install Flask`)

接下来改写Bread Dog的`config.py`，找到`CloudBlacklist`类，并把`url`变量改为`http://你服的IP:5432`，保存并开启Bread Dog Bot即可

如果报错，你可能需要新建`logs`文件夹，如果还不能启动，请把它反馈给我
