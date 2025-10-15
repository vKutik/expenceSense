#!/usr/bin/env python3
"""
Simple Webhook Handler for Telegram Bot
Runs locally to handle webhook requests
"""

from flask import Flask, request, jsonify
import requests
import json

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

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """Handle webhook requests"""
    if request.method == 'GET':
        return jsonify({"status": "webhook_ready"})
    
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
            username = message["from"].get("username", "User")
            
            print(f"Processing message: {text} from {username}")
            
            if text == "/start":
                handle_start(chat_id, username)
            elif text == "/help":
                handle_help(chat_id)
            elif text == "/about":
                send_message(chat_id, "🤖 <b>About SpendSense</b>\n\nVersion 1.0 - Expense tracking bot with Mini App integration!")
            elif text == "/settings":
                send_message(chat_id, "⚙️ <b>Settings</b>\n\nOpen the Mini App to access settings!")
            elif text == "/stats":
                send_message(chat_id, "📊 <b>Statistics</b>\n\nOpen the Mini App to view detailed statistics!")
            else:
                send_message(chat_id, "I don't understand that command. Send /help for available commands.")
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting webhook server...")
    print("Webhook URL: http://localhost:5000/webhook")
    app.run(host='0.0.0.0', port=5000, debug=True)
