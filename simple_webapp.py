"""
Simple Expense Tracker Web App
No authentication required - works as standalone web app
"""
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# In-memory storage
expenses_db = [
    {
        'id': 1,
        'amount': 1200.00,
        'category_id': 7,
        'category': {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
        'description': 'Monthly rent payment',
        'date': '2024-01-01T00:00:00'
    },
    {
        'id': 2,
        'amount': 1200.00,
        'category_id': 7,
        'category': {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
        'description': 'Monthly rent payment',
        'date': '2024-02-01T00:00:00'
    },
    {
        'id': 3,
        'amount': 1200.00,
        'category_id': 7,
        'category': {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
        'description': 'Monthly rent payment',
        'date': '2024-03-01T00:00:00'
    },
    {
        'id': 4,
        'amount': 1200.00,
        'category_id': 7,
        'category': {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
        'description': 'Monthly rent payment',
        'date': '2024-04-01T00:00:00'
    },
    {
        'id': 5,
        'amount': 1200.00,
        'category_id': 7,
        'category': {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
        'description': 'Monthly rent payment',
        'date': '2024-05-01T00:00:00'
    },
    {
        'id': 6,
        'amount': 1200.00,
        'category_id': 7,
        'category': {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
        'description': 'Monthly rent payment',
        'date': '2024-06-01T00:00:00'
    }
]
categories_db = [
    {'id': 1, 'name': 'Food', 'emoji': '🍕', 'color': '#FF6B6B'},
    {'id': 2, 'name': 'Transport', 'emoji': '🚗', 'color': '#4ECDC4'},
    {'id': 3, 'name': 'Shopping', 'emoji': '🛍️', 'color': '#45B7D1'},
    {'id': 4, 'name': 'Entertainment', 'emoji': '🎬', 'color': '#96CEB4'},
    {'id': 5, 'name': 'Health', 'emoji': '🏥', 'color': '#FFEAA7'},
    {'id': 6, 'name': 'Utilities', 'emoji': '⚡', 'color': '#DDA0DD'},
    {'id': 7, 'name': 'Rent', 'emoji': '🏠', 'color': '#FF8C42'},
    {'id': 8, 'name': 'Other', 'emoji': '📦', 'color': '#98D8C8'}
]

@app.route('/')
def index():
    """Main page."""
    return render_template('simple_index.html')

@app.route('/categories')
def categories():
    """Categories management page."""
    return render_template('categories.html')

@app.route('/statistics')
def statistics():
    """Statistics page."""
    return render_template('statistics.html')

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available categories."""
    return jsonify({
        'success': True,
        'categories': categories_db
    })

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses."""
    try:
        total = sum(expense['amount'] for expense in expenses_db)
        return jsonify({
            'success': True,
            'expenses': expenses_db,
            'total': total
        })
    except Exception as e:
        logger.error(f"Error getting expenses: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    """Add new expense."""
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        category_id = int(data.get('category_id', 0))
        description = data.get('description', '')
        
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
        
        # Find category
        category = next((cat for cat in categories_db if cat['id'] == category_id), None)
        if not category:
            return jsonify({'error': 'Invalid category'}), 400
        
        expense = {
            'id': len(expenses_db) + 1,
            'amount': amount,
            'category_id': category_id,
            'category': category,
            'description': description,
            'date': datetime.now().isoformat()
        }
        
        expenses_db.append(expense)
        
        return jsonify({
            'success': True,
            'expense': expense,
            'message': 'Expense added successfully'
        })
        
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete expense."""
    try:
        global expenses_db
        expenses_db = [exp for exp in expenses_db if exp['id'] != expense_id]
        
        return jsonify({
            'success': True,
            'message': 'Expense deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get expense statistics."""
    try:
        if not expenses_db:
            return jsonify({
                'success': True,
                'total': 0,
                'count': 0,
                'average': 0,
                'by_category': []
            })
        
        total = sum(expense['amount'] for expense in expenses_db)
        count = len(expenses_db)
        average = total / count if count > 0 else 0
        
        # Calculate by category
        category_totals = {}
        for expense in expenses_db:
            cat_id = expense['category_id']
            if cat_id not in category_totals:
                category_totals[cat_id] = 0
            category_totals[cat_id] += expense['amount']
        
        by_category = []
        for cat in categories_db:
            amount = category_totals.get(cat['id'], 0)
            percentage = (amount / total * 100) if total > 0 else 0
            by_category.append({
                'category': cat,
                'amount': amount,
                'percentage': percentage
            })
        
        return jsonify({
            'success': True,
            'total': total,
            'count': count,
            'average': average,
            'by_category': by_category
        })
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create new category."""
    try:
        data = request.json
        name = data.get('name', '').strip()
        emoji = data.get('emoji', '📦').strip()
        color = data.get('color', '#98D8C8')
        
        if not name:
            return jsonify({'error': 'Category name is required'}), 400
        
        # Check if category already exists
        if any(cat['name'].lower() == name.lower() for cat in categories_db):
            return jsonify({'error': 'Category already exists'}), 400
        
        # Create new category
        new_category = {
            'id': max(cat['id'] for cat in categories_db) + 1 if categories_db else 1,
            'name': name,
            'emoji': emoji,
            'color': color
        }
        
        categories_db.append(new_category)
        
        return jsonify({
            'success': True,
            'category': new_category,
            'message': 'Category created successfully'
        })
        
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update category."""
    try:
        data = request.json
        name = data.get('name', '').strip()
        emoji = data.get('emoji', '').strip()
        color = data.get('color', '')
        
        # Find category
        category = next((cat for cat in categories_db if cat['id'] == category_id), None)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if new name conflicts with existing categories
        if name and name.lower() != category['name'].lower():
            if any(cat['name'].lower() == name.lower() and cat['id'] != category_id for cat in categories_db):
                return jsonify({'error': 'Category name already exists'}), 400
        
        # Update category
        if name:
            category['name'] = name
        if emoji:
            category['emoji'] = emoji
        if color:
            category['color'] = color
        
        return jsonify({
            'success': True,
            'category': category,
            'message': 'Category updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete category."""
    try:
        # Check if category is being used by expenses
        if any(expense['category_id'] == category_id for expense in expenses_db):
            return jsonify({'error': 'Cannot delete category that has expenses'}), 400
        
        # Find and remove category
        global categories_db
        categories_db = [cat for cat in categories_db if cat['id'] != category_id]
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Simple Expense Tracker Web App...")
    logger.info("🌐 Web App: http://localhost:5000")
    logger.info("📱 Features: Add expenses, view statistics, category tracking")
    app.run(host='0.0.0.0', port=5000, debug=True)
