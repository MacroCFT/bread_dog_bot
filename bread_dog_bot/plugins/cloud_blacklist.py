from nonebot import on_command, logger  # , on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
# from nonebot.adapters.onebot.v11.exception import ApiNotAvailable

import utils.admin
import utils.cloud_blacklist
import utils.msg_whitelist

# import config

cloud_blacklist_detection = on_command("云黑检测")


@cloud_blacklist_detection.handle()
async def cloud_blacklist_detection_handle(bot: Bot, event: GroupMessageEvent):
    if event.get_plaintext() == "云黑检测":
        logger.info(f"「{event.get_user_id()}」执行了 「云黑检测」")
        admins = utils.admin.get()
        if event.get_user_id() in admins:
            member_list = await bot.get_group_member_list(group_id=event.group_id)
            member_qq = []
            for i in member_list:
                member_qq.append(str(i["user_id"]))
            result, blacklist = utils.cloud_blacklist.detect(member_qq)
            if result:
                if not blacklist:
                    await cloud_blacklist_detection.finish(f"检测成功！\n群内暂时无云黑用户\n继续保持哦")
                else:
                    await cloud_blacklist_detection.finish(f"检测成功！\n以下是群内云黑用户：\n" + "\n".join(blacklist))
            else:
                if blacklist == "权限验证失败":
                    blacklist = "Token错误，请检查config.py文件中的token是否正确"
                await cloud_blacklist_detection.finish(f"检测失败！\n{blacklist}")
        else:
            await cloud_blacklist_detection.finish(f"检测失败！\n权限不足！\n请输入【帮助 云黑检测】获取该功能更多信息")


cloud_blacklist_kick = on_command("踢出云黑")


@cloud_blacklist_kick.handle()
async def cloud_blacklist_detection_handle(bot: Bot, event: GroupMessageEvent):
    if event.get_plaintext() == "踢出云黑":
        logger.info(f"「{event.get_user_id()}」执行了 「踢出云黑」")
        admins = utils.admin.get()
        if event.get_user_id() in admins:
            member_list = await bot.get_group_member_list(group_id=event.group_id)
            member_qq = []
            for i in member_list:
                member_qq.append(str(i["user_id"]))
            result, blacklist = utils.cloud_blacklist.detect(member_qq)
            if result:
                if not blacklist:
                    await cloud_blacklist_detection.finish(f"检测成功！\n群内暂时无云黑用户\n继续保持哦")
                else:
                    success = []
                    fail = []
                    for n in blacklist:
                        try:
                            await bot.set_group_kick(group_id=event.group_id, user_id=n)
                            success.append(n)
                        except:
                            fail.append(n)
                    await cloud_blacklist_detection.finish(f"检测成功！\n移除成功的云黑用户：\n" + "\n".join(success) + "\n移除失败的云黑用户：\n" + "\n".join(fail))
            else:
                if blacklist == "权限验证失败":
                    blacklist = "Token错误，请检查config.py文件中的token是否正确"
                await cloud_blacklist_detection.finish(f"检测失败！\n{blacklist}")
        else:
            await cloud_blacklist_detection.finish(f"检测失败！\n权限不足！\n请输入【帮助 踢出云黑】获取该功能更多信息")


add_cloud_blacklist = on_command("添加云黑")


@add_cloud_blacklist.handle()
async def add_blacklist_handle(bot: Bot, event: GroupMessageEvent):
    logger.info(f"「{event.get_user_id()}」执行了 「添加云黑」")
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            reason = text[2]
            group_id = event.group_id

            if not qq.isdigit():
                await add_cloud_blacklist.finish(f"添加失败！\n无效的参数\n请输入正确的QQ号")

            result, reason = utils.cloud_blacklist.add(qq=qq, reason=reason, group_id=str(group_id))
            if result:
                logger.info(f"「{event.get_user_id()}」添加了云黑 QQ={qq} group_id={str(group_id)} reason={result}")
                await add_cloud_blacklist.finish(f"添加成功！")
            else:
                if reason == "权限验证失败":
                    reason = "Token错误，请检查config.py文件中的token是否正确"
                await add_cloud_blacklist.finish(f"添加失败！\n{reason}")
        else:
            await add_cloud_blacklist.finish(f"添加失败！\n用法错误！\n请输入【帮助 添加云黑】获取该功能更多信息")
    else:
        await add_cloud_blacklist.finish(f"添加失败！\n权限不足！\n请输入【帮助 添加云黑】获取该功能更多信息")


del_cloud_blacklist = on_command("删除云黑")


@del_cloud_blacklist.handle()
async def del_cloud_blacklist_handle(bot: Bot, event: GroupMessageEvent):
    logger.info(f"「{event.get_user_id()}」执行了 「删除云黑」")
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            qq = text[1]

            if not qq.isdigit():
                await del_cloud_blacklist.finish(f"添加失败！\n无效的参数\n请输入正确的QQ号")

            result, reason = utils.cloud_blacklist.delete(qq=qq)
            if result:
                await del_cloud_blacklist.finish(f"删除成功！")
                logger.info(f"「{event.get_user_id()}」删除了QQ为「{qq}」的云黑")
            else:
                if reason == "权限验证失败":
                    reason = "Token错误，请检查config.py文件中的token是否正确"
                await del_cloud_blacklist.finish(f"删除失败！\n{reason}")
        else:
            await del_cloud_blacklist.finish(f"删除失败！\n用法错误！\n请输入【帮助 删除云黑】获取该功能更多信息")
    else:
        await del_cloud_blacklist.finish(f"删除失败！\n权限不足！\n请输入【帮助 删除云黑】获取该功能更多信息")


query_cloud_blacklist = on_command("云黑信息")


@query_cloud_blacklist.handle()
async def query_cloud_blacklist_handle(bot: Bot, event: GroupMessageEvent):
    logger.info(f"「{event.get_user_id()}」执行了 「云黑信息」")
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            qq = text[1]

            if not qq.isdigit():
                await query_cloud_blacklist.finish(f"添加失败！\n无效的参数\n请输入正确的QQ号")

            result, reason = utils.cloud_blacklist.query(qq=qq)
            if result:
                await query_cloud_blacklist.finish(f"查询成功！\nQQ：{reason[0]}\n添加群号：{reason[1]}\n原因：{reason[2]}")
            else:
                await query_cloud_blacklist.finish(f"查询失败！\n{reason}")
        else:
            await query_cloud_blacklist.finish(f"查询失败！\n用法错误！\n请输入【帮助 云黑信息】获取该功能更多信息")
    else:
        await query_cloud_blacklist.finish(f"查询失败！\n权限不足！\n请输入【帮助 云黑信息】获取该功能更多信息")

#
# detect_blacklist = on_message()
#
#
# @detect_blacklist.handle()
# async def detect_blacklist_handle(bot: Bot, event: GroupMessageEvent):
#     if config.Event.Welcome.kick_blacklist:
#         qq = event.get_user_id()
#         result, reason = utils.cloud_blacklist.query(qq=event.get_user_id())
#         if result:
#             try:
#                 await bot.set_group_kick(group_id=event.group_id, user_id=int(qq))
#                 msg = f"发现云黑用户:{qq}\n已踢出该用户"
#             except ApiNotAvailable:
#                 msg = f"发现云黑用户:{qq}\n踢出失败，请设置机器人为群管理员"
#             detect_blacklist.finish(msg)
