#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiAFKBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiAFKBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

from typing import Union
from datetime import datetime, timedelta
from Yukki import cleanmode, app, botname
from Yukki.database import is_cleanmode_on
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["ثانية", "دقيقه", "ساعة", "يومًا"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=5),
    }
    cleanmode[chat_id].append(put)


async def auto_clean():
    while not await asyncio.sleep(30):
        try:
            for chat_id in cleanmode:
                if not await is_cleanmode_on(chat_id):
                    continue
                for x in cleanmode[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        except:
                            continue
                    else:
                        continue
        except:
            continue


asyncio.create_task(auto_clean())


RANDOM = [
    "https://te.legra.ph/file/372bde2718e1bada3fa13.jpg",
    "https://te.legra.ph/file/c6522aabb7e39c354e9e3.jpg",
    "https://te.legra.ph/file/739662cda3c6d0c7bff1f.jpg",
    "https://te.legra.ph/file/867f5a8e6975a7b2c5a3a.jpg",
    "https://te.legra.ph/file/cb0b3217cd19e7ebf1243.jpg",
    "https://te.legra.ph/file/867f5a8e6975a7b2c5a3a.jpg",
    "https://telegra.ph//file/3b59b15e1914b4fa18b71.jpg",
    "https://telegra.ph//file/efb26cc17eef6fe82d910.jpg",
    "https://telegra.ph//file/ab4925a050e07b00f63c5.jpg",
    "https://telegra.ph//file/d169a77fd52b46e421414.jpg",
    "https://telegra.ph//file/dab9fc41f214f9cded1bb.jpg",
    "https://telegra.ph//file/e05d6e4faff7497c5ae56.jpg",
    "https://telegra.ph//file/1e54f0fff666dd53da66f.jpg",
    "https://telegra.ph//file/18e98c60b253d4d926f5f.jpg",
    "https://telegra.ph//file/b1f7d9702f8ea590b2e0c.jpg"
]


HELP_TEXT = f"""مرحبا بك لـ {botname}مركز المساعدة.

- عندما يذكرك شخص ما في محادثة ، سيتم إعلام المستخدم بأنك في وضع عدم الاتصال . يمكنك أيضًا تقديم سبب لعدم اتصالك ، والذي سيتم توفيره للمستخدم أيضًا.


/AFK - سيؤدي ذلك إلى وضعك في وضع عدم الاتصال.

/AFK [سبب] - سيؤدي ذلك إلى وضعك في وضع عدم الاتصال لسبب ما.

/AFK [رد على ملصق / صورة] - سيؤدي هذا إلى تعيينك في وضع عدم الاتصال بصورة أو ملصق.

/AFK [تم الرد على ملصق / صورة] [السبب] - هذا سوف يجعلك غير متصل مع ارسال صورة معينه وكتابة السبب


/setting - لتغيير أو تعديل الإعدادات الأساسية للبوت.‌‌
"""

def settings_markup(status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="🔄 الوضع النظيف", callback_data="cleanmode_answer"),
            InlineKeyboardButton(
                text="✅ تفعيل" if status == True else "❌ تعطيل",
                callback_data="CLEANMODE",
            ),
        ],
        [
            InlineKeyboardButton(text="🗑 غلق القائمة", callback_data="اغلاق"),
        ],
    ]
    return buttons
