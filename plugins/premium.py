from pyrogram import filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS
from database.database import user_data, increasepremtime, remove_premium
from datetime import datetime

# ── /add_prem ──────────────────────────────────────────────────
@Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
async def add_user_premium_command(client: Bot, message: Message):
    # Step 1: Get user ID
    while True:
        try:
            user_id_msg = await client.ask(
                chat_id=message.from_user.id,
                text="ᴇɴᴛᴇʀ ᴛʜᴇ ɪᴅ ᴏꜰ ᴜꜱᴇʀ 🔢\n\nᴘʀᴇꜱꜱ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ:",
                timeout=60
            )
        except:
            return
        if user_id_msg.text == "/cancel":
            await user_id_msg.reply("ᴘʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
            return
        try:
            await client.get_users(user_ids=user_id_msg.text)
            break
        except:
            await user_id_msg.reply("❌ ᴇʀʀᴏʀ 😖\n\nᴛʜᴇ ᴜꜱᴇʀ ɪᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.")

    user_id = int(user_id_msg.text)

    # Step 2: Get plan choice
    while True:
        try:
            plan_msg = await client.ask(
                chat_id=message.from_user.id,
                text=(
                    "ᴄʜᴏᴏꜱᴇ ᴀ ᴘʟᴀɴ:\n\n"
                    "⁕ <code>1</code> — 7 Days\n"
                    "⁕ <code>2</code> — 1 Month\n"
                    "⁕ <code>3</code> — 3 Months\n"
                    "⁕ <code>4</code> — 6 Months\n"
                    "⁕ <code>5</code> — 1 Year\n\n"
                    "ᴘʀᴇꜱꜱ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ:"
                ),
                timeout=60
            )
        except:
            return
        if plan_msg.text == "/cancel":
            await plan_msg.reply("ᴘʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
            return
        if not plan_msg.text.isdigit() or int(plan_msg.text) not in [1, 2, 3, 4, 5]:
            await plan_msg.reply("❌ Wrong input. Send a number between 1–5.")
            continue
        break

    plan = int(plan_msg.text)
    plan_labels = {1: "7 Days", 2: "1 Month", 3: "3 Months", 4: "6 Months", 5: "1 Year"}
    timestring = plan_labels[plan]

    try:
        expiry = await increasepremtime(user_id, plan)
        await message.reply(
            f"✅ <b>Premium Added!</b>\n\n"
            f"👤 User: <code>{user_id}</code>\n"
            f"📦 Plan: <b>{timestring}</b>\n"
            f"📅 Expires: <b>{expiry.strftime('%d %b %Y')}</b>"
        )
        await client.send_message(
            chat_id=user_id,
            text=(
                f"🎉 <b>PREMIUM ACTIVATED!</b>\n\n"
                f"✅ Plan: <b>{timestring}</b>\n"
                f"📅 Expires: <b>{expiry.strftime('%d %b %Y')}</b>\n\n"
                f"Enjoy your benefits:\n"
                f"○ DIRECT FILES\n"
                f"○ AD-FREE EXPERIENCE\n"
                f"○ UNLIMITED MOVIES, SERIES & ANIME"
            )
        )
    except Exception as e:
        await message.reply(f"❌ Some error occurred: {e}")


# ── /rem_prem ──────────────────────────────────────────────────
@Bot.on_message(filters.command('rem_prem') & filters.private & filters.user(ADMINS))
async def rem_user_premium_command(client: Bot, message: Message):
    while True:
        try:
            user_id_msg = await client.ask(
                chat_id=message.from_user.id,
                text="ᴇɴᴛᴇʀ ᴛʜᴇ ɪᴅ ᴏꜰ ᴜꜱᴇʀ 🔢\n\nᴘʀᴇꜱꜱ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ:",
                timeout=60
            )
        except:
            return
        if user_id_msg.text == "/cancel":
            await user_id_msg.reply("ᴘʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ!")
            return
        try:
            await client.get_users(user_ids=user_id_msg.text)
            break
        except:
            await user_id_msg.reply("❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ.")

    user_id = int(user_id_msg.text)
    try:
        await remove_premium(user_id)
        await message.reply(f"✅ Premium removed for <code>{user_id}</code>")
        await client.send_message(
            chat_id=user_id,
            text="⚠️ <b>Your premium membership has been removed by admin.</b>"
        )
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


# ── /myplan ────────────────────────────────────────────────────
@Bot.on_message(filters.command("myplan") & filters.private)
async def my_plan_cmd(client: Bot, message: Message):
    user_id = message.from_user.id
    user = await user_data.find_one({'_id': user_id})

    if not user or not user.get('premium'):
        await message.reply(
            "❌ <b>No active premium plan.</b>\n\n"
            "Use /buy to get premium access."
        )
        return

    expiry = user.get('expiry_date')
    if not expiry or expiry < datetime.now():
        await message.reply(
            "⚠️ <b>Your premium has expired!</b>\n\n"
            "Use /buy to renew."
        )
        return

    remaining = expiry - datetime.now()
    days_left = remaining.days
    hours_left = remaining.seconds // 3600

    await message.reply(
        f"✅ <b>ACTIVE PREMIUM PLAN</b>\n\n"
        f"📅 Expires: <b>{expiry.strftime('%d %b %Y')}</b>\n"
        f"⏳ Remaining: <b>{days_left} days, {hours_left} hrs</b>"
    )
