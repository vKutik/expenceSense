"""
Repository Pattern for Data Access
Simple in-memory storage with clean interfaces
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from models import User, Expense, Category

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user data"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
    
    def create(self, user: User) -> User:
        """Create a new user"""
        self._users[user.id] = user
        logger.info(f"User created: {user.id}")
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self._users.get(user_id)
    
    def exists(self, user_id: int) -> bool:
        """Check if user exists"""
        return user_id in self._users
    
    def get_all(self) -> List[User]:
        """Get all users"""
        return list(self._users.values())
    
    def count(self) -> int:
        """Get user count"""
        return len(self._users)
    
    def update_bank_balance(self, user_id: int, new_balance: float) -> bool:
        """Update user's bank balance"""
        user = self._users.get(user_id)
        if user:
            user.update_balance(new_balance)
            logger.info(f"Bank balance updated for user {user_id}: ${new_balance}")
            return True
        return False


class ExpenseRepository:
    """Repository for expense data"""
    
    def __init__(self):
        self._expenses: Dict[int, List[Expense]] = {}
    
    def create(self, expense: Expense) -> Expense:
        """Create a new expense"""
        user_id = expense.user_id
        if user_id not in self._expenses:
            self._expenses[user_id] = []
        
        # Auto-assign ID if not set
        if expense.id is None:
            expense.id = len(self._expenses[user_id]) + 1
        
        self._expenses[user_id].append(expense)
        logger.info(f"Expense created: {expense.id} for user {user_id}")
        return expense
    
    def get_by_user(self, user_id: int) -> List[Expense]:
        """Get all expenses for a user"""
        return self._expenses.get(user_id, [])
    
    def get_by_id(self, user_id: int, expense_id: int) -> Optional[Expense]:
        """Get specific expense by ID"""
        user_expenses = self._expenses.get(user_id, [])
        return next((exp for exp in user_expenses if exp.id == expense_id), None)
    
    def delete(self, user_id: int, expense_id: int) -> bool:
        """Delete an expense"""
        user_expenses = self._expenses.get(user_id, [])
        for i, expense in enumerate(user_expenses):
            if expense.id == expense_id:
                del user_expenses[i]
                logger.info(f"Expense deleted: {expense_id}")
                return True
        return False
    
    def get_total_for_user(self, user_id: int) -> float:
        """Get total expenses for a user"""
        user_expenses = self._expenses.get(user_id, [])
        return sum(expense.amount for expense in user_expenses)
    
    def get_category_totals(self, user_id: int) -> Dict[int, float]:
        """Get expenses grouped by category"""
        user_expenses = self._expenses.get(user_id, [])
        category_totals = {}
        
        for expense in user_expenses:
            cat_id = expense.category_id
            if cat_id not in category_totals:
                category_totals[cat_id] = 0
            category_totals[cat_id] += expense.amount
        
        return category_totals
    
    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses across all users"""
        all_expenses = []
        for user_expenses in self._expenses.values():
            all_expenses.extend(user_expenses)
        return all_expenses
    
    def count_total_expenses(self) -> int:
        """Get total number of expenses"""
        return sum(len(expenses) for expenses in self._expenses.values())


class CategoryRepository:
    """Repository for category data"""
    
    def __init__(self):
        self._categories = {}
        self._load_default_categories()
    
    def _load_default_categories(self):
        """Load default categories"""
        from models import CategoryFactory
        default_categories = CategoryFactory.get_default_categories()
        for category in default_categories:
            self._categories[category.id] = category
    
    def get_all(self) -> List[Category]:
        """Get all categories"""
        return list(self._categories.values())
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self._categories.get(category_id)
    
    def exists(self, category_id: int) -> bool:
        """Check if category exists"""
        return category_id in self._categories


class StatisticsRepository:
    """Repository for statistics calculations"""
    
    def __init__(self, expense_repo: ExpenseRepository, category_repo: CategoryRepository):
        self.expense_repo = expense_repo
        self.category_repo = category_repo
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        expenses = self.expense_repo.get_by_user(user_id)
        total = self.expense_repo.get_total_for_user(user_id)
        category_totals = self.expense_repo.get_category_totals(user_id)
        
        # Calculate category statistics
        category_stats = []
        for cat_id, amount in category_totals.items():
            category = self.category_repo.get_by_id(cat_id)
            if category:
                percentage = (amount / total * 100) if total > 0 else 0
                category_stats.append({
                    'category': category.to_dict(),
                    'amount': amount,
                    'percentage': round(percentage, 1)
                })
        
        return {
            'total': total,
            'count': len(expenses),
            'category_stats': category_stats
        }
