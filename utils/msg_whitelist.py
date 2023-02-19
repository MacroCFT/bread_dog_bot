from pydantic import BaseModel, Extra
from typing import Union
from nonebot import get_driver
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Event, PrivateMessageEvent, GroupMessageEvent, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent


class Config(BaseModel, extra=Extra.ignore):
    whitelist: dict[str, list] = {"private": [], "group": []}


def get_whitelist_list():
    try:
        whitelist = dict(get_driver().config.whitelist)
    except AttributeError:
        logger.error("私聊群聊白名单未配置或有误！")
        return [], []
    try:
        private = whitelist["private"]
        group = whitelist["group"]
        if isinstance(private, list) and isinstance(group, list):
            return private, group
        else:
            logger.error("私聊群聊白名单格式有误！")
            return [], []
    except AttributeError:
        logger.error("私聊群聊白名单格式有误！")
        return [], []


def in_whitelist(event: Union[Event, PrivateMessageEvent, GroupMessageEvent, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent]):
    private, group = get_whitelist_list()
    if isinstance(event, PrivateMessageEvent):
        logger.info("接收到私聊消息")
        if event.get_user_id() in private:
            return True
        else:
            return False
    elif isinstance(event, GroupMessageEvent):
        logger.info("接受到群聊消息")
        if event.group_id in group:
            return True
        else:
            return False
    elif isinstance(event, GroupIncreaseNoticeEvent):
        logger.info("接受到入群消息")
        if event.group_id in group:
            return True
        else:
            return False
    elif isinstance(event, GroupDecreaseNoticeEvent):
        logger.info("接受到离群消息")
        if event.group_id in group:
            return True
        else:
            return False
    else:
        logger.info("接受到其他消息")
        return True
