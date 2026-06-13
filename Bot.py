import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ─────────────────────────────────────────────
#  ⚙️  CONFIGURATION — Sirf yahan edit karo
# ─────────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

CHANNEL_1_ID   = "@your_channel_1"
CHANNEL_1_LINK = "https://t.me/your_channel_1"
CHANNEL_1_NAME = "🎮 Channel 1"

CHANNEL_2_ID   = "@your_channel_2"
CHANNEL_2_LINK = "https://t.me/your_channel_2"
CHANNEL_2_NAME = "🎁 Channel 2"
# ─────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """
🎉✨ *GOOGLE PLAY REDEEM CODE GIVEAWAY!* ✨🎉

Hey there, lucky one! 👋

We're thrilled to announce our *exclusive Google Play Redeem Code Giveaway* — and YOU could be one of the winners! 🏆

━━━━━━━━━━━━━━━━━━━━━
🎁 *WHAT'S UP FOR GRABS?*
━━━━━━━━━━━━━━━━━━━━━
🔹 Google Play Gift Codes
🔹 100% Genuine & Verified Codes
🔹 Instant Delivery (within 24 hours)
🔹 Multiple Winners Every Round!

━━━━━━━━━━━━━━━━━━━━━
📋 *HOW TO PARTICIPATE?*
━━━━━━━━━━━━━━━━━━━━━
✅ Step 1 — Join *both* our channels below
✅ Step 2 — Click the *"🎯 Claim My Code"* button
✅ Step 3 — Wait for your code (within 24 hrs!) ⏳

━━━━━━━━━━━━━━━━━━━━━
⚡ *LIMITED CODES AVAILABLE — Don't miss out!*
━━━━━━━━━━━━━━━━━━━━━

👇 *Join both channels to unlock your giveaway entry:*
"""

NOT_JOINED_MESSAGE = """
⚠️ *Oops! You haven't joined both channels yet!*

You must join *BOTH* channels to be eligible for the giveaway. 🎁

👇 Please join the channels below and then click *"🎯 Claim My Code"* again!
"""

SUCCESS_MESSAGE = """
🎊 *Congratulations! You're All Set!* 🎊

✅ Both channels verified successfully!

━━━━━━━━━━━━━━━━━━━━━
🎁 *YOUR REDEEM CODE IS PENDING...*
━━━━━━━━━━━━━━━━━━━━━

⏳ Your Google Play Redeem Code has been added to the queue!

📬 You will receive your exclusive code within *24 hours*.

━━━━━━━━━━━━━━━━━━━━━
📌 *IMPORTANT NOTES:*
━━━━━━━━━━━━━━━━━━━━━
🔔 Make sure your DMs are *open* to receive the code
🔕 Do *NOT* leave the channels before receiving your code
⚠️  Leaving channels = disqualification from the giveaway
━━━━━━━━━━━━━━━━━━━━━

Thank you for participating! 🙏
*Good luck & stay tuned!* 🍀✨
"""

async def is_member(bot, user_id: int, channel_id: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        logger.warning(f"Could not check membership for {channel_id}: {e}")
        return False

def join_buttons_keyboard(show_claim: bool = False) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(f"Join {CHANNEL_1_NAME}", url=CHANNEL_1_LINK),
            InlineKeyboardButton(f"Join {CHANNEL_2_NAME}", url=CHANNEL_2_LINK),
        ],
    ]
    if show_claim:
        keyboard.append(
            [InlineKeyboardButton("🎯 Claim My Code", callback_data="claim")]
        )
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode="Markdown",
        reply_markup=join_buttons_keyboard(show_claim=True),
        disable_web_page_preview=True,
    )

async def claim_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    bot     = context.bot

    joined_ch1 = await is_member(bot, user_id, CHANNEL_1_ID)
    joined_ch2 = await is_member(bot, user_id, CHANNEL_2_ID)

    if joined_ch1 and joined_ch2:
        await query.message.reply_text(
            SUCCESS_MESSAGE,
            parse_mode="Markdown",
        )
    else:
        await query.message.reply_text(
            NOT_JOINED_MESSAGE,
            parse_mode="Markdown",
            reply_markup=join_buttons_keyboard(show_claim=True),
            disable_web_page_preview=True,
        )

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(claim_callback, pattern="^claim$"))
    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()