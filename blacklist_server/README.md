# 一个简陋的云黑服务器

### 此云黑服务器有更优替代方式，[>请看这里<](https://github.com/Qianyiovo/bread_dog_blacklist_system)

配置文件为`config.json`

> host:str 绑定IP，一般`0.0.0.0`

> port:int 端口，默认是`5432`，建议不要改动，除非服务器限制了端口出

> token:dict 可以使用的云黑token，格式为{"token": ["add", "del", "list"]}

<details>
<summary>权限列表</summary>

+ list 可查询云黑
+ add 可添加云黑
+ del 可删除云黑
</details>


数据库为`black_list.db`
表名:black_list
> qq 云黑用户QQ

> group 加入云黑的群组

> reason 云黑此人的理由

使用方法:
运行main.py即可(你可能需要配置Python3并安装Flask `pip install Flask`)
`Windows`下可直接运行已打包的文件 `main.exe`

接下来改写Bread Dog的`config.py`，找到`CloudBlacklist`类，并把`url`变量改为`http://你服的IP:你配置的端口`，把`token`变量改为你配置的密钥之一，保存并开启Bread Dog Bot即可
![image](https://user-images.githubusercontent.com/115162925/207231293-7c01ce47-6657-4962-99b4-bc777d72e47a.png)

如果报错，请把它连同它生成的日志反馈给我


<details>
<summary>API参考</summary>

+ /blacklist/?token=密钥,需要有list权限&qq=QQ号&qq=可添加多个&qq=也可不添加&qq=添加则返回包含这些QQ的云黑数据&qq=不包含则返回所有数据
+ /blacklist/add/?token=密钥,需要有add权限&QQ=QQ号&groupID=添加云黑的群号
+ /blacklist/delete/?token=密钥,需要有del权限&QQ=QQ号
</details>

<details>
