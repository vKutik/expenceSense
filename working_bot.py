"""
Working Telegram Bot - Processes messages and responds
"""
import requests
import time
import json

BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"
MINI_APP_URL = "https://snake-gcaeog0dh-volodymyr-s-projects-9f0184a4.vercel.app"
USER_ID = 489146762  # Your Telegram ID

def send_message(chat_id, text, reply_markup=None):
    """Send message to user"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(url, json=data)
    return response.json()

def send_start_message(chat_id):
    """Send start message with Mini App button"""
    
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "📱 Open Expense Tracker",
                    "web_app": {
                        "url": MINI_APP_URL
                    }
                }
            ]
        ]
    }
    
    message = """
👋 *Welcome to Expense Tracker!*

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
    
    return send_message(chat_id, message, keyboard)

def send_help_message(chat_id):
    """Send help message"""
    message = """
*Expense Tracker Bot Commands:*

/start - Open the expense tracker app
/help - Show this help message
/about - About the application
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

*Need help?* Contact support
"""
    
    return send_message(chat_id, message)

def send_about_message(chat_id):
    """Send about message"""
    message = """
*Expense Tracker v1.2*

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
*Version:* 1.2.0
*Last Updated:* October 2024
"""
    
    return send_message(chat_id, message)

def process_message(update):
    """Process incoming message"""
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')
    
    print(f"Processing message from {chat_id}: {text}")
    
    if text == '/start':
        result = send_start_message(chat_id)
        print(f"Start message sent: {result.get('ok', False)}")
        
    elif text == '/help':
        result = send_help_message(chat_id)
        print(f"Help message sent: {result.get('ok', False)}")
        
    elif text == '/about':
        result = send_about_message(chat_id)
        print(f"About message sent: {result.get('ok', False)}")
        
    else:
        # Respond to any other message
        result = send_message(chat_id, 
            "Hi! 👋\n\nUse /start to open the Expense Tracker app!\n\n*Commands:*\n/start - Open app\n/help - Help\n/about - About")
        print(f"Generic response sent: {result.get('ok', False)}")

def get_updates(offset=None):
    """Get updates from Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {}
    if offset:
        params['offset'] = offset
    
    response = requests.get(url, params=params)
    return response.json()

def main():
    """Main bot loop"""
    print("🤖 Starting Working Bot...")
    print(f"📱 Mini App URL: {MINI_APP_URL}")
    print(f"👤 User ID: {USER_ID}")
    print("=" * 40)
    
    last_update_id = None
    
    # Send a welcome message first
    print("📤 Sending welcome message...")
    result = send_start_message(USER_ID)
    if result.get('ok'):
        print("✅ Welcome message sent!")
    else:
        print(f"❌ Failed to send welcome: {result}")
    
    while True:
        try:
            # Get updates
            updates = get_updates(offset=last_update_id)
            
            if not updates.get('ok'):
                print(f"❌ Error getting updates: {updates}")
                time.sleep(5)
                continue
            
            update_list = updates.get('result', [])
            
            if update_list:
                print(f"📨 Processing {len(update_list)} updates...")
                
                for update in update_list:
                    last_update_id = update.get('update_id') + 1
                    process_message(update)
            else:
                print("⏱️ No new updates, waiting...")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n👋 Bot stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
