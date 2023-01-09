from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, GroupIncreaseNoticeEvent, Message, \
    GroupDecreaseNoticeEvent
from nonebot.typing import T_State

import config
import models.server
import utils.cloud_blacklist
import utils.server
import utils.whitelist

welcome = on_notice()


# 群友入群
@welcome.handle()  # 监听 welcome
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    qq = event.get_user_id()  # 获取新成员的id
    u_info = await bot.get_stranger_info(user_id=int(qq), no_cache=False)
    msg = f'{MessageSegment.at(qq)}\n欢迎加入{config.Group.name}~\n用户等级为{u_info["level"]}级\n请发送【服务器列表】来查看本群的所有服务器'
    await welcome.send(message=Message(msg))  # 发送消息
    result, reason = utils.cloud_blacklist.query(qq)
    if result:
        if config.Event.Welcome.kick_blacklist:
            try:
                await bot.set_group_kick(group_id=event.group_id, user_id=int(qq))
                msg = "已踢出该玩家"
            except:
                msg = "踢出失败，请设置机器人为群管理员"
        else:
            msg = "存在云黑，但未踢出"
        await welcome.finish(f"云黑检测成功！\n该玩家位于云黑名单中\n添加群：{reason[1]}\n原因：{reason[2]}\n{msg}")
    else:
        if reason == "未找到该QQ":
            await welcome.finish(f'云黑检测成功！\n该玩家未在云黑名单中，快来和大家一起玩吧！')
        else:
            await welcome.finish(f'云黑检测失败！\n{reason}')


# 群友退群
@welcome.handle()
async def h_r(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):  # event: GroupDecreaseNoticeEvent  群成员减少事件
    qq = event.get_user_id()  # 获取新成员的id
    name = await bot.get_stranger_info(user_id=int(qq), no_cache=False)
    result, player_info = utils.whitelist.GetInfo.by_qq(qq)
    if result:
        success = 0
        result, server_list = utils.server.GetInfo.all()
        for i in server_list:
            conn = models.server.Connect(i[2], i[3], i[4])
            result, reason = conn.delete_whitelist(qq)
            if result:
                success += 1
        msg = f'{name["nickname"]}({qq}) 离开了{config.Group.name}，已删除对应白名单({success}/{len(server_list)})，大家快出来送别它吧！\n'
    else:
        msg = f"{name['nickname']}({qq}) 离开了{config.Group.name}，大家快出来送别它吧！"
    await welcome.finish(message=Message(msg))  # 发送消息
