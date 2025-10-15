#!/usr/bin/env python3
"""
Deploy Solution for Telegram Mini App
This creates a simple public hosting solution
"""

from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Mini App HTML with real Telegram user data
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
            text-align: center;
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

        .debug-info {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-size: 12px;
            color: #1976d2;
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
            <!-- Debug Info -->
            <div class="debug-info" id="debugInfo">
                <strong>Debug Info:</strong><br>
                Telegram WebApp: <span id="telegramStatus">Checking...</span><br>
                User Data: <span id="userDataStatus">Checking...</span>
            </div>

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
                    <div style="text-align: center; padding: 20px; color: #666;">No expenses yet. Add your first expense!</div>
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
                // Check Telegram WebApp availability
                const hasTelegram = !!window.Telegram?.WebApp;
                document.getElementById('telegramStatus').textContent = hasTelegram ? 'Available ✅' : 'Not Available ❌';
                
                if (hasTelegram) {
                    // Get Telegram WebApp data
                    const initData = window.Telegram?.WebApp?.initData || '';
                    const telegramData = window.Telegram?.WebApp?.initDataUnsafe || {};
                    const user = window.Telegram?.WebApp?.initDataUnsafe?.user || {};
                    
                    console.log('=== TELEGRAM DEBUG INFO ===');
                    console.log('Telegram WebApp available:', hasTelegram);
                    console.log('initData:', initData);
                    console.log('telegramData:', telegramData);
                    console.log('user:', user);
                    console.log('============================');
                    
                    document.getElementById('userDataStatus').textContent = user.id ? 'Available ✅' : 'Not Available ❌';
                    
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
                        
                        console.log('✅ Using REAL Telegram user data:', currentUser);
                    } else {
                        // No user data available
                        currentUser = {
                            id: 1,
                            first_name: 'Guest',
                            last_name: 'User',
                            username: 'guest'
                        };
                        
                        document.getElementById('userName').textContent = 'Guest User';
                        document.getElementById('userDetails').textContent = '@guest';
                        
                        console.log('⚠️ No Telegram user data, using fallback');
                    }
                    
                    // Configure Telegram WebApp
                    window.Telegram.WebApp.ready();
                    window.Telegram.WebApp.expand();
                } else {
                    // Not in Telegram environment
                    currentUser = {
                        id: 1,
                        first_name: 'Test',
                        last_name: 'User',
                        username: 'testuser'
                    };
                    
                    document.getElementById('userName').textContent = 'Test User';
                    document.getElementById('userDetails').textContent = '@testuser';
                    document.getElementById('userDataStatus').textContent = 'Not in Telegram ❌';
                    
                    console.log('⚠️ Not in Telegram environment');
                }
                
                // Load expenses from localStorage
                loadExpenses();
                updateStats();
                
            } catch (error) {
                console.error('Error initializing app:', error);
                document.getElementById('userName').textContent = 'Error';
                document.getElementById('userDetails').textContent = 'Failed to load';
            }
        }

        function addExpense() {
            const amount = parseFloat(document.getElementById('expenseAmount').value);
            const category = document.getElementById('expenseCategory').value;
            const description = document.getElementById('expenseDescription').value;

            if (!amount || amount <= 0) {
                alert('Please enter a valid amount');
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
                list.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">No expenses yet. Add your first expense!</div>';
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

@app.route('/health')
def health():
    """Health check"""
    return {"status": "healthy", "service": "telegram-mini-app"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"🌐 Starting Telegram Mini App on port {port}...")
    print("📱 Shows REAL Telegram username")
    print("🚀 Ready to serve!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
