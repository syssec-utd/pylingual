from ..matcher import arc
from ..assets_updater import check_song_update, check_char_update
from ..resource_manager import assets_root
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
from os import path
from shutil import rmtree
from typing import List

async def assets_update_handler(event: MessageEvent, arg: Message=CommandArg()):
    args: List = arg.extract_plain_text().split()
    if args[0] == 'assets_update':
        if len(args) == 2:
            if args[1] == '--purge':
                if path.exists(assets_root / 'song'):
                    rmtree(assets_root / 'song')
                if path.exists(assets_root / 'char'):
                    rmtree(assets_root / 'char')
        await arc.send('正在更新，请关注控制台更新进度…')
        result_song = await check_song_update()
        result_char = await check_char_update()
        await arc.finish(MessageSegment.reply(event.message_id) + '\n'.join([f'成功更新 {len(result_song)} 张曲绘, ', f'成功更新 {len(result_char)} 张立绘']))