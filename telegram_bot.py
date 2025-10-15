"""
Telegram Bot Configuration for Mini App Integration
"""
import os
import logging
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBotConfig:
    """Configuration for Telegram bot and mini app"""
    
    def __init__(self):
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', '8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4')
        self.WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app')
        self.WEBHOOK_URL = os.getenv('WEBHOOK_URL', f'{self.WEBAPP_URL}/webhook')
        
        # Mini App configuration
        self.MINI_APP_TITLE = "Expense Tracker"
        self.MINI_APP_DESCRIPTION = "Track your expenses with a modern, minimalist interface"
        self.MINI_APP_SHORT_NAME = "expensetracker"
        
    def get_webhook_url(self) -> str:
        """Get webhook URL for bot"""
        return self.WEBHOOK_URL
    
    def get_mini_app_url(self) -> str:
        """Get mini app URL"""
        return self.WEBAPP_URL

# Global configuration
config = TelegramBotConfig()

class TelegramBotHandler:
    """Main bot handler for commands and messages"""
    
    def __init__(self):
        self.app = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.first_name}) started the bot")
        
        # Create keyboard with Mini App button
        keyboard = [
            [InlineKeyboardButton(
                "📱 Open Expense Tracker", 
                web_app=WebAppInfo(url=config.get_mini_app_url())
            )],
            [InlineKeyboardButton("ℹ️ About", callback_data="about")],
            [InlineKeyboardButton("🆘 Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = f"""
👋 *Welcome to Expense Tracker, {user.first_name}!*

💰 Track your expenses with ease
📊 View detailed statistics  
🎯 Set and manage budgets
📱 Access from any device

*Features:*
• 🏷️ Smart categorization
• 📈 Visual analytics
• 💳 Bank balance tracking
• 🔒 Secure authentication
• ☁️ Cloud sync (Premium)

Tap the button below to open the app:
        """
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
*Expense Tracker Bot Commands:*

/start - Open the expense tracker app
/help - Show this help message
/about - About the application
/settings - Bot settings
/stats - Quick stats (if authenticated)

*How to use:*
1. Tap "📱 Open Expense Tracker" to launch the app
2. Your Telegram account will be automatically authenticated
3. Start tracking your expenses right away!

*User Levels:*
👤 Guest - Basic features, session storage
📝 Registered - Persistent file storage
⭐ Premium - Database storage, advanced features
👑 Admin - Cloud storage, full access

*Need help?* Contact @yourusername
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_text = f"""
*Expense Tracker v1.1*

🎯 *Purpose:* Modern expense tracking with clean design
🏗️ *Architecture:* Clean Architecture with multiple storage layers
🔐 *Security:* Multi-level authentication system
📱 *Platform:* Telegram Mini App

*Technical Features:*
• Flask backend with clean architecture
• Multi-tier storage (Memory, File, Database, Cloud)
• Token-based authentication
• Real-time updates with observer pattern
• Mobile-first responsive design

*Storage Options:*
• 💾 Memory - Fast, session-only
• 📁 File - Local persistence
• 🗄️ Database - ACID transactions
• ☁️ Cloud - Auto backup & sync

*Built with:* Python, Flask, SQLite, HTML5, CSS3

*Developer:* Your Name
*Version:* 1.1.0
*Last Updated:* October 2024
        """
        
        await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        user = update.effective_user
        
        settings_text = f"""
*Settings for @{user.username}*

*Current Status:*
👤 User Level: Guest (Default)
💾 Storage: Memory
🔑 Authentication: Telegram-based

*Available Upgrades:*
📝 Registered - Persistent storage
⭐ Premium - Database features
👑 Admin - Cloud access

*Privacy:*
✅ Data encrypted in transit
✅ Secure token authentication
✅ No personal data sharing

*Notifications:*
🔔 Expense reminders (Premium)
📊 Weekly reports (Premium)
⚠️ Budget alerts (Premium)

Contact admin for level upgrades.
        """
        
        await update.message.reply_text(settings_text, parse_mode=ParseMode.MARKDOWN)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - show quick stats"""
        user = update.effective_user
        
        # This would normally fetch from your API
        stats_text = f"""
*Quick Stats for {user.first_name}*

💰 *Total Expenses:* $0.00
📊 *This Month:* $0.00
🏷️ *Categories Used:* 0
📅 *Last Expense:* None

*Top Categories:*
No expenses yet

*To view detailed stats:*
Tap "📱 Open Expense Tracker" to access full analytics
        """
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "about":
            await query.edit_message_text(
                "Tap /about for detailed information about the app",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📱 Open App", web_app=WebAppInfo(url=config.get_mini_app_url()))
                ]])
            )
        elif query.data == "help":
            await query.edit_message_text(
                "Tap /help for detailed help and commands",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📱 Open App", web_app=WebAppInfo(url=config.get_mini_app_url()))
                ]])
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user = update.effective_user
        message_text = update.message.text
        
        if message_text and message_text.startswith('/'):
            # Unknown command
            await update.message.reply_text(
                "Unknown command. Use /help to see available commands.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📱 Open Expense Tracker", web_app=WebAppInfo(url=config.get_mini_app_url()))
                ]])
            )
        else:
            # Regular message - encourage app usage
            await update.message.reply_text(
                f"Hi {user.first_name}! 👋\n\n"
                "To track your expenses, please use the Expense Tracker app:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📱 Open Expense Tracker", web_app=WebAppInfo(url=config.get_mini_app_url()))
                ]])
            )
    
    async def webhook_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle webhook updates"""
        logger.info(f"Webhook received: {update}")
        return "OK"
    
    def setup_handlers(self):
        """Setup bot command and message handlers"""
        handlers = [
            CommandHandler("start", self.start_command),
            CommandHandler("help", self.help_command),
            CommandHandler("about", self.about_command),
            CommandHandler("settings", self.settings_command),
            CommandHandler("stats", self.stats_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message),
        ]
        
        for handler in handlers:
            self.app.add_handler(handler)
        
        # Add callback query handler
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def setup_webhook(self):
        """Setup webhook for the bot"""
        try:
            webhook_url = config.get_webhook_url()
            await self.app.bot.set_webhook(url=webhook_url)
            logger.info(f"Webhook set to: {webhook_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            return False
    
    async def get_webhook_info(self):
        """Get webhook information"""
        try:
            webhook_info = await self.app.bot.get_webhook_info()
            logger.info(f"Webhook info: {webhook_info}")
            return webhook_info
        except Exception as e:
            logger.error(f"Failed to get webhook info: {e}")
            return None
    
    def create_app(self):
        """Create and configure the bot application"""
        self.app = Application.builder().token(config.BOT_TOKEN).build()
        self.setup_handlers()
        return self.app

# Global bot handler instance
bot_handler = TelegramBotHandler()

def get_bot_info():
    """Get bot information for configuration"""
    return {
        "bot_token": config.BOT_TOKEN,
        "webapp_url": config.get_mini_app_url(),
        "webhook_url": config.get_webhook_url(),
        "mini_app_title": config.MINI_APP_TITLE,
        "mini_app_description": config.MINI_APP_DESCRIPTION,
        "mini_app_short_name": config.MINI_APP_SHORT_NAME
    }

async def main():
    """Main function to run the bot"""
    app = bot_handler.create_app()
    
    # Setup webhook
    await bot_handler.setup_webhook()
    
    # Get webhook info
    await bot_handler.get_webhook_info()
    
    logger.info("Bot is ready!")
    logger.info(f"Mini App URL: {config.get_mini_app_url()}")
    logger.info(f"Webhook URL: {config.get_webhook_url()}")
    
    # Start the bot
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
