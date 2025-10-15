"""
Expense Tracker Web App
Modern phone interface for expense tracking
"""
import os
import hmac
import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from telegram_bot import bot_handler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"
DATABASE_PATH = 'expenses.db'

# In-memory storage for demo (replace with database in production)
users_db = {}
expenses_db = {}
categories_db = {}

# Default categories
DEFAULT_CATEGORIES = [
    {'id': 1, 'name': 'Food', 'emoji': '🍕', 'color': '#FF6B6B'},
    {'id': 2, 'name': 'Transport', 'emoji': '🚗', 'color': '#4ECDC4'},
    {'id': 3, 'name': 'Shopping', 'emoji': '🛍️', 'color': '#45B7D1'},
    {'id': 4, 'name': 'Entertainment', 'emoji': '🎬', 'color': '#96CEB4'},
    {'id': 5, 'name': 'Health', 'emoji': '🏥', 'color': '#FFEAA7'},
    {'id': 6, 'name': 'Utilities', 'emoji': '⚡', 'color': '#DDA0DD'},
    {'id': 7, 'name': 'Other', 'emoji': '📦', 'color': '#98D8C8'}
]

def verify_telegram_webapp_data(init_data: str, bot_token: str) -> Optional[Dict[str, str]]:
    """
    Verifies the authenticity of data received from Telegram Mini Apps.
    https://core.telegram.org/bots/webapps#checking-authorization
    """
    if not init_data:
        return None

    data_check_string = []
    data = {}
    
    # Parse init_data
    for param in init_data.split('&'):
        key, value = param.split('=', 1)
        key = key.strip()
        value = value.strip()
        data[key] = value
        if key != 'hash':
            data_check_string.append(f"{key}={value}")

    data_check_string.sort()
    data_check_string = "\n".join(data_check_string)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    
    if h.hexdigest() == data.get('hash'):
        user_data = json.loads(data.get('user', '{}'))
        if user_data:
            return {
                'id': user_data.get('id'),
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'username': user_data.get('username'),
                'language_code': user_data.get('language_code')
            }
        return None
    return None

@app.route('/')
def index():
    """Main Mini App page."""
    return render_template('index.html')

