#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiAFKBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiAFKBot/blob/master/LICENSE >
#
# All rights reserved.

import time
import random

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

from Yukki import app, boot, botname, botusername
from Yukki.database.cleanmode import cleanmode_off, cleanmode_on, is_cleanmode_on
from Yukki.helpers import get_readable_time, put_cleanmode, settings_markup, RANDOM, HELP_TEXT


@app.on_message(filters.command(["start", "settings", "بدأ" ]) & filters.group & ~filters.edited)
async def on_start(_, message: Message):
    bot_uptime = int(time.time() - boot)
    Uptime = get_readable_time(bot_uptime)
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📜 مركز المساعدة",
                    url=f"https://t.me/{botusername}?start=help",
                ),
               
                InlineKeyboardButton(
                    text="🔧 الاعدادات",
                    callback_data="settings_callback",
                ),
            ]
        ]
    )
    
    image = random.choice(RANDOM)
    send = await message.reply_photo(image, caption=f"هلو عيني اسمي  {botname} \n\n لمعرفة المزيد عني تحقق من قسم المساعدة. نشط منذ {Uptime}", reply_markup=upl)
    await put_cleanmode(message.chat.id, send.message_id)
    

@app.on_message(filters.command(["help"]) & filters.group & ~filters.edited)
async def on_help(_, message: Message):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📜 مركز المساعدة",
                    url=f"https://t.me/{botusername}?start=help",
                ),
            ]
        ]
    )
    send = await message.reply_text("Contact me in PM for help.", reply_markup=upl)
    await put_cleanmode(message.chat.id, send.message_id)

@app.on_message(filters.command(["start"]) & filters.private & ~filters.edited)
async def on_private_start(_, message: Message):
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            return await message.reply_text(HELP_TEXT)
    else:
        bot_uptime = int(time.time() - boot)
        Uptime = get_readable_time(bot_uptime)
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="➕ اضفني لمجموعتك",
                        url=f"https://t.me/{botusername}?startgroup=true",
                    ),
                ]
            ]
        )
        image = random.choice(RANDOM)
        await message.reply_photo(image, caption=f"هلو عيني اسمي  {botname}.\n\n معرفة المزيد عني تحقق من قسم المساعدة. نشط منذ {Uptime}", reply_markup=upl)

@app.on_message(filters.command(["help"]) & filters.private & ~filters.edited)
async def on_private_help(_, message: Message):
    return await message.reply_text(HELP_TEXT)
        
@app.on_callback_query(filters.regex("close"))
async def on_close_button(client, CallbackQuery):
    await CallbackQuery.answer()
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex("cleanmode_answer"))
async def on_cleanmode_button(client, CallbackQuery):
    await CallbackQuery.answer("⁉️ ما هذا\n\nعند تفعيلها سيقوم البوت بحذف اوامره بعد خمس دقائق للمحافظة على مجموعتك نظيفة .", show_alert=True)

@app.on_callback_query(filters.regex("settings_callback"))
async def on_settings_button(client, CallbackQuery):
    await CallbackQuery.answer()
    status = await is_cleanmode_on(CallbackQuery.message.chat.id)
    buttons = settings_markup(status)
    return await CallbackQuery.edit_message_text(f"⚙️ **اعدادات البوت**\n\n🖇**المجموعة:** {CallbackQuery.message.chat.title}\n🔖**ايدي المجموعة:** `{CallbackQuery.message.chat.id}`\n\n💡**اختر الزر الذي تريد تعديله من الاسفل .**", reply_markup=InlineKeyboardMarkup(buttons),)

@app.on_callback_query(filters.regex("CLEANMODE"))
async def on_cleanmode_change(client, CallbackQuery):
    admin = await app.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    if admin.status in ["creator", "administrator"]:
        pass
    else:
        return await CallbackQuery.answer("المشرفين فقط من يمكنهم التحمم بهذا الاعداد.", show_alert=True)
    await CallbackQuery.answer()
    status = None
    if await is_cleanmode_on(CallbackQuery.message.chat.id):
        await cleanmode_off(CallbackQuery.message.chat.id)
    else:
        await cleanmode_on(CallbackQuery.message.chat.id)
        status = True
    buttons = settings_markup(status)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return
