#!/usr/bin/env python3
"""
Public Mini App for Telegram
Simple Flask app without authentication protection
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

# Simple HTML template for Mini App
MINI_APP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpendSense - Expense Tracker</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #ffffff;
            color: #000000;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 400px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: #000000;
            color: #ffffff;
            padding: 20px;
            text-align: center;
        }

        .user-info {
            background: #f8f9fa;
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }

        .user-name {
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 5px;
        }

        .user-details {
            font-size: 14px;
            color: #666666;
        }

        .content {
            padding: 20px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #000000;
        }

        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #000000;
            border-radius: 10px;
            font-size: 16px;
            background: #ffffff;
            color: #000000;
        }

        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #007bff;
        }

        .btn {
            background: #000000;
            color: #ffffff;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }

        .btn:hover {
            background: #333333;
        }

        .expense-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border: 2px solid #000000;
        }

        .expense-amount {
            font-size: 18px;
            font-weight: bold;
            color: #000000;
        }

        .expense-category {
            font-size: 14px;
            color: #666666;
            margin-top: 5px;
        }

        .stats {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border: 2px solid #000000;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }

        .hidden {
            display: none;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #666666;
        }

        .error {
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            border: 2px solid #c62828;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 SpendSense</h1>
            <p>Personal Expense Tracker</p>
        </div>

        <div class="user-info">
            <div class="user-name" id="userName">Loading...</div>
            <div class="user-details" id="userDetails">Loading...</div>
        </div>

        <div class="content">
            <!-- Add Expense Form -->
            <div class="form-group">
                <h3>Add New Expense</h3>
            </div>
            <div class="form-group">
                <label for="expenseAmount">Amount</label>
                <input type="number" id="expenseAmount" placeholder="0.00" step="0.01">
            </div>
            <div class="form-group">
                <label for="expenseCategory">Category</label>
                <select id="expenseCategory">
                    <option value="food">🍕 Food</option>
                    <option value="transport">🚗 Transport</option>
                    <option value="shopping">🛍️ Shopping</option>
                    <option value="entertainment">🎬 Entertainment</option>
                    <option value="utilities">⚡ Utilities</option>
                    <option value="health">🏥 Health</option>
                    <option value="other">📝 Other</option>
                </select>
            </div>
            <div class="form-group">
                <label for="expenseDescription">Description (optional)</label>
                <textarea id="expenseDescription" placeholder="What did you spend on?" rows="3"></textarea>
            </div>
            <button class="btn" onclick="addExpense()">Add Expense</button>

            <!-- Statistics -->
            <div class="stats">
                <h3>📊 Statistics</h3>
                <div class="stat-item">
                    <span>Total Spent:</span>
                    <span id="totalSpent">$0.00</span>
                </div>
                <div class="stat-item">
                    <span>Transactions:</span>
                    <span id="transactionCount">0</span>
                </div>
            </div>

            <!-- Expense List -->
            <div>
                <h3>Recent Expenses</h3>
                <div id="expenseList">
                    <div class="loading">No expenses yet. Add your first expense!</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let expenses = [];
        let currentUser = null;

        // Initialize the app
        function initApp() {
            try {
                // Get Telegram WebApp data
                const initData = window.Telegram?.WebApp?.initData || '';
                const telegramData = window.Telegram?.WebApp?.initDataUnsafe || {};
                const user = window.Telegram?.WebApp?.initDataUnsafe?.user || {};
                
                console.log('Telegram WebApp available:', !!window.Telegram?.WebApp);
                console.log('Telegram user data:', user);
                
                if (user && user.id) {
                    // Use real Telegram user data
                    currentUser = {
                        id: user.id,
                        first_name: user.first_name || 'User',
                        last_name: user.last_name || '',
                        username: user.username || 'user'
                    };
                    
                    // Update UI with real Telegram data
                    document.getElementById('userName').textContent = 
                        `${currentUser.first_name} ${currentUser.last_name || ''}`.trim();
                    document.getElementById('userDetails').textContent = 
                        `@${currentUser.username}`;
                    
                    console.log('✅ Using real Telegram user data:', currentUser);
                } else {
                    // Fallback for testing
                    currentUser = {
                        id: 1,
                        first_name: 'Guest',
                        last_name: 'User',
                        username: 'guest'
                    };
                    
                    document.getElementById('userName').textContent = 'Guest User';
                    document.getElementById('userDetails').textContent = '@guest';
                    
                    console.log('⚠️ Using fallback user data');
                }
                
                // Configure Telegram WebApp
                if (window.Telegram?.WebApp) {
                    window.Telegram.WebApp.ready();
                    window.Telegram.WebApp.expand();
                }
                
                // Load expenses from localStorage
                loadExpenses();
                updateStats();
                
            } catch (error) {
                console.error('Error initializing app:', error);
                showError('Failed to initialize app');
            }
        }

        function addExpense() {
            const amount = parseFloat(document.getElementById('expenseAmount').value);
            const category = document.getElementById('expenseCategory').value;
            const description = document.getElementById('expenseDescription').value;

            if (!amount || amount <= 0) {
                showError('Please enter a valid amount');
                return;
            }

            const expense = {
                id: Date.now(),
                amount: amount,
                category: category,
                description: description,
                date: new Date().toISOString(),
                user_id: currentUser ? currentUser.id : 1
            };

            expenses.push(expense);
            saveExpenses();
            updateStats();
            updateExpenseList();
            
            // Clear form
            document.getElementById('expenseAmount').value = '';
            document.getElementById('expenseDescription').value = '';
            
            console.log('✅ Expense added:', expense);
        }

        function loadExpenses() {
            const saved = localStorage.getItem('expenses');
            if (saved) {
                expenses = JSON.parse(saved);
                updateExpenseList();
            }
        }

        function saveExpenses() {
            localStorage.setItem('expenses', JSON.stringify(expenses));
        }

        function updateStats() {
            const total = expenses.reduce((sum, expense) => sum + expense.amount, 0);
            document.getElementById('totalSpent').textContent = `$${total.toFixed(2)}`;
            document.getElementById('transactionCount').textContent = expenses.length;
        }

        function updateExpenseList() {
            const list = document.getElementById('expenseList');
            
            if (expenses.length === 0) {
                list.innerHTML = '<div class="loading">No expenses yet. Add your first expense!</div>';
                return;
            }

            list.innerHTML = expenses.slice(-10).reverse().map(expense => `
                <div class="expense-item">
                    <div class="expense-amount">$${expense.amount.toFixed(2)}</div>
                    <div class="expense-category">
                        ${getCategoryEmoji(expense.category)} ${expense.category} 
                        ${expense.description ? ' - ' + expense.description : ''}
                    </div>
                </div>
            `).join('');
        }

        function getCategoryEmoji(category) {
            const emojis = {
                food: '🍕',
                transport: '🚗',
                shopping: '🛍️',
                entertainment: '🎬',
                utilities: '⚡',
                health: '🏥',
                other: '📝'
            };
            return emojis[category] || '📝';
        }

        function showError(message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = message;
            document.querySelector('.content').insertBefore(errorDiv, document.querySelector('.content').firstChild);
            
            setTimeout(() => {
                errorDiv.remove();
            }, 3000);
        }

        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', initApp);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the Mini App"""
    return render_template_string(MINI_APP_HTML)

@app.route('/api/expenses', methods=['GET', 'POST'])
def expenses():
    """API endpoint for expenses"""
    if request.method == 'POST':
        # Handle expense creation
        data = request.get_json()
        return jsonify({"success": True, "message": "Expense saved"})
    
    return jsonify({"expenses": []})

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "public-mini-app"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🌐 Starting Public Mini App on port {port}...")
    print("📱 Accessible without authentication")
    print("🚀 Ready to serve Telegram Mini App!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
