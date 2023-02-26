from urllib import parse
from nonebot import on_startswith, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
import os
import utils.msg_whitelist
from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError

# 感谢@ACaiCat的提供的wiki代码
wiki = on_startswith(("搜索", "wiki", "Wiki", "WIKI"))


@wiki.handle()
async def wiki_(event: GroupMessageEvent):
    if utils.msg_whitelist.in_whitelist(event):
        logger.info(f"「{event.get_user_id()}」执行了 「wiki」")
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            msg = event.get_plaintext().replace("搜索", "").replace("wiki", "").replace("Wiki", "").replace("WIKI", "").replace(
                " ", "")
            await wiki.send(
                f"\n已从Wiki上帮你找到【{msg}】\nhttps://terraria.wiki.gg/zh/wiki/Special:%E6%90%9C%E7%B4"
                f"%A2?search={parse.quote(msg)}\n正在加载网页图片...", at_sender=True)
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.goto(f"https://terraria.wiki.gg/zh/wiki/Special:%E6%90%9C%E7%B4%A2?"
                                    f"search={parse.quote(msg)}", timeout=60000)
                    await page.get_by_role("button", name="确定").click()
                    await page.screenshot(path=r'./img/wiki.png', full_page=True, omit_background=True)
                    await browser.close()
                if os.name == "nt":  # windows
                    await wiki.finish(MessageSegment.image("file:///" + os.getcwd() + "\\img\\wiki.png"))
                else:  # linux
                    await wiki.finish(MessageSegment.image("file://" + os.getcwd() + "/img/wiki.png"))
            except TimeoutError:
                await wiki.finish("访问网站超时，图片请求取消")
            except FileNotFoundError:
                await wiki.finish("图片不存在，这应该是内部错误导致的")
        else:
            await wiki.finish("\n搜索失败！\n搜索内容不能为空！\n请输入【帮助 wiki】获取该功能更多信息", at_sender=True)
