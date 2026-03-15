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
            text=f"<b>○ More Bots: <a href='https://t.me/Master_xkid'>Master</a>\n○ Language: <a href='https://www.python.org/'>Python 3</a>\n○ Fueled By: <a href='https://t.me/Askmovies4'>InfoHub Updates</a>\n○ Server: <a href='https://www.ubuntu.com/'>Private VPS</a></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔒 Close", callback_data="close")]
            ])
        )
    elif data == "buy_prem":
        await query.message.edit_text(
            text=(
                f"<b>♻️ AVAILABLE PLANS ♻️</b>\n\n"
                f"• <b>1 WEEK</b>  -  <code>{PRICE1}</code>\n"
                f"• <b>1 MONTH</b>  -  <code>{PRICE2}</code>\n"
                f"• <b>3 MONTHS</b>  -  <code>{PRICE3}</code>\n"
                f"• <b>6 MONTHS</b>  -  <code>{PRICE4}</code>\n\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"<b>🎁 PREMIUM FEATURES</b>\n\n"
                f"○ NO NEED TO VERIFY\n"
                f"○ DIRECT FILES\n"
                f"○ AD-FREE EXPERIENCE\n"
                f"○ UNLIMITED MOVIES, SERIES & ANIME\n"
                f"○ FULL ADMIN SUPPORT\n\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"✨ <b>UPI ID</b> - <code>{UPI_ID}</code>\n\n"
                f"<b>CHECK YOUR ACTIVE PLAN</b> /myplan\n\n"
                f"🚫 <b>MUST SEND SCREENSHOT AFTER PAYMENT</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ 📸", url=SCREENSHOT_URL)],
                [InlineKeyboardButton("🔒 Close", callback_data="close")]
            ])
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
