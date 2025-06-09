import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv("TOKEN")
CHANNEL_ID =
int(os.getenv("CHANNEL_ID"))

welcome_text = "Welcome to the group 🫂"
pending_setups = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("CREATOR", url="https://t.me/t_h_e_devil_666")]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "ℍ𝔸𝕀, 𝕀  𝔸𝕄  𝔸 𝕎𝔼𝕃ℂ𝕆𝕄𝔼ℝ 𝔽𝕆ℝ 𝔾ℝ𝕆𝕌ℙ𝕊\n"
        "𝔸𝔻𝔻  𝕄𝔼  𝕋𝕆   𝕐𝕆𝕌ℝ  𝔾ℝ𝕆𝕌ℙ",
        reply_markup=markup
    )
    await context.bot.send_message(chat_id=CHANNEL_ID, text="🤖 Welcomer bot started and online!")

async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setwelcome <message>")
        return

    user_id = update.effective_user.id
    pending_setups[user_id] = " ".join(context.args)

    keyboard = [[InlineKeyboardButton("Approve Admin", callback_data=f"approve_{user_id}")]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click the button below to verify admin rights before setting the welcome message.",
        reply_markup=markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if not data.startswith("approve_"):
        return

    target_id = int(data.split("_")[1])
    chat_id = query.message.chat.id

    member = await context.bot.get_chat_member(chat_id, user_id)

    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        if user_id == target_id and user_id in pending_setups:
            global welcome_text
            welcome_text = pending_setups.pop(user_id)
            await query.edit_message_text("Welcome message set successfully!")
        else:
            await query.edit_message_text("Mismatch or no pending setup found.")
    else:
        await query.edit_message_text("You must be an admin to approve this action.")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(
            f"{welcome_text}, {user.mention_html()}",
            parse_mode="HTML"
        )

async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /notify <message>")
        return
    message = " ".join(context.args)
    await context.bot.send_message(chat_id=CHANNEL_ID, text=f"📢 {message}")
    await update.message.reply_text("✅ Message sent to channel.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setwelcome", setwelcome))
app.add_handler(CommandHandler("notify", notify))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

print("Bot is running...")
app.run_polling()
