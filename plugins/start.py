# ────────────────────────────────────────────────────────────────
# ✅  THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐  FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────────────────────────────────────
import asyncio
import os
import random
import sys
import time
import string
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, CHANNEL_ID, FORCE_MSG, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, OWNER_TAG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, OWNER_ID, SHORTLINK_API_URL, SHORTLINK_API_KEY, USE_PAYMENT, USE_SHORTLINK, VERIFY_EXPIRE, TIME, TUT_VID, U_S_E_P
from helper_func import encode, get_readable_time, increasepremtime, subscribed, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_admin, add_user, del_admin, del_user, full_adminbase, full_userbase, gen_new_count, get_clicks, inc_count, new_link, present_admin, present_hash, present_user, store_batch, get_batch

SECONDS = TIME
TUT_VID = f"{TUT_VID}"
DISABLE_FILE_SEND = False
DISABLE_FILE_SEND = os.environ.get("DISABLE_FILE_SEND", "").lower() == "true"


async def send_messages_by_ids(client, message, ids):
    if DISABLE_FILE_SEND:
        await message.reply("Sorry, this bot is not active. Please use the new link.")
        return []
    temp_msg = await message.reply("ɢɪᴠᴇ ᴍᴇ ᴀ ꜱᴇᴄᴏɴᴅ ʜᴇʀᴇ...⏳ ")
    try:
        messages = await get_messages(client, ids)
    except:
        await message.reply_text("ᴇʜʜ, ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ! 🥲")
        return []
    await temp_msg.delete()
    snt_msgs = []
    for msg in messages:
        if bool(CUSTOM_CAPTION) & bool(msg.document):
            caption = CUSTOM_CAPTION.format(
                previouscaption="" if not msg.caption else msg.caption.html,
                filename=msg.document.file_name
            )
        else:
            caption = "" if not msg.caption else msg.caption.html
        try:
            snt_msg = await msg.copy(
                chat_id=message.from_user.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=None,
                protect_content=PROTECT_CONTENT
            )
            await asyncio.sleep(0.5)
            snt_msgs.append(snt_msg)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            snt_msg = await msg.copy(
                chat_id=message.from_user.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=None,
                protect_content=PROTECT_CONTENT
            )
            snt_msgs.append(snt_msg)
        except:
            pass
    return snt_msgs


async def schedule_delete(message, snt_msgs):
    if SECONDS == 0 or not snt_msgs:
        return
    notification_msg = await message.reply(
        f"❗ ❕  <u>ʀᴇᴍɪɴᴅᴇʀ</u> ❗ ❕ \n\n<b>ᴛʜᴇ ꜱᴇɴᴛ ꜰɪʟᴇ(ꜱ) ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɪɴ {get_exp_time(SECONDS)}.\n\n<i>ᴘʟᴇᴀꜱᴇ ꜰᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ ᴘᴇʀꜱᴏɴᴀʟ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ꜰɪʀꜱᴛ ᴀɴᴅ ᴛʜᴇɴ ꜱᴛᴀʀᴛ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛʜᴇᴍ ᴛʜᴇʀᴇ.</i>"
    )
    await asyncio.sleep(SECONDS)
    for snt_msg in snt_msgs:
        try:
            await snt_msg.delete()
        except:
            pass
    await notification_msg.edit(
        "<b>ᴛʜᴇ ꜱᴇɴᴛ ꜰɪʟᴇ(ꜱ) ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ. ʜᴏᴘᴇ ʏᴏᴜ ʜᴀᴠᴇ ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ ᴘᴇʀꜱᴏɴᴀʟ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ʙʏ ɴᴏᴡ! 🌚</b>"
    )


