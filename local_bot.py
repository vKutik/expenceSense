#!/usr/bin/env python3
"""
Local Telegram Bot - Simple version for testing
"""

import requests
import time
import json

# Bot configuration
BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    """Get updates from Telegram"""
    url = f"{BASE_URL}/getUpdates"
    params = {"offset": offset, "timeout": 30}
    
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return None

def send_message(chat_id, text, reply_markup=None):
    """Send message to user"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def handle_start(chat_id, username):
    """Handle /start command"""
    welcome_text = f"""
🎉 <b>Welcome to SpendSense!</b>

Hello {username}! 👋

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
    
    return send_message(chat_id, welcome_text, keyboard)

def handle_help(chat_id):
    """Handle /help command"""
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
    
    return send_message(chat_id, help_text)

def handle_about(chat_id):
    """Handle /about command"""
    about_text = """
🤖 <b>About SpendSense</b>

<b>Version:</b> 1.0
<b>Framework:</b> Flask + Telegram Mini App
<b>Features:</b> 
• Modern design patterns (MVC, Repository, Service Layer)
• Multi-storage system (Memory, File, Database, Cloud)
• User authentication levels
• Real-time expense tracking
• Bank balance management

Built with ❤️ for expense management
    """
    
    return send_message(chat_id, about_text)

def handle_callback(callback_query):
    """Handle callback queries"""
    chat_id = callback_query["message"]["chat"]["id"]
    data = callback_query["data"]
    
    if data == "stats":
        send_message(chat_id, "📊 <b>Statistics</b>\n\nOpen the Mini App to view detailed statistics!")
    elif data == "settings":
        send_message(chat_id, "⚙️ <b>Settings</b>\n\nOpen the Mini App to access settings!")

def process_updates(updates):
    """Process incoming updates"""
    for update in updates.get("result", []):
        update_id = update["update_id"]
        
        # Handle messages
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            username = message["from"].get("username", "User")
            
            print(f"Received message: {text} from {username}")
            
            if text == "/start":
                handle_start(chat_id, username)
            elif text == "/help":
                handle_help(chat_id)
            elif text == "/about":
                handle_about(chat_id)
            elif text == "/settings":
                send_message(chat_id, "⚙️ <b>Settings</b>\n\nOpen the Mini App to access settings!")
            elif text == "/stats":
                send_message(chat_id, "📊 <b>Statistics</b>\n\nOpen the Mini App to view detailed statistics!")
            else:
                send_message(chat_id, "I don't understand that command. Send /help for available commands.")
        
        # Handle callback queries
        elif "callback_query" in update:
            callback_query = update["callback_query"]
            handle_callback(callback_query)
        
        return update_id
    
    return None

def main():
    """Main bot loop"""
    print("🤖 SpendSense Bot Started!")
    print("Press Ctrl+C to stop")
    
    last_update_id = None
    
    try:
        while True:
            updates = get_updates(last_update_id)
            
            if updates and updates.get("ok"):
                last_update_id = process_updates(updates)
                if last_update_id:
                    last_update_id += 1
            else:
                print("No updates or error occurred")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()