@app.route('/api/init', methods=['POST'])
def init_app():
    """Initialize the Mini App with user data."""
    try:
        init_data = request.json.get('initData', '')
        if not init_data:
            return jsonify({'error': 'No init data provided'}), 400
        
        # Authenticate user
        user_data = verify_telegram_webapp_data(init_data, BOT_TOKEN)
        if not user_data:
            return jsonify({'error': 'Invalid Telegram data'}), 401
        
        user_id = user_data['id']
        
        # Create or get user
        if user_id not in users_db:
            users_db[user_id] = {
                'id': user_id,
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'username': user_data.get('username'),
                'language_code': user_data.get('language_code'),
                'created_at': datetime.now().isoformat()
            }
            expenses_db[user_id] = []
            logger.info(f"New user created: {user_id}")
        
        return jsonify({
            'success': True,
            'user': users_db[user_id],
            'categories': DEFAULT_CATEGORIES
        })
        
    except Exception as e:
        logger.error(f"Error in init_app: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get user expenses."""
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        user_id = int(user_id)
        expenses = expenses_db.get(user_id, [])
        
        # Add category info to expenses
        for expense in expenses:
            category = next((cat for cat in DEFAULT_CATEGORIES if cat['id'] == expense['category_id']), None)
            expense['category'] = category
        
        return jsonify({
            'success': True,
            'expenses': expenses,
            'total': sum(expense['amount'] for expense in expenses)
        })
        
    except Exception as e:
        logger.error(f"Error getting expenses: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    """Add new expense."""
    try:
        data = request.json
        user_id = data.get('userId')
        amount = data.get('amount')
        category_id = data.get('categoryId')
        description = data.get('description', '')
        
        if not all([user_id, amount, category_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user_id = int(user_id)
        amount = float(amount)
        category_id = int(category_id)
        
        # Create expense
        expense = {
            'id': len(expenses_db.get(user_id, [])) + 1,
            'user_id': user_id,
            'amount': amount,
            'category_id': category_id,
            'description': description,
            'date': datetime.now().isoformat()
        }
        
        if user_id not in expenses_db:
            expenses_db[user_id] = []
        
        expenses_db[user_id].append(expense)
        
        # Add category info
        category = next((cat for cat in DEFAULT_CATEGORIES if cat['id'] == category_id), None)
        expense['category'] = category
        
        logger.info(f"Expense added: {expense}")
        
        return jsonify({
            'success': True,
            'expense': expense
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        user_id = int(user_id)
        expenses = expenses_db.get(user_id, [])
        
        # Find and remove expense
        for i, expense in enumerate(expenses):
            if expense['id'] == expense_id:
                del expenses[i]
                logger.info(f"Expense deleted: {expense_id}")
                return jsonify({'success': True})
        
        return jsonify({'error': 'Expense not found'}), 404
        
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available categories."""
    return jsonify({
        'success': True,
        'categories': DEFAULT_CATEGORIES
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get user statistics."""
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        user_id = int(user_id)
        expenses = expenses_db.get(user_id, [])
        
        # Calculate stats
        total = sum(expense['amount'] for expense in expenses)
        category_totals = {}
        
        for expense in expenses:
            cat_id = expense['category_id']
            if cat_id not in category_totals:
                category_totals[cat_id] = 0
            category_totals[cat_id] += expense['amount']
        
        # Add category info to stats
        stats = []
        for cat_id, amount in category_totals.items():
            category = next((cat for cat in DEFAULT_CATEGORIES if cat['id'] == cat_id), None)
            if category:
                stats.append({
                    'category': category,
                    'amount': amount,
                    'percentage': (amount / total * 100) if total > 0 else 0
                })
        
        return jsonify({
            'success': True,
            'total': total,
            'count': len(expenses),
            'category_stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return controllers['health'].health_check()

@app.route('/api/balance', methods=['GET'])
def get_bank_balance():
    """Get user's bank balance."""
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    return controllers['balance'].get_balance(int(user_id))

@app.route('/api/balance', methods=['POST'])
def update_bank_balance():
    """Update user's bank balance."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    user_id = data.get('userId')
    new_balance = data.get('balance')
    
    if not user_id or new_balance is None:
        return jsonify({'error': 'User ID and balance required'}), 400
    
    try:
        new_balance = float(new_balance)
    except (ValueError, TypeError):
        return jsonify({'error': 'Balance must be a valid number'}), 400
    
    return controllers['balance'].update_balance(int(user_id), new_balance)

@app.route('/webhook', methods=['POST'])
async def telegram_webhook():
    """Handle Telegram webhook updates"""
    try:
        if request.method == "POST":
            # Get the update from Telegram
            update_data = request.get_json()
            
            # Process the update through the bot handler
            await bot_handler.webhook_handler(update_data, None)
            
            return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/setup', methods=['POST'])
async def setup_bot():
    """Setup bot webhook and mini app"""
    try:
        # Setup webhook
        success = await bot_handler.setup_webhook()
        
        if success:
            return jsonify({
                "success": True,
                "message": "Bot webhook configured successfully",
                "webhook_url": bot_handler.config.get_webhook_url(),
                "mini_app_url": bot_handler.config.get_mini_app_url()
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to setup webhook"
            }), 500
    except Exception as e:
        logger.error(f"Bot setup error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/info', methods=['GET'])
def get_bot_info():
    """Get bot configuration information"""
    from telegram_bot import get_bot_info
    return jsonify(get_bot_info())

if __name__ == '__main__':
    print("🚀 Starting Telegram Mini App with Clean Architecture...")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print("📱 Phone Interface: Modern mobile-first design")
    print("🏗️ Architecture: MVC + Repository + Service + Observer patterns")
    print("🔐 Account Login: Telegram authentication")
    print("💰 Expense Tracker: Full functionality with event system")
    print("🌐 Web App: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
