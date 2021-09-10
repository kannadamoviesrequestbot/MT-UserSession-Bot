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


API_TEXT = """🙋‍♂ **Hi {},**
**I am a String Session generator bot.**
**For generating string session send me your** `API_ID` 🐿

**👇JOIN MY CHANNEL👇**

👉 **[JOIN MY CHANNEL](https://t.me/KANNADAMOVIES_17)

👉 [JOIN MY GROUP](https://t.me/searchkannadamovies)**

**👤THIS IS MADE BY❤ @BAGURUJOINAGUUKANNADAMOVIES_17**

**🤔Any Help**  /help

**🤖About Bot** /about
"""

HASH_TEXT = "**Ok Now Send your** `API_HASH` **to Continue.\n\nPress /cancel to Cancel.🐧**"
PHONE_NUMBER_TEXT = (
    "**📞Now send your Phone number to Continue**"
    "**include Country code.**\n\n**Eg:** `+9112345678910`\n\n"
    "**Press /cancel to Cancel😔.**"
)



@Client.on_message(filters.private & filters.command("start"))
async def generate_str(c, m):
    get_api_id = await c.ask(
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
        await m.reply("**--😜 API ID Invalid 🤣--**\n**Press /start to create again😔**.")
        return

    get_api_hash = await c.ask(
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
        await m.reply("--**😜 API HASH Invalid 🤣**--\n**Press /start to create again.**😔")
        return

    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await c.send_message(m.chat.id ,f"**🤣 ERROR: 😜** `{str(e)}`\nPress /start to create again.")
        return

    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    while True:
        get_phone_number = await c.ask(
            chat_id=m.chat.id,
            text=PHONE_NUMBER_TEXT
        )
        phone_number = get_phone_number.text
        if await is_cancel(m, phone_number):
            return
        await get_phone_number.delete()
        await get_phone_number.request.delete()

        confirm = await c.ask(
            chat_id=m.chat.id,
            text=f'🤔 Is `{phone_number}` correct? (y/n): \n\n👇type:👇\n👉`Y` - If Yes\n👉`N` - If No'
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
        await m.reply(f"__Sorry to say you that you have floodwait of {e.x} Seconds 😞__")
        return
    except ApiIdInvalid:
        await m.reply("🕵‍♂ The API ID or API HASH is Invalid.\n\nPress /start to create again.")
        return
    except PhoneNumberInvalid:
        await m.reply("☎ Your Phone Number is Invalid.`\n\nPress /start to create again.")
        return

    try:
        sent_type = {"app": "Telegram App 💌",
            "sms": "SMS 💬",
            "call": "Phone call 📱",
            "flash_call": "phone flash call 📲"
        }[code.type]
        otp = await c.ask(
            chat_id=m.chat.id,
            text=(f"I had sent an OTP to the number `{phone_number}` through {sent_type}\n\n"
                  "Please enter the OTP in the format `1 2 3 4 5` __(provied white space between numbers)__\n\n"
                  "If Bot not sending OTP then try /start the Bot.\n"
                  "Press /cancel to Cancel."), timeout=300)
    except TimeoutError:
        await m.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /start to create again.")
        return
    if await is_cancel(m, otp.text):
        return
    otp_code = otp.text
    await otp.delete()
    await otp.request.delete()
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await m.reply("**📵 Invalid Code**\n\nPress /start to create again.")
        return 
    except PhoneCodeExpired:
        await m.reply("**⌚ Code is Expired**\n\nPress /start to create again.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await c.ask(
                chat_id=m.chat.id, 
                text="`🔐 This account have two-step verification code.\nPlease enter your second factor authentication code.`\nPress /cancel to Cancel.",
                timeout=300
            )
        except TimeoutError:
            await m.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /start to create again.")
            return
        if await is_cancel(m, two_step_code.text):
            return
        new_code = two_step_code.text
        await two_step_code.delete()
        await two_step_code.request.delete()
        try:
            await client.check_password(new_code)
        except Exception as e:
            await m.reply(f"**⚠️ ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await c.send_message(m.chat.id ,f"**⚠️ ERROR:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await client.send_message("me", f"**Your String Session 👇**\n\n`{session_string}`\n\n**Thanks For using**\n\n**👤Any Doubt @KANNADAMOVIES_17** {(await c.get_me()).mention(style='md')}")
        text = "**✅ Successfully Generated Your String Session and sent to you saved messages.\nCheck your saved messages or Click on Below Button.**\n\n**MOVIES Updates @KANNADAMOVIES_17**"
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="String Session ↗️", url=f"tg://openmessage?user_id={m.chat.id}")]]
        )
        await c.send_message(m.chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await c.send_message(m.chat.id ,f"**⚠️ ERROR:** `{str(e)}`")
        return


@Client.on_message(filters.private & filters.command("help"))
async def help(c, m):
    await help_cb(c, m, cb=False)


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m, cb=True):
    help_text = """**Hey You need Help??👨‍✈️**

**>>>> press the start button\n
>>>> Send Your API_ID when bot ask.\n
>>>> Then send your API_HASH when bot ask.\n
>>>> Send your mobile number.\n
>>>> Send the OTP reciveved to your numer in the format** `1 2 3 4 5` **(Give space b/w each digit)\n
>>>> (If you have two step verification send to bot if bot ask.)\n
\nNOTE:
\nIf you made any mistake anywhere press /cancel and then press /start\n\n🥰**
"""

    buttons = [[
        InlineKeyboardButton('JOIN MY CHANNEL', url='https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17'),
        InlineKeyboardButton('JOIN MY GROUP', url='https://t.me/searchkannadamovies'),
        ],[
        InlineKeyboardButton('👤Any Doubt', url='https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17'),
        InlineKeyboardButton('CHANNEL Updates', url='https://t.me/searchkannadamovies'),
        ],[
        InlineKeyboardButton('💥Join my Channel💥', url='https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17'),
        ],[
        InlineKeyboardButton('📕 About', callback_data='about'),
        InlineKeyboardButton('❌ Close', callback_data='close')
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
    about_text = f"""**📃MY DETAILS:**
\n🤖 **My Name:** {me.mention(style='md')}  
\n📝 **Language:** [Python3](https://www.python.org/)
\n👨‍💻 **Developer:** [beereshbanakards](https://t.me/beereshbanakards)
\n📢 **Channel:** [CHANNEL Updates](https://t.me/searchkannadamovies)
\n👥 **Group:** [Any Doubt](https://t.me/KANNADAMOVIES_17)
\n🌐 **Source Code:** [Press Me 😋](https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17)
\n🚀 **MY Channel:** [KANNADAMOVIES_17](https://t.me/searchkannadamovies)
\n 1:- [JOIN AND SUPPORT](https://t.me/KANNADAMOVIES_17)
\n 2:- [THIS BOT IS MADE BY❤ @BAGURUJOINAGUUKANNADAMOVIES_17](https://t.me/searchkannadamovies)
"""

    buttons = [[
        InlineKeyboardButton('Join my Channel', url='https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17'),
        InlineKeyboardButton('Join my Group', url='https://t.me/searchkannadamovies'),
        ],[
        InlineKeyboardButton('👤Any Doubt', url='https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17'),
        InlineKeyboardButton('channel Updates', url='https://t.me/searchkannadamovies'),
        ],[
        InlineKeyboardButton('💥Join my Channel💥', url='https://t.me/BAGURUJOINAGUUKANNADAMOVIES_17'),
        ],[
        InlineKeyboardButton('💡 Help', callback_data='help'),
        InlineKeyboardButton('❌ Close', callback_data='close')
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
        await msg.reply("⛔ Process Cancelled.\n\n**👤Any Doubt Join my channel💝
@BAGURUJOINAGUUKANNADAMOVIES_17**")
        return True
    return False 
