<p align="center">
    <img src="logo.jpg" width="200px" height="200px">
</p>

<div align="center">

# Bread Dog Bot

_✨基于 [Nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的 Terraria TShock QQ 机器人✨_

![Python](https://img.shields.io/badge/python-3.8.6%2B-blue)
![Nonebot2](https://img.shields.io/badge/nonebot-2.0.0-yellow)
![Go-cqhttp](https://img.shields.io/badge/go--cqhttp-1.0.0-red)
<br/>    
![GitHub](https://img.shields.io/github/license/Qianyiovo/bread_dog_bot)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Qianyiovo/bread_dog_bot?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/Qianyiovo/bread_dog_bot)


</div>

## 声明

**本项目仅用于学习，请勿用于非法用途**


## 功能

<details>
<summary>基础功能</summary>


+ 添加服务器
+ 删除服务器
+ 重置服务器列表
+ 服务器列表
+ 在线
+ 执行
+ 发送
+ 进度
</details>

<details>
<summary>绑定功能</summary>


+ 添加白名单
+ 删除白名单
+ 改绑白名单
+ 查询白名单
+ 查询服白名单
+ 重置白名单列表
</details>

<details>
<summary>管理功能</summary>


+ 添加管理员
+ 删除管理员
+ 管理员列表
</details>

<details>
<summary>玩家功能</summary>


+ 签到
+ 添加金币
+ 扣除金币
+ 设置金币
+ 玩家信息
+ 玩家背包
</details>

<details>
<summary>云黑功能</summary>


+ 云黑检测
+ 云黑信息
+ 添加云黑
+ 删除云黑
</details>

<details>
<summary>邮箱功能</summary>


+ 玩家邮箱
+ 添加邮件
+ 删除邮件
+ 发送邮件
+ 领取邮件
+ 回收邮件
</details>

<details>
<summary>抽奖功能</summary>


+ 随机抽奖
+ 奖池列表
+ 奖池
+ 添加奖池
+ 删除奖池
+ 添加奖池物品
+ 删除奖池物品
+ 奖池抽奖
</details>

<details>
<summary>排行榜功能</summary>


+ 可能写不了了
</details>


## 使用方式简览
1.安装一个适合你电脑的[Python](https://www.python.org)，建议使用3.10

必要时可以创建一个虚拟环境

2.配置你的服务器，为它开启REST并创建一个密钥，必要时可以安装项目`ServerPlugins`内的插件

3.克隆本仓库

```shell
git clone https://github.com/StarCloud-CY/bread_dog_bot.git
```

4.安装对应的模块

```shell
pip install -r requirements.txt
```

你可能需要换源并安装`Visual Build Tools`

5.配置基础文件

打开`.env.dev`文件，在列表中找到`SUPERUSERS`项，把你的QQ号填入双引号中，配置超管账户，现在你还需要配置`WHITELIST`项

![image](https://user-images.githubusercontent.com/115162925/211240568-c52e4e15-4a7b-4cb1-aa53-2e46bb9a4aaf.png)


6.运行程序

```shell
nb run
```

7.为你的机器人添加服务器，配置基本项目


## 版本要求
强烈推荐使用 Terraria v1.4.4+ (TShock5+)

云黑服务器可使用~~星云写的云黑服务器或~~[千亦的云黑服务器](https://github.com/Qianyiovo/bread_dog_blacklist_system)


## 前置插件

所有插件都可以在项目[ServerPlugins](https://github.com/Qianyiovo/bread_dog_bot/tree/main/ServerPlugins)目录下找到

<details>
<summary>Better Whitelist</summary>

**必备插件**

更好的白名单


</details>

<details>
<summary>REST API Extensions</summary>

**可选插件**

扩展了 REST API，可以获取玩家的背包、进度等信息

以下功能需要安装此插件才能正常使用
+ 玩家背包
+ 进度
</details>


## 更新日志
版本更新请参考[此处](change_log.md)


## 特别感谢

[Mrs4s](https://github.com/Mrs4s): [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[NoneBot](https://github.com/nonebot): [NoneBot2](https://github.com/nonebot/nonebot2)

<details>
<summary>以及以下朋友们！</summary>


+ BestATong 88.00 CNY
+ 迅猛龙 20.00 CNY
+ 问心 50.00 CNY

</details>
还有原作者: `Qianyiovo`

## 贡献

如果你喜欢本项目，可以请[原作者喝杯可乐](https://afdian.net/@qianyiovo)，我会继续努力的！


## 许可

本项目使用[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

意味着你可以运行本项目，并向你的用户提供服务，如后续有对本项目源码的修改，你需要向用户公开修改后的此项目的源码。
