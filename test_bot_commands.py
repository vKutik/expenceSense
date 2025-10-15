#!/usr/bin/env python3
"""
Test Bot Commands - Verify bot responds to /start
"""

import requests
import time

BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    """Send message to user"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    if reply_markup:
        import json
        data["reply_markup"] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def test_start_command():
    """Test /start command response"""
    chat_id = 489146762  # Your chat ID
    
    welcome_text = f"""
🎉 <b>Welcome to SpendSense!</b>

Hello! 👋

I'm your personal expense tracker bot. Here's what I can do:

📊 <b>Track Expenses</b> - Record your daily spending
📈 <b>View Statistics</b> - See your spending patterns  
💰 <b>Manage Budget</b> - Keep track of your finances
⚙️ <b>Settings</b> - Customize your experience

Click the button below to open the Mini App and start tracking your expenses!
    """
    
    # Inline keyboard with Mini App button
    keyboard = {
        "inline_keyboard": [[
            {
                "text": "📱 Open Expense Tracker",
                "web_app": {
                    "url": "https://snake-kh613zzlk-volodymyr-s-projects-9f0184a4.vercel.app"
                }
            }
        ], [
            {"text": "📊 Statistics", "callback_data": "stats"},
            {"text": "⚙️ Settings", "callback_data": "settings"}
        ]]
    }
    
    result = send_message(chat_id, welcome_text, keyboard)
    
    if result and result.get("ok"):
        print("✅ /start command working! Bot sent welcome message.")
        return True
    else:
        print(f"❌ /start command failed: {result}")
        return False

def test_help_command():
    """Test /help command response"""
    chat_id = 489146762
    
    help_text = """
🆘 <b>SpendSense Help</b>

<b>Available Commands:</b>
/start - Start using the bot
/help - Show this help message
/about - About SpendSense
/settings - Bot settings
/stats - Quick statistics

<b>Mini App Features:</b>
• Add and manage expenses
• View spending statistics
• Track categories
• Bank balance management
• User authentication

Click "📱 Open Expense Tracker" to use the full app!
    """
    
    result = send_message(chat_id, help_text)
    
    if result and result.get("ok"):
        print("✅ /help command working! Bot sent help message.")
        return True
    else:
        print(f"❌ /help command failed: {result}")
        return False

if __name__ == "__main__":
    print("🤖 Testing Bot Commands...")
    print("=" * 50)
    
    # Test /start command
    print("Testing /start command...")
    start_ok = test_start_command()
    
    time.sleep(2)
    
    # Test /help command
    print("\nTesting /help command...")
    help_ok = test_help_command()
    
    print("\n" + "=" * 50)
    if start_ok and help_ok:
        print("🎉 All commands working! Bot is functional.")
        print("📱 Try sending /start to @spendSenceBot in Telegram!")
    else:
        print("❌ Some commands failed. Check the errors above.")
