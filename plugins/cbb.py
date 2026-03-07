# ────────────────────────────────────────────────────────────────

# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.

# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams

# ────────────────────────────────────────────────────────────────

from pyrogram import __version__
from bot import Bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import PRICE1, PRICE2, PRICE3, PRICE4, PRICE5, UPI_ID, UPI_IMAGE_URL, SCREENSHOT_URL

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ More Bots: <a href='https://t.me/Master_xkid'>Master</a>\n○ Language: <a href='https://www.python.org/'>Python 3</a>\n○ Fueled By: <a href='https://t.me/Askmovies4'>InfoHub Updates</a>\n○ Server: <a href='https://www.ubuntu.com/'>Private VPS</a></b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data == "buy_prem":
        await query.message.edit_text(
            text=f"👋 @{query.from_user.username}, here are our Prime Membership plans – {PRICE1}/7 days, {PRICE2}/1 month, {PRICE3}/3 months, {PRICE4}/6 months, {PRICE5}/1 year | 💵 UPI ID: <code>{UPI_ID}</code> | 📸 <a href='{UPI_IMAGE_URL}'>Scan QR Code</a> to pay | 🧾 After payment, send your screenshot | 💬 For help or alternative payment methods, contact @Master_xkid",
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(
                [   
                    [
                        InlineKeyboardButton("ꜱᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ 📸", url=(SCREENSHOT_URL))
                    ],
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )

# ────────────────────────────────────────────────────────────────

# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.

# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams

# ────────────────────────────────────────────────────────────────  