async def send_verify_message(client, message, id):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    await update_verify_status(id, verify_token=token, link="")
    link = await get_shortlink(SHORTLINK_API_URL, SHORTLINK_API_KEY, f'https://telegram.me/{client.username}?start=verify_{token}')
    if USE_PAYMENT:
        btn = [
            [InlineKeyboardButton("ᴠᴇʀɪꜰʏ 🎀", url=link)],
            [InlineKeyboardButton('ʜᴏᴡ ᴛᴏ ᴠᴇʀɪꜰʏ 🥲', url=TUT_VID)],
            [InlineKeyboardButton("ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ", callback_data="buy_prem")]
        ]
    else:
        btn = [
            [InlineKeyboardButton("ᴠᴇʀɪꜰʏ 🎀", url=link)],
            [InlineKeyboardButton('ʜᴏᴡ ᴛᴏ ᴠᴇʀɪꜰʏ 🥲', url=TUT_VID)]
        ]
    await message.reply(
        "ʏᴏᴜʀ ᴛᴏᴋᴇɴ ʜᴀꜱ ᴇxᴘɪʀᴇᴅ! ❌ ❌ \n\nᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪꜰʏ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇꜱꜱ ꜰᴏʀ ɴᴇxᴛ 24 ʜᴏᴜʀꜱ",
        reply_markup=InlineKeyboardMarkup(btn),
        protect_content=False,
        quote=True
    )


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    verify_status = await get_verify_status(id)

    # ── Handle verify_ token callback ───────────────────────────
    if USE_SHORTLINK and "verify_" in message.text:
        if id not in ADMINS:
            if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                await update_verify_status(id, is_verified=False)
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply("ᴇʜʜ, ᴛʜᴇ ᴛᴏᴋᴇɴ ʀᴇᴄᴇɪᴠᴇᴅ ɪꜱ ᴀɴ ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ ᴏɴᴇ.")
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            await message.reply(
                "ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ ʙᴜᴅᴅʏ!! 🎉\n\nʏᴏᴜʀ ᴛᴏᴋᴇɴ ʜᴀꜱ ʙᴇᴇɴ ᴠᴇʀɪꜰɪᴇᴅ!\n\n<i>ʏᴏᴜ ᴡɪʟʟ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇꜱꜱ ꜰᴏʀ ᴛʜᴇ ɴᴇxᴛ 24 ʜᴏᴜʀꜱ!</i>",
                protect_content=False,
                quote=True
            )
            return

    # ── File request handling ────────────────────────────────────
    if len(message.text) > 7:

        # ── VERIFY GATE (applies to ALL link types) ──────────────
        if USE_SHORTLINK and id not in ADMINS:
            if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                await update_verify_status(id, is_verified=False)
                verify_status = await get_verify_status(id)
            if not verify_status['is_verified']:
                await send_verify_message(client, message, id)
                return
        # ─────────────────────────────────────────────────────────

        try:
            base64_string = message.text.split(" ", 1)[1]
        except:
            return

        # ── fs_ format (single file from channel_post.py) ────────
        if base64_string.startswith("fs_"):
            try:
                import base64 as _b64
                msg_id = int(_b64.b64decode(base64_string[3:] + "==").decode())
                ids = [msg_id]
            except Exception:
                return
            snt_msgs = await send_messages_by_ids(client, message, ids)
            await schedule_delete(message, snt_msgs)
            return

        _string = await decode(base64_string)

        # ── batchkey format ──────────────────────────────────────
        if _string.startswith("batchkey_"):
            key = _string[len("batchkey_"):]
            msg_ids = await get_batch(key)
            if not msg_ids:
                await message.reply("ꜱᴏʀʀʏ, ʙᴀᴛᴄʜ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ. 🥲")
                return
            snt_msgs = await send_messages_by_ids(client, message, msg_ids)
            await schedule_delete(message, snt_msgs)
            return

        argument = _string.split("-")

        # ── poster_bot raw-ID format: get-id1-id2-id3-... ────────
        # poster_bot encodes raw message IDs directly (no channel_id multiplication).
        # Detect by checking: if argument[1] is NOT divisible by channel_id,
        # these are raw IDs — use them directly without division.
        def is_raw_id_format(parts, ch_id):
            try:
                return int(parts[1]) % ch_id != 0
            except:
                return False

        if len(argument) >= 2 and is_raw_id_format(argument, abs(client.db_channel.id)):
            try:
                ids = [int(x) for x in argument[1:]]
            except:
                return
            snt_msgs = await send_messages_by_ids(client, message, ids)
            await schedule_delete(message, snt_msgs)
            return

        # ── original multiplied format (len 4 or 5) ──────────────
        if (len(argument) == 5) or (len(argument) == 4):
            if not await present_hash(base64_string):
                try:
                    await gen_new_count(base64_string)
                except:
                    pass
            await inc_count(base64_string)
            if len(argument) == 5:
                try:
                    start = int(int(argument[3]) / abs(client.db_channel.id))
                    end = int(int(argument[4]) / abs(client.db_channel.id))
                except:
                    return
                ids = range(start, end+1) if start <= end else []
            elif len(argument) == 4:
                try:
                    ids = [int(int(argument[3]) / abs(client.db_channel.id))]
                except:
                    return
            snt_msgs = await send_messages_by_ids(client, message, ids)
            await schedule_delete(message, snt_msgs)
            return

        # ── original multiplied format (len 3 or 2) ──────────────
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            ids = range(start, end+1) if start <= end else []
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        else:
            return
        snt_msgs = await send_messages_by_ids(client, message, ids)
        await schedule_delete(message, snt_msgs)
        return

    # ── /start with no file payload ──────────────────────────────
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("💝 Cartoongram", url='https://t.me/Cartoongram23')],
        [
            InlineKeyboardButton("💸 ᴘʀᴇᴍɪᴜᴍ", callback_data="buy_prem"),
            InlineKeyboardButton("😊 ᴀʙᴏᴜᴛ ᴍᴇ", callback_data="about")
        ],
        [
            InlineKeyboardButton("🔄️ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ", url='https://t.me/ND2330'),
            InlineKeyboardButton("🔒 ᴄʟᴏꜱᴇ", callback_data="close")
        ]
    ])
    await message.reply_text(
        text=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )


