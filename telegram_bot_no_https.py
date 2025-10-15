"""
Telegram Bot without HTTPS requirement
Uses your bot token: 8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4
Works without ngrok by using inline keyboards and direct web links
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    
    # Create inline keyboard without localhost URL
    keyboard = [
        [
            InlineKeyboardButton("📊 View Expenses", callback_data="view_expenses"),
            InlineKeyboardButton("💰 Add Expense", callback_data="add_expense")
        ],
        [
            InlineKeyboardButton("📈 Statistics", callback_data="statistics"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📱 Help", callback_data="help"),
            InlineKeyboardButton("🌐 Web App Info", callback_data="webapp_info")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
💰 <b>Welcome to Expense Tracker!</b>

Hello {user.first_name}! I'll help you track your expenses.

<b>🏗️ Architecture:</b>
• Repository Pattern
• Service Layer  
• Controller Layer
• REST API

<b>🌐 Web App:</b> http://localhost:5000
<b>📱 Bot Features:</b>
• 💰 Add expenses
• 📊 View expenses
• 📈 Statistics
• ⚙️ Settings

Choose an option below or open the web app:
    """
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "view_expenses":
        await query.edit_message_text(
            "📊 <b>View Expenses</b>\n\n"
            "To view your expenses:\n\n"
            "🌐 <b>Web App:</b> http://localhost:5000\n\n"
            "Or use the REST API:\n"
            "<b>GET</b> http://localhost:5000/api/expenses?userId=123\n\n"
            "The web app provides a better interface with charts and categories.",
            parse_mode='HTML'
        )
    
    elif query.data == "add_expense":
        await query.edit_message_text(
            "💰 <b>Add Expense</b>\n\n"
            "To add a new expense:\n\n"
            "🌐 <b>Web App:</b> http://localhost:5000\n\n"
            "Or use the REST API:\n"
            "<b>POST</b> http://localhost:5000/api/expenses\n"
            "<code>{\n"
            '  "userId": 123,\n'
            '  "amount": 25.50,\n'
            '  "categoryId": 1,\n'
            '  "description": "Coffee"\n'
            "}</code>\n\n"
            "The web app provides an easy form to fill out.",
            parse_mode='HTML'
        )
    
    elif query.data == "statistics":
        await query.edit_message_text(
            "📈 <b>Statistics</b>\n\n"
            "View detailed statistics:\n\n"
            "🌐 <b>Web App:</b> http://localhost:5000\n\n"
            "Features:\n"
            "• 📊 Interactive expense charts\n"
            "• 📅 Daily/Monthly reports\n"
            "• 🏷️ Category breakdown\n"
            "• 💰 Budget tracking\n\n"
            "The web app provides beautiful visualizations.",
            parse_mode='HTML'
        )
    
    elif query.data == "settings":
        await query.edit_message_text(
            "⚙️ <b>Settings</b>\n\n"
            "Configure your preferences:\n\n"
            "🌐 <b>Web App:</b> http://localhost:5000\n\n"
            "Settings include:\n"
            "• 🏷️ Manage categories\n"
            "• 💰 Set budgets\n"
            "• 📊 Chart preferences\n"
            "• 🔔 Notifications\n"
            "• 🌍 Language settings\n\n"
            "Use the web app for full settings management.",
            parse_mode='HTML'
        )
    
    elif query.data == "help":
        await query.edit_message_text(
            "📱 <b>Help & Information</b>\n\n"
            "<b>🤖 Bot Token:</b> 8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4\n"
            "<b>🌐 Web App:</b> http://localhost:5000\n"
            "<b>🏗️ Architecture:</b> 3-layer (Repository, Service, Controller)\n\n"
            "<b>📡 REST API Endpoints:</b>\n"
            "• GET /health - Health check\n"
            "• GET /api/expenses?userId=X - Get expenses\n"
            "• POST /api/expenses - Add expense\n"
            "• DELETE /api/expenses/{id}?userId=X - Delete expense\n"
            "• GET /api/categories?userId=X - Get categories\n\n"
            "<b>🌐 Web App Features:</b>\n"
            "• Beautiful interface\n"
            "• Interactive charts\n"
            "• Category management\n"
            "• Real-time updates\n"
            "• Mobile responsive",
            parse_mode='HTML'
        )
    
    elif query.data == "webapp_info":
        await query.edit_message_text(
            "🌐 <b>Web App Information</b>\n\n"
            "<b>URL:</b> http://localhost:5000\n\n"
            "<b>How to access:</b>\n"
            "1. Open your web browser\n"
            "2. Go to: http://localhost:5000\n"
            "3. Use the full expense tracking interface\n\n"
            "<b>Features:</b>\n"
            "• 💰 Add expenses with categories\n"
            "• 📊 View expense charts\n"
            "• 📈 Statistics and analytics\n"
            "• ⚙️ Manage categories\n"
            "• 📱 Mobile-friendly design\n\n"
            "<b>Note:</b> The web app provides the full experience with interactive interface and charts.",
            parse_mode='HTML'
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text.lower()
    
    if "expense" in text or "add" in text:
        await update.message.reply_text(
            "💰 <b>Add Expense</b>\n\n"
            "🌐 Open the web app: http://localhost:5000\n\n"
            "Or use the REST API with your favorite HTTP client.",
            parse_mode='HTML'
        )
    
    elif "view" in text or "expenses" in text or "list" in text:
        await update.message.reply_text(
            "📊 <b>View Expenses</b>\n\n"
            "🌐 Open the web app: http://localhost:5000\n\n"
            "The web app shows your expenses with beautiful charts and categories.",
            parse_mode='HTML'
        )
    
    elif "statistics" in text or "stats" in text or "chart" in text:
        await update.message.reply_text(
            "📈 <b>Statistics</b>\n\n"
            "🌐 Open the web app: http://localhost:5000\n\n"
            "View interactive charts and detailed analytics.",
            parse_mode='HTML'
        )
    
    elif "settings" in text or "config" in text:
        await update.message.reply_text(
            "⚙️ <b>Settings</b>\n\n"
            "🌐 Open the web app: http://localhost:5000\n\n"
            "Manage categories, budgets, and preferences.",
            parse_mode='HTML'
        )
    
    elif "help" in text:
        await update.message.reply_text(
            "📱 <b>Help</b>\n\n"
            "🌐 <b>Web App:</b> http://localhost:5000\n\n"
            "The web app provides the full expense tracking experience with:\n"
            "• Interactive interface\n"
            "• Charts and statistics\n"
            "• Category management\n"
            "• Mobile-friendly design",
            parse_mode='HTML'
        )
    
    else:
        await update.message.reply_text(
            "🤖 <b>Expense Tracker Bot</b>\n\n"
            "I'm here to help you manage your expenses!\n\n"
            "🌐 <b>Web App:</b> http://localhost:5000\n\n"
            "Use the buttons or send /start to see all options.",
            parse_mode='HTML'
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
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Telegram Bot without HTTPS requirement...")
    logger.info(f"Bot Token: {BOT_TOKEN[:10]}...")
    logger.info("Web App URL: http://localhost:5000")
    logger.info("No ngrok required - uses direct web links")
    application.run_polling()

if __name__ == '__main__':
    main()
