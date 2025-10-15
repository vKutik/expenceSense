#!/usr/bin/env python3
"""
Standalone Webhook Handler for Telegram Bot
This runs independently to handle webhook requests
"""

from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Bot configuration
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
        data["reply_markup"] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def handle_start(chat_id, username, first_name):
    """Handle /start command"""
    welcome_text = f"""
🎉 <b>Welcome to SpendSense!</b>

Hello {first_name}! 👋

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
                    "url": "https://snake-ofgsh5b83-volodymyr-s-projects-9f0184a4.vercel.app"
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

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """Handle webhook requests"""
    if request.method == 'GET':
        return jsonify({"status": "webhook_ready", "message": "Telegram webhook handler is running"})
    
    try:
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({"status": "no_data"}), 400
        
        print(f"Received update: {update_data}")
        
        # Handle messages
        if "message" in update_data:
            message = update_data["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            user = message.get("from", {})
            username = user.get("username", "User")
            first_name = user.get("first_name", "User")
            
            print(f"Processing message: {text} from {first_name} (@{username})")
            
            if text == "/start":
                result = handle_start(chat_id, username, first_name)
                if result and result.get("ok"):
                    print("✅ /start command processed successfully")
                else:
                    print(f"❌ /start command failed: {result}")
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
        elif "callback_query" in update_data:
            callback_query = update_data["callback_query"]
            chat_id = callback_query["message"]["chat"]["id"]
            data = callback_query["data"]
            
            if data == "stats":
                send_message(chat_id, "📊 <b>Statistics</b>\n\nOpen the Mini App to view detailed statistics!")
            elif data == "settings":
                send_message(chat_id, "⚙️ <b>Settings</b>\n\nOpen the Mini App to access settings!")
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "telegram-webhook"})

if __name__ == '__main__':
    print("🌐 Starting Telegram Webhook Handler...")
    print("🔗 Webhook URL: http://localhost:5000/webhook")
    print("📱 Bot: @spendSenceBot")
    print("🚀 Ready to handle Telegram updates!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