#=====================================================================================#
WAIT_MSG = """<b>Processing ...</b>"""
REPLY_ERROR = """<code>Use this command as a replay to any telegram message without any spaces.</code>"""
#=====================================================================================#

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="⌬ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ✇", url=client.invitelink),
            InlineKeyboardButton(text="✇ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ⌬", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton(text="〄  ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ⍟", url=client.invitelink3),
            InlineKeyboardButton(text="⍟ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 〄 ", url=client.invitelink4),
        ]
    ]
    try:
        buttons.append([
            InlineKeyboardButton(
                text='• ɴᴏᴡ ᴄʟɪᴄᴋ ʜᴇʀᴇ •',
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass
    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.command('ch2l') & filters.private)
async def gen_link_encoded(client: Bot, message: Message):
    try:
        hash = await client.ask(text="Enter the code here... \n /cancel to cancel the operation", chat_id=message.from_user.id, timeout=60)
    except Exception as e:
        await hash.reply(f"😔 some error occurred {e}")
        return
    if hash.text == "/cancel":
        await hash.reply("Cancelled 😉!")
        return
    link = f"https://t.me/{client.username}?start={hash.text}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🎉 Click Here ", url=link)]])
    await hash.reply_text(f"<b>🧑‍💻 Here is your generated link</b>", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot 👥")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = successful = blocked = deleted = unsuccessful = 0
        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ ᴍᴇꜱꜱᴀɢᴇ..</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
            total += 1
        await pls_wait.edit(f"<b>Broadcast Completed 🟢\nTotal: {total}\nSuccessful: {successful}\nBlocked: {blocked}\nDeleted: {deleted}\nUnsuccessful: {unsuccessful}</b>")
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.command('auth') & filters.private)
async def auth_command(client: Bot, message: Message):
    await client.send_message(chat_id=OWNER_ID, text=f"Message for @{OWNER_TAG}\n<code>{message.from_user.id}</code>\n/add_admin <code>{message.from_user.id}</code> 🤫")
    await message.reply("Please wait for verification from the owner. 🫣")


@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def command_add_admin(client: Bot, message: Message):
    while True:
        try:
            admin_id = await client.ask(text="Enter admin id 🔢\n /cancel to cancel : ", chat_id=message.from_user.id, timeout=60)
        except Exception as e:
            return
        if admin_id.text == "/cancel":
            await admin_id.reply("Cancelled 😉!")
            return
        try:
            await Bot.get_users(user_ids=admin_id.text, self=client)
            break
        except:
            await admin_id.reply("❌ Error 😖\n\nThe admin id is incorrect.", quote=True)
    if not await present_admin(admin_id.text):
        try:
            await add_admin(admin_id.text)
            await message.reply(f"Added admin <code>{admin_id.text}</code> 😼")
        except:
            await message.reply("Failed to add admin. 😔")
    else:
        await message.reply("admin already exist. 💀")


