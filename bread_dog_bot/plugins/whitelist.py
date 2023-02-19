from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.permission import SUPERUSER
import models.server
import utils.server
import utils.admin
import utils.whitelist
import config
from utils.msg_whitelist import in_whitelist

add_whitelist = on_command("添加白名单")


@add_whitelist.handle()
async def add_whitelist_handle(bot: Bot, event: Event):
    if in_whitelist(event):
        logger.info(f"「{event.get_user_id()}」执行了 「添加白名单」")
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            if config.Whitelist.method == "normal":  # 普通模式
                player_name = text[1]
                if not player_name.isalnum():
                    await add_whitelist.finish("添加失败！\n不合法的名称\n名称只能包含中文字母数字")
                result, server_info_list = utils.server.GetInfo.all()
                msg = []
                if result:
                    if server_info_list:
                        result, player_info = utils.whitelist.GetInfo.by_qq(event.get_user_id())
                        if result:
                            msg.append(f'警告：你正在重新添加白名单，将使用"{player_info[2]}"添加白名单')
                        max_servers = len(server_info_list)
                        success_server = 0
                        failed_server = 0
                        for i in server_info_list:
                            conn = models.server.Connect(i[2], i[3], i[4])
                            result, reason = conn.add_whitelist(event.get_user_id(), player_name)
                            if result:
                                success_server += 1
                            else:
                                msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                           f"{reason}")
                                failed_server += 1
                        error_msg = "\n".join(msg)
                        await add_whitelist.finish(Message(
                            f"--添加白名单--\n共{max_servers}个服务器，成功{success_server}个，失败{failed_server}个\n{error_msg}"))
                    else:
                        await add_whitelist.finish(Message("添加失败！\n没有添加服务器！"))
                else:
                    await add_whitelist.finish(Message("添加失败！\n无法连接至数据库"))
            elif config.Whitelist.method == "cluster":  # 集群模式
                main_server_id = config.Whitelist.main_server
                player_name = text[1]
                result, server_info = utils.server.GetInfo.by_id(main_server_id)
                if result:
                    conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
                    result, reason = conn.add_whitelist(event.get_user_id(), player_name)
                    if result:
                        await add_whitelist.finish("添加成功！")
                    else:
                        await add_whitelist.finish("添加失败！\n" + reason)
                else:
                    await add_whitelist.finish(Message("添加失败！\n无法连接至数据库"))
            else:
                await add_whitelist.finish(Message("添加失败！\n未知的模式\n请在config.py中重新配置"))
        else:
            await add_whitelist.finish("添加失败！\n用法错误！\n请输入【帮助 添加白名单】获取该功能更多信息")


# rebind_whitelist = on_command("改绑白名单")
#
#
# @rebind_whitelist.handle()
# async def rebind_whitelist_handle(bot: Bot, event: Event):
#     logger.info(f"「{event.get_user_id()}」执行了 「改绑白名单」")
#     admin_list = utils.admin.get()
#     if event.get_user_id() in admin_list:
#         text = event.get_plaintext().split(" ")
#         if len(text) == 3:
#             player_name = text[2]
#             qq = text[1]
#             result, reason = utils.whitelist.GetInfo.by_qq(qq)
#             if result:
#                 if not player_name.isalnum():
#                     await rebind_whitelist.finish("改绑失败！\n不合法的名称\n名称只能包含中文字母数字")
#                 #
#                 msg = ""
#                 success_server = 0
#                 if config.Whitelist.method == "normal":  # 普通模式
#                     result, server_info_list = utils.server.GetInfo.all()
#                     error_msg = []
#                     if result:
#                         if server_info_list:
#                             max_servers = len(server_info_list)
#                             failed_server = 0
#                             for i in server_info_list:
#                                 result, reason = utils.whitelist.delete_from_server(i[2], i[3], i[4], reason[2])
#                                 if result:
#                                     success_server += 1
#                                 else:
#                                     error_msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
#                                                f"{reason}")
#                                     failed_server += 1
#                             error_msg = "\n".join(error_msg)
#                             msg = f"共{max_servers}个服务器，成功{success_server}个，失败{failed_server}个\n{error_msg}"
#                         else:
#                             await rebind_whitelist.finish(Message("删除失败！\n没有可用的服务器！"))
#                     else:
#                         await rebind_whitelist.finish(Message("删除失败！\n无法连接至数据库"))
#                 elif config.Whitelist.method == "cluster":  # 集群模式
#                     main_server_id = config.Whitelist.main_server
#                     result, server_info = utils.server.GetInfo.by_id(main_server_id)
#                     if result:
#                         result, reason = utils.whitelist.delete_from_server(server_info[2], server_info[3], server_info[4], reason[2])
#                         if result:
#                             success_server = 1
#                             msg = "白名单删除成功！"
#                         else:
#                             await rebind_whitelist.finish("删除失败！\n" + reason)
#                     else:
#                         await rebind_whitelist.finish(Message("删除失败！\n无法连接至数据库"))
#                 else:
#                     await rebind_whitelist.finish(Message("删除失败！\n未知的模式\n请在config.py中重新配置"))
#                 #
#                 if success_server:
#                     result, reason = utils.whitelist.rebind_db(qq, player_name)
#                     if result:
#                         await rebind_whitelist.finish(f"改绑成功，之前的白名单已被移除，请重新添加白名单\n{msg}")
#                     else:
#                         if reason == "不存在此玩家":
#                             await rebind_whitelist.finish(f"改绑失败！\n删除白名单成功但无法找到你的白名单\n可能是内部错误导致的\n{msg}")
#                         else:
#                             await rebind_whitelist.finish(f"改绑失败！\n无法连接到数据库\n{reason}\n{msg}")
#                 else:
#                     await rebind_whitelist.finish(f"改绑失败！\n无法删除对应的服务器白名单\n{msg}")
#             else:
#                 if reason == "不存在此玩家":
#                     await rebind_whitelist.finish(f"改绑失败！\n你还没有添加白名单")
#                 else:
#                     await rebind_whitelist.finish(f"改绑失败！\n无法连接到数据库\n{reason}")
#         else:
#             await rebind_whitelist.finish("改绑失败！\n用法错误！\n请输入【帮助 改绑白名单】获取该功能更多信息")
#     else:
#         await rebind_whitelist.finish("删除失败！\n权限不足！\n请输入【帮助 改绑白名单】获取该功能更多信息")


