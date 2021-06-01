import os
import json
import time
import asyncio

from asyncio.exceptions import TimeoutError

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)


API_TEXT = """🙋‍♂ 𝐇𝐢 {},
I am a String Session Generatoe Bot

[🖥️How To Get UserSession For Website🖥️](https://youtu.be/WUN_12-dYOM)

Any Doubt @Mo_Tech_Group

For Ganerating String Session Send Me Your `API_ID` 🐿
"""

     buttons = [[
        InlineKeyboardButton('🖥️Tutorial Video🖥️', url='https://youtu.be/WUN_12-dYOM'),
        ],[
        InlineKeyboardButton('📕 About', callback_data='about'),
        InlineKeyboardButton('Close ❌️', callback_data='help')
    ]]
    if cb:
        await m.answer()
        await m.message.edit(text=api_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    else:
        await m.reply_text(text=api_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)
 

HASH_TEXT = "𝐎𝐤, 𝐍𝐨𝐰 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 `API_HASH` 𝐓𝐨 𝐂𝐨𝐧𝐭𝐢𝐧𝐮𝐞.\n\n𝐏𝐫𝐞𝐬𝐬 /cancel 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥.🐧"
PHONE_NUMBER_TEXT = (
    "📞𝐍𝐨𝐰 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝐏𝐡𝐨𝐧𝐞 𝐍𝐮𝐦𝐛𝐞𝐫 𝐓𝐨 𝐂𝐨𝐧𝐭𝐢𝐧𝐮𝐞"
    "𝐈𝐧𝐜𝐥𝐮𝐝𝐞 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 𝐂𝐨𝐝𝐞.\n**Eg:** `+911234567890`\n\n"
    "𝐏𝐫𝐞𝐬𝐬 /cancel 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥."
)



@Client.on_message(filters.private & filters.command("start"))
async def generate_str(c, m):
    get_api_id = await Client.ask(
        self=c,
        chat_id=m.chat.id,
        text=API_TEXT.format(m.from_user.mention(style='md')),
        filters=filters.text
    )
    api_id = get_api_id.text
    if await is_cancel(m, api_id):
        return

    await get_api_id.delete()
    await get_api_id.request.delete()
    try:
        check_api = int(api_id)
    except Exception:
        await m.reply("**🛑 𝐀𝐏𝐈 𝐈𝐃 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 🛑**\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return

    get_api_hash = await Client.ask(
        self=c,
        chat_id=m.chat.id, 
        text=HASH_TEXT,
        filters=filters.text
    )
    api_hash = get_api_hash.text
    if await is_cancel(m, api_hash):
        return

    await get_api_hash.delete()
    await get_api_hash.request.delete()

    if not len(api_hash) >= 30:
        await m.reply("🛑 𝐀𝐏𝐈 𝐇𝐀𝐒𝐇 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 🛑\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return

    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await c.send_message(m.chat.id ,f"🛑 𝐄𝐑𝐑𝐎𝐑 🛑 `{str(e)}`\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return

    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    while True:
        get_phone_number = await Client.ask(
            self=c,
            chat_id=m.chat.id,
            text=PHONE_NUMBER_TEXT
        )
        phone_number = get_phone_number.text
        if await is_cancel(m, phone_number):
            return
        await get_phone_number.delete()
        await get_phone_number.request.delete()

        confirm = await Client.ask(
            self=c,
            chat_id=m.chat.id,
            text=f'🤔 𝐈𝐬 `{phone_number}` 𝐂𝐨𝐫𝐫𝐞𝐜𝐭? (y/n): \n\n𝐓𝐲𝐩𝐞👇\n👉`y` - If Yes\n👉`n` - If No'
        )
        if await is_cancel(m, confirm.text):
            return
        if "y" in confirm.text.lower():
            await confirm.delete()
            await confirm.request.delete()
            break
    try:
        code = await client.send_code(phone_number)
        await asyncio.sleep(1)
    except FloodWait as e:
        await m.reply(f"𝐒𝐨𝐫𝐫𝐲 𝐓𝐨 𝐒𝐚𝐲 𝐘𝐨𝐮 𝐓𝐡𝐚𝐭 𝐘𝐨𝐮 𝐇𝐚𝐯𝐞 𝐅𝐥𝐨𝐨𝐝𝐰𝐚𝐢𝐭 𝐨𝐟 {e.x} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 😔")
        return
    except ApiIdInvalid:
        await m.reply("🕵‍♂ 𝐓𝐡𝐞 𝐀𝐏𝐈 𝐈𝐃 𝐨𝐫 𝐀𝐏𝐈 𝐇𝐀𝐒𝐇 𝐈𝐬 𝐈𝐧𝐯𝐚𝐥𝐢𝐝.\n\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return
    except PhoneNumberInvalid:
        await m.reply("☎ 𝐘𝐨𝐮𝐫 𝐏𝐡𝐨𝐧𝐞 𝐍𝐮𝐦𝐛𝐞𝐫 𝐈𝐬 𝐈𝐧𝐯𝐚𝐥𝐢𝐝.\n\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return

    try:
        sent_type = {"app": "Telegram App 💌",
            "sms": "SMS 💬",
            "call": "Phone call 📱",
            "flash_call": "phone flash call 📲"
        }[code.type]
        otp = await Client.ask(
            self=c,
            chat_id=m.chat.id,
            text=(f"𝐈 𝐇𝐚𝐝 𝐒𝐞𝐧𝐭 𝐀𝐧 𝐎𝐓𝐏 𝐓𝐨 𝐓𝐡𝐞 𝐍𝐮𝐦𝐛𝐞𝐫‌‌ `{phone_number}` 𝐓𝐡𝐫𝐨𝐮𝐠𝐡 {sent_type}\n\n"
                  "𝐏𝐥𝐞𝐚𝐬𝐞 𝐄𝐧𝐭𝐞𝐫 𝐓𝐡𝐞 𝐎𝐓𝐏 𝐈𝐧 𝐓𝐡𝐞 𝐅𝐨𝐫𝐦𝐚𝐭 `1 2 3 4 5` __(ᴘʀᴏᴠɪᴇᴅ ᴡʜɪᴛᴇ sᴘᴀᴄᴇ ʙᴇᴛᴡᴇᴇɴ ɴᴜᴍʙᴇʀs)__\n\n"
                  "𝐈𝐟 𝐁𝐨𝐭 𝐍𝐨𝐭 𝐒𝐞𝐧𝐝𝐢𝐧𝐠 𝐎𝐓𝐏 𝐓𝐡𝐞𝐧 𝐓𝐫𝐲 /start 𝐓𝐡𝐞 𝐁𝐨𝐭.\n"
                  "𝐏𝐫𝐞𝐬𝐬 /cancel 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥."), timeout=300)
    except TimeoutError:
        await m.reply("⏰ 𝗧𝗶𝗺𝗲𝗢𝘂𝘁 𝗘𝗿𝗿𝗼𝗿: 𝐘𝐨𝐮 𝐑𝐞𝐚𝐜𝐡𝐞𝐝 𝐓𝐢𝐦𝐞 𝐋𝐢𝐦𝐢𝐭 𝐎𝐟 5 𝐌𝐢𝐧.\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return
    if await is_cancel(m, otp.text):
        return
    otp_code = otp.text
    await otp.delete()
    await otp.request.delete()
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await m.reply("**📵 Invalid Code**\n\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return 
    except PhoneCodeExpired:
        await m.reply("**⌚ Code is Expired**\n\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await Client.ask(
                self=c,
                chat_id=m.chat.id, 
                text="`🔐 𝐓𝐡𝐢𝐬 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐡𝐚𝐯𝐞 𝐭𝐰𝐨-𝐬𝐭𝐞𝐩 𝐯𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐜𝐨𝐝𝐞.\n𝐏𝐫𝐞𝐬𝐬 𝐞𝐧𝐭𝐞𝐫 𝐲𝐨𝐮𝐫 𝐬𝐞𝐜𝐨𝐧𝐝 𝐟𝐚𝐜𝐭𝐨𝐫 𝐚𝐮𝐭𝐡𝐞𝐧𝐭𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐜𝐨𝐝𝐞.\n𝐏𝐫𝐞𝐬𝐬 /𝐜𝐚𝐧𝐜𝐞𝐥 𝐭𝐨 𝐂𝐚𝐧𝐜𝐞𝐥.",
                timeout=300
            )
        except TimeoutError:
            await m.reply("**⏰ 𝗧𝗶𝗺𝗲𝗢𝘂𝘁 𝗘𝗿𝗿𝗼𝗿: 𝐘𝐨𝐮 𝐑𝐞𝐚𝐜𝐡𝐞𝐝 𝐓𝐢𝐦𝐞 𝐋𝐢𝐦𝐢𝐭 𝐎𝐟 5 𝐌𝐢𝐧.\n𝐏𝐫𝐞𝐬𝐬 /start 𝐓𝐨 𝐂𝐫𝐞𝐚𝐭𝐞 𝐀𝐠𝐚𝐢𝐧.")
            return
        if await is_cancel(m, two_step_code.text):
            return
        new_code = two_step_code.text
        await two_step_code.delete()
        await two_step_code.request.delete()
        try:
            await client.check_password(new_code)
        except Exception as e:
            await m.reply(f"**⚠️ 𝐄𝐑𝐑𝐎𝐑:** `{str(e)}`")
            return
    except Exception as e:
        await c.send_message(m.chat.id ,f"**⚠️ 𝐄𝐑𝐑𝐎𝐑:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await client.send_message("me", f"**𝐘𝐨𝐮𝐫 𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 👇**\n\n`{session_string}`\n\n💖Thanks💖For💖using💖 {(await c.get_me()).mention(style='md')}\n\n👤 Join @Mo_Tech_Group")
        text = "✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 𝐘𝐨𝐮𝐫 𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐀𝐧𝐝 𝐒𝐞𝐧𝐭 𝐓𝐨 𝐘𝐨𝐮 𝐒𝐚𝐯𝐞𝐝 𝐌𝐞𝐬𝐬𝐚𝐠𝐞𝐬.\n𝐂𝐡𝐞𝐜𝐤 𝐲𝐨𝐮𝐫 𝐒𝐚𝐯𝐞𝐝 𝐌𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐨𝐫 𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 𝐁𝐞𝐥𝐨𝐰 𝐁𝐮𝐭𝐭𝐨𝐧.\n\n𝐁𝐨𝐭 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 - **@Mo_Tech_YT**"
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 ↗️", url=f"tg://openmessage?user_id={m.chat.id}")]]
        )
        await c.send_message(m.chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await c.send_message(m.chat.id ,f"**⚠️ 𝐄𝐑𝐑𝐎𝐑:** `{str(e)}`")
        return


@Client.on_message(filters.private & filters.command("help"))
async def help(c, m):
    await help_cb(c, m, cb=False)


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m, cb=True):
    help_text = """**Hey You Need Help??👨‍✈️**


💢 𝐏𝐫𝐞𝐬𝐬 𝐓𝐡𝐞 /start 𝐁𝐮𝐭𝐭𝐨𝐧.

💢 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝙰𝙿𝙸_𝙸𝙳 𝐖𝐡𝐞𝐧 𝐁𝐨𝐭 𝐀𝐬𝐤.

💢 𝐓𝐡𝐞𝐧 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝙰𝙿𝙸_𝙷𝙰𝚂𝙷 𝐖𝐡𝐞𝐧 𝐁𝐨𝐭 𝐀𝐬𝐤.

💢 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝐌𝐨𝐛𝐢𝐥𝐞 𝐍𝐮𝐦𝐛𝐞𝐫.

💢 𝐒𝐞𝐧𝐝 𝐓𝐡𝐞 𝐎𝐓𝐏 𝐑𝐞𝐜𝐢𝐯𝐞𝐯𝐞𝐝 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐍𝐮𝐦𝐛𝐞𝐫 𝐈𝐧 𝐓𝐡𝐞 𝐅𝐨𝐫𝐦𝐚𝐭 `1 2 3 4 5` (ɢɪᴠᴇ sᴘᴀᴄᴇ ʙ/ᴡ ᴇᴀᴄʜ ᴅɪɢɪᴛ)

💢 (ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴡᴏ sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ sᴇɴᴅ ᴛᴏ ʙᴏᴛ ɪꜰ ʙᴏᴛ ᴀsᴋ.)


**NOTE:**

𝐈𝐟 𝐘𝐨𝐮 𝐌𝐚𝐝𝐞 𝐀𝐧𝐲 𝐌𝐢𝐬𝐭𝐚𝐤𝐞 𝐀𝐧𝐲𝐰𝐡𝐞𝐫𝐞 𝐏𝐫𝐞𝐬𝐬 /cancel 𝐀𝐧𝐝 𝐓𝐡𝐞𝐧 𝐏𝐫𝐞𝐬𝐬 /start
"""

    buttons = [[
        InlineKeyboardButton('🖥️Tutorial Video🖥️', url='https://youtu.be/WUN_12-dYOM'),
        ],[
        InlineKeyboardButton('📕 About', callback_data='about'),
        InlineKeyboardButton('Close ❌️', callback_data='close')
    ]]
    if cb:
        await m.answer()
        await m.message.edit(text=help_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    else:
        await m.reply_text(text=help_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)


@Client.on_message(filters.private & filters.command("about"))
async def about(c, m):
    await about_cb(c, m, cb=False)


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m, cb=True):
    me = await c.get_me()
    about_text = f"""**MY DETAILS:**

🤖 𝐌𝐲 𝐍𝐚𝐦𝐞: {me.mention(style='md')}
    
📝 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞: [ 𝐏𝐲𝐭𝐡𝐨𝐧3](https://www.python.org/)

🧰 𝐅𝐫𝐚𝐦𝐞𝐰𝐨𝐫𝐤: [𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦](https://github.com/pyrogram/pyrogram)

👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: [𝐌𝐑𝐊-𝐘𝐓](https://t.me/MRK_YT)

📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: [𝐌𝐓 𝐁𝐎𝐓 𝐒𝐔𝐏𝐏𝐎𝐑𝐓](https://t.me/MO_TECH_YT)

🌐 𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞: [𝐏𝐫𝐞𝐬𝐬 𝐌𝐞 😋](https://github.com/MRK-YT/MT-UserSession-Bot)

🚀 𝐘𝐨𝐮𝐓𝐮𝐛𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: [𝐌𝐓 𝐁𝐎𝐓](https://youtube.com/channel/UCmGBpXoM-OEm-FacOccVKgQ)
"""

     buttons = [[
        InlineKeyboardButton('💡 𝗛𝗲𝗹𝗽', callback_data='help'),
        InlineKeyboardButton('❌ 𝗖𝗹𝗼𝘀𝗲', callback_data='close')
    ]]
    if cb:
        await m.answer()
        await m.message.edit(about_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    else:
        await m.reply_text(about_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)


@Client.on_callback_query(filters.regex('^close$'))
async def close(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("⛔ 𝐏𝐫𝐨𝐜𝐞𝐬𝐬 𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝.")
        return True
    return False


