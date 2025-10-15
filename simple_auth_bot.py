"""
Simple Telegram Bot with Registration and Sign-in
Works without HTTPS requirements
"""
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4"

# Simple in-memory user database
users_db = {}
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - automatically authenticate via Telegram."""
    user = update.effective_user
    
    # Automatically create/update user from Telegram data
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'created_at': '2025-10-13',
        'expenses': []
    }
    
    users_db[user.id] = user_data
    user_sessions[user.id] = True
    
    # Go directly to add expense page
    await show_add_expense_page_direct(update, context)

async def show_add_expense_page_direct(update, context):
    """Show the add expense page directly."""
    user = update.effective_user
    
    # Create keyboard with quick action buttons
    keyboard = [
        [InlineKeyboardButton("💰 Add Expense", callback_data="add_expense")],
        [InlineKeyboardButton("📊 View Expenses", callback_data="view_expenses")],
        [InlineKeyboardButton("📈 Statistics", callback_data="statistics")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"💰 <b>Welcome to Expense Tracker!</b>\n\n"
        f"Hello {user.first_name}! You're automatically signed in via Telegram.\n\n"
        f"<b>Add New Expense:</b>\n"
        f"Send a message in this format:\n\n"
        f"<code>amount category description</code>\n\n"
        f"<b>Example:</b>\n"
        f"<code>25.50 food lunch at restaurant</code>\n\n"
        f"<b>Available Categories:</b>\n"
        f"• food - 🍕 Food & Dining\n"
        f"• transport - 🚗 Transportation\n"
        f"• shopping - 🛍️ Shopping\n"
        f"• entertainment - 🎬 Entertainment\n"
        f"• health - 🏥 Health & Medical\n"
        f"• utilities - ⚡ Utilities\n"
        f"• other - 📦 Other\n\n"
        f"Send your expense now:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    # Set user state for expense input
    context.user_data['waiting_for_expense'] = True


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main menu for registered users - goes directly to add expense."""
    user = update.effective_user
    user_data = users_db[user.id]
    
    # Create a fake callback query to use show_add_expense_page
    class FakeQuery:
        def __init__(self, user):
            self.from_user = user
        
        async def edit_message_text(self, text, parse_mode=None, reply_markup=None):
            await update.message.reply_text(text, parse_mode=parse_mode, reply_markup=reply_markup)
    
    fake_query = FakeQuery(user)
    await show_add_expense_page(fake_query, context)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "add_expense":
        await handle_add_expense(query, context)
    elif query.data == "view_expenses":
        await handle_view_expenses(query, context)
    elif query.data == "statistics":
        await handle_statistics(query, context)
    elif query.data == "settings":
        await handle_settings(query, context)


