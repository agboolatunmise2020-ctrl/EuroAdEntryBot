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
    "Welcome to Euro Community Portal\n\n"
    "A free educational resource on financial markets and economic literacy.\n\n"
    "Use the menu below to explore our content.\n\n"
    "All content is for informational and educational purposes only."
)

DISCLAIMER_TEXT = (
    "Important Disclaimer\n\n"
    "All content provided here is strictly for educational and informational purposes only.\n\n"
    "- This is not financial advice\n"
    "- No returns or outcomes are guaranteed\n"
    "- Financial markets involve substantial risk of loss\n"
    "- Past performance does not indicate future results\n"
    "- Always consult a licensed financial advisor before making any decisions\n\n"
    "Please make informed decisions responsibly."
)

MARKET_TEXT = (
    "Weekly Market Overview\n\n"
    "General Sentiment: Neutral to Positive\n\n"
    "Key Observations This Week:\n"
    "- Major indices are approaching key price levels\n"
    "- EUR/USD holding above medium-term support\n"
    "- Commodities remain sensitive to global developments\n\n"
    "Events to Monitor:\n"
    "- Inflation data releases from major economies\n"
    "- Central bank policy announcements\n"
    "- Employment and labour market reports\n\n"
    "This overview is for educational purposes only. Not financial advice."
)

BASICS_TEXT = (
    "Financial Markets — Key Concepts\n\n"
    "What are Financial Markets?\n"
    "Financial markets are platforms where buyers and sellers exchange assets such as currencies, "
    "stocks, and commodities. Understanding how they work is a key part of financial literacy.\n\n"
    "Core Concepts:\n"
    "- Supply and Demand — prices are driven by market forces\n"
    "- Risk Management — understanding and limiting exposure\n"
    "- Diversification — spreading risk across different assets\n"
    "- Economic Indicators — data that reflects the health of an economy\n"
    "- Price Trends — how markets move over time\n\n"
    "Key Principles for Beginners:\n"
    "1. Always research before making any financial decision\n"
    "2. Understand the risks involved in any financial activity\n"
    "3. Keep a record of your learning and decisions\n"
    "4. Focus on building knowledge before anything else\n\n"
    "For educational purposes only."
)

FAQ_TEXT = (
    "Frequently Asked Questions\n\n"
    "Q: What are financial markets?\n"
    "A: They are systems where assets like currencies, shares, and commodities are bought and sold.\n\n"
    "Q: What is market volatility?\n"
    "A: Volatility refers to how much and how quickly prices change in a market.\n\n"
    "Q: What is an economic indicator?\n"
    "A: Data points like inflation rates or employment figures that reflect economic conditions.\n\n"
    "Q: What is risk management?\n"
    "A: The process of identifying and reducing potential financial losses through planning.\n\n"
    "Q: How can I improve my financial literacy?\n"
    "A: Read reputable sources, follow economic news, and consult licensed professionals.\n\n"
    "All answers are for educational purposes only."
)

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Disclaimer", callback_data="disclaimer"),
            InlineKeyboardButton("Market Overview", callback_data="market")
        ],
        [
            InlineKeyboardButton("Key Concepts", callback_data="basics"),
            InlineKeyboardButton("FAQ", callback_data="faq")
        ]
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Menu", callback_data="back_to_menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "disclaimer":
        await query.edit_message_text(
            DISCLAIMER_TEXT,
            reply_markup=back_menu()
        )
    elif query.data == "market":
        await query.edit_message_text(
            MARKET_TEXT,
            reply_markup=back_menu()
        )
    elif query.data == "basics":
        await query.edit_message_text(
            BASICS_TEXT,
            reply_markup=back_menu()
        )
    elif query.data == "faq":
        await query.edit_message_text(
            FAQ_TEXT,
            reply_markup=back_menu()
        )
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            WELCOME_TEXT,
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
