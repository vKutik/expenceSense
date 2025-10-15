"""
Bot Setup Script for Telegram Mini App
"""
import asyncio
import requests
import json
from telegram_bot import bot_handler, config

async def setup_webhook():
    """Setup webhook for the bot"""
    print("🔧 Setting up Telegram bot webhook...")
    
    try:
        # Create bot app
        app = bot_handler.create_app()
        
        # Setup webhook
        success = await bot_handler.setup_webhook()
        
        if success:
            print("✅ Webhook configured successfully!")
            print(f"   Webhook URL: {config.get_webhook_url()}")
            print(f"   Mini App URL: {config.get_mini_app_url()}")
            
            # Get webhook info
            webhook_info = await bot_handler.get_webhook_info()
            if webhook_info:
                print(f"   Webhook Info: {webhook_info}")
            
            return True
        else:
            print("❌ Failed to setup webhook")
            return False
            
    except Exception as e:
        print(f"❌ Error setting up webhook: {e}")
        return False

def setup_mini_app():
    """Setup mini app configuration"""
    print("\n📱 Setting up Mini App configuration...")
    
    mini_app_config = {
        "title": config.MINI_APP_TITLE,
        "description": config.MINI_APP_DESCRIPTION,
        "short_name": config.MINI_APP_SHORT_NAME,
        "url": config.get_mini_app_url(),
        "webhook_url": config.get_webhook_url()
    }
    
    print("✅ Mini App configuration:")
    for key, value in mini_app_config.items():
        print(f"   {key}: {value}")
    
    return mini_app_config

def create_bot_commands():
    """Create bot commands menu"""
    print("\n🤖 Setting up bot commands...")
    
    commands = [
        {"command": "start", "description": "Open the Expense Tracker app"},
        {"command": "help", "description": "Show help and available commands"},
        {"command": "about", "description": "About the application"},
        {"command": "settings", "description": "Bot and app settings"},
        {"command": "stats", "description": "Quick expense statistics"}
    ]
    
    print("✅ Bot commands configured:")
    for cmd in commands:
        print(f"   /{cmd['command']} - {cmd['description']}")
    
    return commands

def print_manual_setup():
    """Print manual setup instructions"""
    print("\n📋 Manual Setup Instructions:")
    print("=" * 50)
    
    print("\n1. 🤖 Bot Configuration:")
    print("   - Go to @BotFather on Telegram")
    print("   - Send /newapp")
    print(f"   - Bot: @your_bot_username")
    print(f"   - Title: {config.MINI_APP_TITLE}")
    print(f"   - Description: {config.MINI_APP_DESCRIPTION}")
    print(f"   - Photo: Upload app icon (optional)")
    print(f"   - Web App URL: {config.get_mini_app_url()}")
    
    print("\n2. 🔗 Webhook Setup:")
    print(f"   - Webhook URL: {config.get_webhook_url()}")
    print("   - Method: POST")
    print("   - Content-Type: application/json")
    
    print("\n3. 📱 Mini App Features:")
    print("   - Automatic Telegram authentication")
    print("   - User level detection (Guest/Registered/Premium/Admin)")
    print("   - Multi-storage system based on user level")
    print("   - Real-time expense tracking")
    print("   - Statistics and analytics")
    
    print("\n4. 🧪 Testing:")
    print("   - Send /start to your bot")
    print("   - Tap 'Open Expense Tracker' button")
    print("   - Verify automatic authentication")
    print("   - Test expense creation and viewing")
    
    print("\n5. 🔧 Environment Variables:")
    print("   - BOT_TOKEN: Your Telegram bot token")
    print("   - WEBAPP_URL: Your deployed app URL")
    print("   - WEBHOOK_URL: Your webhook endpoint")

async def main():
    """Main setup function"""
    print("🚀 Telegram Bot & Mini App Setup")
    print("=" * 50)
    
    # Setup webhook
    webhook_success = await setup_webhook()
    
    # Setup mini app config
    mini_app_config = setup_mini_app()
    
    # Setup bot commands
    commands = create_bot_commands()
    
    # Print manual setup instructions
    print_manual_setup()
    
    print("\n" + "=" * 50)
    if webhook_success:
        print("✅ Setup completed successfully!")
        print("📱 Your Mini App is ready to use")
        print(f"🔗 Test it: {config.get_mini_app_url()}")
    else:
        print("⚠️  Setup completed with warnings")
        print("📋 Please follow manual setup instructions above")
    
    print("\n🎯 Next Steps:")
    print("1. Configure Mini App with @BotFather")
    print("2. Test the bot with /start command")
    print("3. Verify automatic authentication works")
    print("4. Deploy to production environment")

if __name__ == "__main__":
    asyncio.run(main())
