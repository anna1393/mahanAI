import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import nest_asyncio
import asyncio
from flask import Flask
from threading import Thread
import os

# کلیدها از محیط سیستم خونده می‌شن
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Flask برای Railway
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# هندلر اصلی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text or ""
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id
    contains_keyword = 'ماهان' in text.lower()

    if is_reply_to_bot or contains_keyword:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "تو نسخه دیجیتال ماهان هستی، خلاق و خودمونی حرف بزن."},
                {"role": "user", "content": text}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await message.reply_text(reply)

# اجرای ربات
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())
