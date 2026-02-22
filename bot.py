import os
TOKEN = os.environ.get("TOKEN")
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Global exchange rate (default None)
exchange_rate = None  # 1m = ? b

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exchange_rate
    text = update.message.text.lower().replace(" ", "")

    # 1️⃣ Set rate: 1m800b
    rate_match = re.match(r"1m(\d+)b", text)
    if rate_match:
        exchange_rate = float(rate_match.group(1))
        await update.message.reply_text(f"Rate set ✅\n1m = {exchange_rate}b")
        return

    if exchange_rate is None:
        await update.message.reply_text("Rate မသတ်မှတ်ရသေးပါ ❗\nဥပမာ: 1m800b")
        return

    # 2️⃣ Myanmar to Baht: 200000m
    m_match = re.match(r"(\d+)m", text)
    if m_match:
        mmk = float(m_match.group(1))
        result = (mmk / 100000) * exchange_rate
        await update.message.reply_text(f"{mmk:.0f}m = {result:.0f}b")
        return

    # 3️⃣ Baht to Myanmar: 1600b
    b_match = re.match(r"(\d+)b", text)
    if b_match:
        baht = float(b_match.group(1))
        result = (baht / exchange_rate) * 100000
        await update.message.reply_text(f"{baht:.0f}b = {result:.0f}m")
        return

    await update.message.reply_text("Format မှားနေပါတယ် ❗")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Exchange Bot Running...")
app.run_polling()
