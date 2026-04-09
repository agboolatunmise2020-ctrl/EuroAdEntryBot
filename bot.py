import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

WELCOME_TEXT = (
    "👋 *Welcome to Euro Community Entry*\n\n"
    "This bot provides a secure gateway to our private trading insights channel. "
    "Click a button below to verify your access, view current market trends, "
    "and join our elite community of traders."
)

ENTRY_RULES_TEXT = (
    "⚠️ *Entry Rules & Disclaimer*\n\n"
    "This Channel doesn't guarantee your profit Earning. "
    "It's meant for *Education purpose only*.\n\n"
    "Trading in any form involves Financial Risk. ⚠️\n\n"
    "Please trade responsibly and only invest what you can afford to lose."
)

MARKET_ANALYSIS_TEXT = (
    "📊 *Weekly Market Analysis*\n\n"
    "*Sentiment:* Neutral/Bullish 📈\n\n"
    "Major assets are testing resistance. Detailed charts and real-time "
    "alerts are posted inside the community.\n\n"
    "_Education only. No financial advice._"
)

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚠️ Entry Rules", callback_data="entry_rules"),
            InlineKeyboardButton("👥 Join Community", url="https://t.me/+AyXFqTTaNEVmNjM1")
        ],
        [
            InlineKeyboardButton("📊 Market Analysis", callback_data="market_analysis"),
            InlineKeyboardButton("💬 Support", url="https://t.me/maxpromarketer")
        ]
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ])

def market_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Join Community", url="https://t.me/+AyXFqTTaNEVmNjM1")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "entry_rules":
        await query.edit_message_text(
            ENTRY_RULES_TEXT,
            parse_mode="Markdown",
            reply_markup=back_menu()
        )
    elif query.data == "market_analysis":
        await query.edit_message_text(
            MARKET_ANALYSIS_TEXT,
            parse_mode="Markdown",
            reply_markup=market_menu()
        )
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

async def main():
    logging.info("Starting Euro Community Portal Bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    logging.info("Bot is running!")
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