@Bot.on_message(filters.command('del_admin') & filters.private & filters.user(OWNER_ID))
async def delete_admin_command(client: Bot, message: Message):
    while True:
        try:
            admin_id = await client.ask(text="Enter admin id 🔢\n /cancel to cancel : ", chat_id=message.from_user.id, timeout=60)
        except:
            return
        if admin_id.text == "/cancel":
            await admin_id.reply("Cancelled 😉!")
            return
        try:
            await Bot.get_users(user_ids=admin_id.text, self=client)
            break
        except:
            await admin_id.reply("❌ Error\n\nThe admin id is incorrect.", quote=True)
    if await present_admin(admin_id.text):
        try:
            await del_admin(admin_id.text)
            await message.reply(f"Admin <code>{admin_id.text}</code> removed 😀")
        except Exception as e:
            await message.reply("Failed to remove admin. 😔")
    else:
        await message.reply("admin doesn't exist. 💀")


@Bot.on_message(filters.command('admins') & filters.private)
async def admin_list_command(client: Bot, message: Message):
    admin_list = await full_adminbase()
    await message.reply(f"Full admin list 📃\n<code>{admin_list}</code>")


@Bot.on_message(filters.command('ping') & filters.private)
async def check_ping_command(client: Bot, message: Message):
    start_t = time.time()
    rm = await message.reply_text("Pinging....", quote=True)
    end_t = time.time()
    await rm.edit(f"Ping 🔥!\n{(end_t - start_t) * 1000:.3f} ms")


@Client.on_message(filters.private & filters.command('restart') & filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(text="<i>ʀᴇꜱᴛᴀʀᴛɪɴɢ ᴛʜᴇ ꜱᴇʀᴠᴇʀꜱ 🔃</i>", quote=True)
    await asyncio.sleep(5)
    await msg.edit("<i>ꜱᴇʀᴠᴇʀꜱ ʀᴇꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅</i>")
    try:
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print(e)


if USE_PAYMENT:
    @Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
    async def add_user_premium_command(client: Bot, message: Message):
        while True:
            try:
                user_id = await client.ask(text="ᴇɴᴛᴇʀ ᴛʜᴇ ɪᴅ ᴏꜰ ᴜꜱᴇʀ 🔢\n\nᴘʀᴇꜱꜱ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ: ", chat_id=message.from_user.id, timeout=60)
            except Exception as e:
                return
            if user_id.text == "/cancel":
                await user_id.edit("ᴘʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
                return
            try:
                await Bot.get_users(user_ids=user_id.text, self=client)
                break
            except:
                await user_id.edit("❌ ᴇʀʀᴏʀ 😖\n\nᴛʜᴇ ᴜꜱᴇʀ ɪᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.", quote=True)
        user_id = int(user_id.text)
        while True:
            try:
                timeforprem = await client.ask(text="Choose:\n⁕ <code>1</code> 7 days\n⁕ <code>2</code> 1 Month\n⁕ <code>3</code> 3 Month\n⁕ <code>4</code> 6 Month\n⁕ <code>5</code> 1 year", chat_id=message.from_user.id, timeout=60)
            except Exception as e:
                return
            if not int(timeforprem.text) in [1, 2, 3, 4, 5]:
                await message.reply("Wrong input. 😖")
                continue
            break
        timeforprem = int(timeforprem.text)
        timestring = {1: "7 days", 2: "1 month", 3: "3 month", 4: "6 month", 5: "1 year"}.get(timeforprem, "")
        try:
            await increasepremtime(user_id, timeforprem)
            await message.reply("Premium added! 🤫")
            await client.send_message(chat_id=user_id, text=f"ᴀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴏꜰ {timestring} ᴀᴄᴛɪᴠᴀᴛᴇᴅ! ✨")
        except Exception as e:
            await message.reply("Some error occurred. Check logs.")

# ────────────────────────────────────────────────────────────────
# ✅  THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐  FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────────────────────────────────────