delete_whitelist = on_command("删除白名单")


@delete_whitelist.handle()
async def delete_whitelist_handle(bot: Bot, event: Event):
    if in_whitelist(event):
        logger.info(f"「{event.get_user_id()}」执行了 「删除白名单」")
        admin_list = utils.admin.get()
        if event.get_user_id() in admin_list:
            text = event.get_plaintext().split(" ")
            if len(text) == 2:
                if config.Whitelist.method == "normal":  # 普通模式
                    qq = text[1]
                    result, server_info_list = utils.server.GetInfo.all()
                    msg = []
                    if result:
                        if server_info_list:
                            success_server = 0
                            failed_server = 0
                            for i in server_info_list:
                                conn = models.server.Connect(i[2], i[3], i[4])
                                result, reason = conn.delete_whitelist(qq)
                                if result:
                                    success_server += 1
                                else:
                                    msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                               f"删除失败！\n"
                                               f"{reason}")
                                    failed_server += 1
                            await delete_whitelist.finish(Message(
                                f"--删除白名单--\n共{len(server_info_list)}个服务器，成功{success_server}个，失败{failed_server}个" + (
                                    ("\n" + "\n".join(msg)) if msg else "")))
                        else:
                            await delete_whitelist.finish(Message("删除失败！\n没有可用的服务器！"))
                    else:
                        await delete_whitelist.finish(Message("删除失败！\n无法连接至数据库"))
                elif config.Whitelist.method == "cluster":  # 集群模式
                    main_server_id = config.Whitelist.main_server
                    qq = text[1]
                    result, server_info = utils.server.GetInfo.by_id(main_server_id)
                    if result:
                        conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
                        result, reason = conn.delete_whitelist(qq)
                        if result:
                            await delete_whitelist.finish("删除成功！")
                        else:
                            await delete_whitelist.finish("删除失败！\n" + reason)
                    else:
                        await delete_whitelist.finish(Message("删除失败！\n无法连接至数据库"))
                else:
                    await delete_whitelist.finish(Message("删除失败！\n未知的模式\n请在config.py中重新配置"))
            else:
                await delete_whitelist.finish("删除失败！\n用法错误！\n请输入【帮助 删除白名单】获取该功能更多信息")

        else:
            await delete_whitelist.finish("删除失败！\n权限不足！\n请输入【帮助 删除白名单】获取该功能更多信息")


reset = on_command("重置白名单", permission=SUPERUSER)


@reset.handle()
async def reset_handle(bot: Bot, event: Event):
    if in_whitelist(event):
        logger.info(f"「{event.get_user_id()}」执行了 「重置白名单」")
        result, reason = utils.whitelist.reset()
        if result:
            await reset.finish("重置成功！\n已重置数据库中的白名单")
        else:
            await reset.finish("重置失败！\n" + reason)
