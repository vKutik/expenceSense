"""
Telegram Bot for Mini App
Launches the expense tracker Mini App
"""
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"
WEB_APP_URL = "http://localhost:5000"  # Change to HTTPS URL for production

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - launches Mini App."""
    user = update.effective_user
    
    # Create WebApp button
    web_app_info = WebAppInfo(url=WEB_APP_URL)
    keyboard = [[KeyboardButton("💰 Open Expense Tracker", web_app=web_app_info)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_message = f"""
💰 <b>Welcome to Expense Tracker!</b>

Hello {user.first_name}! I'll help you track your expenses with our beautiful Mini App.

<b>📱 Features:</b>
• 💰 Add expenses with categories
• 📊 View real-time statistics  
• 📈 Generate expense charts
• 🎯 Touch-friendly interface
• 📱 Mobile optimized
• 🔐 Secure Telegram login

<b>🌐 Mini App Features:</b>
• Modern phone interface
• Account login with Telegram
• Expense tracking
• Category management
• Statistics and analytics

Tap the button below to open the Mini App:
    """
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages - redirect to Mini App."""
    # For any text, show the Mini App button
    web_app_info = WebAppInfo(url=WEB_APP_URL)
    keyboard = [[KeyboardButton("💰 Open Expense Tracker", web_app=web_app_info)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "💰 <b>Expense Tracker Mini App</b>\n\n"
        "Tap the button below to open the expense tracker:\n\n"
        "🌐 <b>Features:</b>\n"
        "• Modern phone interface\n"
        "• Telegram account login\n"
        "• Expense tracking\n"
        "• Statistics and analytics",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors gracefully."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Telegram Mini App Bot...")
    logger.info(f"Bot Token: {BOT_TOKEN[:10]}...")
    logger.info("Web App URL: http://localhost:5000")
    logger.info("Features: Phone interface, Account login, Expense tracking")
    application.run_polling()

if __name__ == '__main__':
    main()