async def show_add_expense_page(query, context):
    """Show the add expense page directly."""
    user = query.from_user
    
    # Create keyboard with quick action buttons
    keyboard = [
        [InlineKeyboardButton("💰 Add Expense", callback_data="add_expense")],
        [InlineKeyboardButton("📊 View Expenses", callback_data="view_expenses")],
        [InlineKeyboardButton("📈 Statistics", callback_data="statistics")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "💰 <b>Add New Expense</b>\n\n"
        "To add an expense, please send a message in this format:\n\n"
        "<code>amount category description</code>\n\n"
        "<b>Example:</b>\n"
        "<code>25.50 food lunch at restaurant</code>\n\n"
        "<b>Available Categories:</b>\n"
        "• food - 🍕 Food & Dining\n"
        "• transport - 🚗 Transportation\n"
        "• shopping - 🛍️ Shopping\n"
        "• entertainment - 🎬 Entertainment\n"
        "• health - 🏥 Health & Medical\n"
        "• utilities - ⚡ Utilities\n"
        "• other - 📦 Other\n\n"
        "Send your expense now:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    
    # Set user state for expense input
    context.user_data['waiting_for_expense'] = True


async def handle_add_expense(query, context):
    """Handle add expense."""
    await show_add_expense_page(query, context)

async def handle_view_expenses(query, context):
    """Handle view expenses."""
    user_id = query.from_user.id
    
    # Ensure user exists in database
    if user_id not in users_db:
        users_db[user_id] = {'expenses': []}
    
    user_data = users_db[user_id]
    expenses = user_data.get('expenses', [])
    
    if not expenses:
        await query.edit_message_text(
            "📊 <b>Your Expenses</b>\n\n"
            "No expenses found. Add your first expense to get started!",
            parse_mode='HTML'
        )
        return
    
    # Format expenses
    total = sum(expense['amount'] for expense in expenses)
    expense_list = "\n".join([
        f"• ${expense['amount']:.2f} - {expense['category']} - {expense['description']}"
        for expense in expenses[-10:]  # Show last 10 expenses
    ])
    
    await query.edit_message_text(
        f"📊 <b>Your Expenses</b>\n\n"
        f"<b>Total Spent:</b> ${total:.2f}\n"
        f"<b>Total Transactions:</b> {len(expenses)}\n\n"
        f"<b>Recent Expenses:</b>\n{expense_list}",
        parse_mode='HTML'
    )

async def handle_statistics(query, context):
    """Handle statistics."""
    user_id = query.from_user.id
    
    # Ensure user exists in database
    if user_id not in users_db:
        users_db[user_id] = {'expenses': []}
    
    user_data = users_db[user_id]
    expenses = user_data.get('expenses', [])
    
    if not expenses:
        await query.edit_message_text(
            "📈 <b>Statistics</b>\n\n"
            "No expenses found. Add some expenses to see statistics!",
            parse_mode='HTML'
        )
        return
    
    # Calculate statistics
    total = sum(expense['amount'] for expense in expenses)
    category_totals = {}
    
    for expense in expenses:
        cat = expense['category']
        if cat not in category_totals:
            category_totals[cat] = 0
        category_totals[cat] += expense['amount']
    
    # Format category stats
    category_stats = "\n".join([
        f"• {cat.title()}: ${amount:.2f} ({amount/total*100:.1f}%)"
        for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    ])
    
    await query.edit_message_text(
        f"📈 <b>Your Statistics</b>\n\n"
        f"<b>Total Spent:</b> ${total:.2f}\n"
        f"<b>Total Transactions:</b> {len(expenses)}\n"
        f"<b>Average per Transaction:</b> ${total/len(expenses):.2f}\n\n"
        f"<b>By Category:</b>\n{category_stats}",
        parse_mode='HTML'
    )

async def handle_settings(query, context):
    """Handle settings."""
    user_id = query.from_user.id
    user = query.from_user
    
    # Ensure user exists in database
    if user_id not in users_db:
        users_db[user_id] = {
            'id': user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'created_at': '2025-10-13',
            'expenses': []
        }
    
    user_data = users_db[user_id]
    
    await query.edit_message_text(
        f"⚙️ <b>Account Settings</b>\n\n"
        f"<b>Account Information:</b>\n"
        f"• Name: {user_data['first_name']} {user_data.get('last_name', '')}\n"
        f"• Username: @{user_data.get('username', 'user')}\n"
        f"• Account ID: {user_data['id']}\n"
        f"• Member since: {user_data['created_at']}\n\n"
        f"<b>Expense Data:</b>\n"
        f"• Total expenses: {len(user_data.get('expenses', []))}\n"
        f"• Total amount: ${sum(exp['amount'] for exp in user_data.get('expenses', [])):.2f}\n\n"
        f"<b>Available Actions:</b>\n"
        f"• Clear all expenses\n"
        f"• Export data\n"
        f"• Account management",
        parse_mode='HTML'
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    user_id = update.effective_user.id
    
    # Check if user is waiting for expense input
    if context.user_data.get('waiting_for_expense'):
        await process_expense_input(update, context)
        return
    
    # Default response - automatically create user if needed
    if user_id not in users_db:
        users_db[user_id] = {
            'id': user_id,
            'first_name': update.effective_user.first_name,
            'last_name': update.effective_user.last_name,
            'username': update.effective_user.username,
            'created_at': '2025-10-13',
            'expenses': []
        }
        user_sessions[user_id] = True
    
    await update.message.reply_text(
        "💰 <b>Expense Tracker</b>\n\n"
        "You are automatically signed in via Telegram. Use the buttons below to manage your expenses.\n\n"
        "Send /start to see the main menu.",
        parse_mode='HTML'
    )

async def process_expense_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process expense input from user."""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    try:
        # Parse expense input: "amount category description"
        parts = text.split(' ', 2)
        if len(parts) < 2:
            await update.message.reply_text(
                "❌ <b>Invalid Format</b>\n\n"
                "Please use: <code>amount category description</code>\n\n"
                "Example: <code>25.50 food lunch at restaurant</code>",
                parse_mode='HTML'
            )
            return
        
        amount = float(parts[0])
        category = parts[1].lower()
        description = parts[2] if len(parts) > 2 else ""
        
        # Validate category
        valid_categories = ['food', 'transport', 'shopping', 'entertainment', 'health', 'utilities', 'other']
        if category not in valid_categories:
            await update.message.reply_text(
                f"❌ <b>Invalid Category</b>\n\n"
                f"Available categories: {', '.join(valid_categories)}\n\n"
                f"Please try again:",
                parse_mode='HTML'
            )
            return
        
        # Ensure user exists in database
        if user_id not in users_db:
            users_db[user_id] = {
                'id': user_id,
                'first_name': update.effective_user.first_name,
                'last_name': update.effective_user.last_name,
                'username': update.effective_user.username,
                'created_at': '2025-10-13',
                'expenses': []
            }
        
        expense = {
            'amount': amount,
            'category': category,
            'description': description,
            'date': '2025-10-13'
        }
        
        users_db[user_id]['expenses'].append(expense)
        
        # Clear waiting state
        context.user_data['waiting_for_expense'] = False
        
        await update.message.reply_text(
            f"✅ <b>Expense Added Successfully!</b>\n\n"
            f"<b>Amount:</b> ${amount:.2f}\n"
            f"<b>Category:</b> {category.title()}\n"
            f"<b>Description:</b> {description or 'No description'}\n\n"
            f"Send /start to see your dashboard.",
            parse_mode='HTML'
        )
        
    except ValueError:
        await update.message.reply_text(
            "❌ <b>Invalid Amount</b>\n\n"
            "Please enter a valid number for the amount.\n\n"
            "Example: <code>25.50 food lunch</code>",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ <b>Error</b>\n\n"
            f"Something went wrong: {str(e)}\n\n"
            f"Please try again:",
            parse_mode='HTML'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors gracefully."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Simple Auth Bot...")
    logger.info(f"Bot Token: {BOT_TOKEN[:10]}...")
    logger.info("Features: Registration, Sign-in, Expense tracking")
    application.run_polling()

if __name__ == '__main__':
    main()
