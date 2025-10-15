"""
Service Layer - Business Logic
Clean separation of concerns with service classes
"""
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from models import User, Expense, Category, ExpenseFactory, CategoryFactory
from repository import UserRepository, ExpenseRepository, CategoryRepository, StatisticsRepository

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related operations"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_or_get_user(self, user_data: Dict[str, Any]) -> User:
        """Create new user or return existing one"""
        user_id = user_data['id']
        
        # Check if user already exists
        existing_user = self.user_repo.get_by_id(user_id)
        if existing_user:
            return existing_user
        
        # Create new user
        user = User(
            id=user_id,
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name'),
            username=user_data.get('username'),
            language_code=user_data.get('language_code')
        )
        
        return self.user_repo.create(user)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repo.get_by_id(user_id)
    
    def validate_user(self, user_id: int) -> bool:
        """Validate if user exists"""
        return self.user_repo.exists(user_id)
    
    def update_bank_balance(self, user_id: int, new_balance: float) -> bool:
        """Update user's bank balance"""
        if not self.validate_user(user_id):
            raise ValueError(f"User {user_id} not found")
        
        if new_balance < 0:
            raise ValueError("Bank balance cannot be negative")
        
        return self.user_repo.update_bank_balance(user_id, new_balance)
    
    def get_bank_balance(self, user_id: int) -> float:
        """Get user's bank balance"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        return user.bank_balance


class ExpenseService:
    """Service for expense-related operations"""
    
    def __init__(self, expense_repo: ExpenseRepository, category_repo: CategoryRepository):
        self.expense_repo = expense_repo
        self.category_repo = category_repo
    
    def create_expense(self, user_id: int, amount: float, category_id: int, description: str = "") -> Expense:
        """Create a new expense with validation"""
        
        # Validate category exists
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category {category_id} not found")
        
        # Create expense using factory
        expense = ExpenseFactory.create_expense(
            user_id=user_id,
            amount=amount,
            category_id=category_id,
            description=description
        )
        
        # Validate expense
        if not expense.validate():
            raise ValueError("Invalid expense data")
        
        # Add category info
        expense.set_category(category)
        
        # Save expense
        return self.expense_repo.create(expense)
    
    def get_user_expenses(self, user_id: int) -> List[Expense]:
        """Get all expenses for a user with category info"""
        expenses = self.expense_repo.get_by_user(user_id)
        
        # Add category information to each expense
        for expense in expenses:
            if not expense.category:
                category = self.category_repo.get_by_id(expense.category_id)
                if category:
                    expense.set_category(category)
        
        return expenses
    
    def delete_expense(self, user_id: int, expense_id: int) -> bool:
        """Delete an expense"""
        return self.expense_repo.delete(user_id, expense_id)
    
    def get_user_total(self, user_id: int) -> float:
        """Get total expenses for a user"""
        return self.expense_repo.get_total_for_user(user_id)
    
    def validate_expense_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate expense data and return cleaned data"""
        errors = []
        
        # Initialize variables
        amount = 0
        category_id = 0
        user_id = None
        
        # Validate amount
        try:
            amount = float(data.get('amount', 0))
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")
        
        # Validate category
        try:
            category_id = int(data.get('categoryId', 0))
            if category_id <= 0:
                errors.append("Category must be selected")
            elif not self.category_repo.exists(category_id):
                errors.append("Invalid category")
        except (ValueError, TypeError):
            errors.append("Category must be a valid selection")
        
        # Validate user
        user_id = data.get('userId')
        if not user_id:
            errors.append("User ID is required")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return {
            'user_id': int(user_id),
            'amount': amount,
            'category_id': category_id,
            'description': str(data.get('description', '')).strip()
        }


class CategoryService:
    """Service for category-related operations"""
    
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo
    
    def get_all_categories(self) -> List[Category]:
        """Get all available categories"""
        return self.category_repo.get_all()
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.category_repo.get_by_id(category_id)
    
    def validate_category(self, category_id: int) -> bool:
        """Validate if category exists"""
        return self.category_repo.exists(category_id)


class StatisticsService:
    """Service for statistics operations"""
    
    def __init__(self, stats_repo: StatisticsRepository):
        self.stats_repo = stats_repo
    
    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        return self.stats_repo.get_user_stats(user_id)
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics"""
        # This would typically come from a system stats repository
        # For now, return basic counts
        return {
            'total_users': 0,  # Would need user repo access
            'total_expenses': 0,  # Would need expense repo access
            'last_updated': datetime.now().isoformat()
        }


class AppService:
    """Main application service - orchestrates other services"""
    
    def __init__(self):
        # Initialize repositories
        self.user_repo = UserRepository()
        self.expense_repo = ExpenseRepository()
        self.category_repo = CategoryRepository()
        self.stats_repo = StatisticsRepository(self.expense_repo, self.category_repo)
        
        # Initialize services
        self.user_service = UserService(self.user_repo)
        self.expense_service = ExpenseService(self.expense_repo, self.category_repo)
        self.category_service = CategoryService(self.category_repo)
        self.statistics_service = StatisticsService(self.stats_repo)
    
    def initialize_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize user and return app data"""
        user = self.user_service.create_or_get_user(user_data)
        categories = self.category_service.get_all_categories()
        
        return {
            'user': user.to_dict(),
            'categories': [cat.to_dict() for cat in categories]
        }
    
    def add_expense(self, expense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new expense with full validation"""
        # Validate data
        validated_data = self.expense_service.validate_expense_data(expense_data)
        
        # Create expense
        expense = self.expense_service.create_expense(
            user_id=validated_data['user_id'],
            amount=validated_data['amount'],
            category_id=validated_data['category_id'],
            description=validated_data['description']
        )
        
        return {'expense': expense.to_dict()}
    
    def get_user_expenses(self, user_id: int) -> Dict[str, Any]:
        """Get user expenses with total"""
        expenses = self.expense_service.get_user_expenses(user_id)
        total = self.expense_service.get_user_total(user_id)
        
        return {
            'expenses': [exp.to_dict() for exp in expenses],
            'total': total
        }
    
    def delete_expense(self, user_id: int, expense_id: int) -> Dict[str, Any]:
        """Delete an expense"""
        success = self.expense_service.delete_expense(user_id, expense_id)
        
        if not success:
            raise ValueError("Expense not found")
        
        return {'success': True}
    
    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        return self.statistics_service.get_user_statistics(user_id)
    
    def update_bank_balance(self, user_id: int, new_balance: float) -> Dict[str, Any]:
        """Update user's bank balance"""
        success = self.user_service.update_bank_balance(user_id, new_balance)
        return {'success': success}
    
    def get_bank_balance(self, user_id: int) -> Dict[str, Any]:
        """Get user's bank balance"""
        balance = self.user_service.get_bank_balance(user_id)
        return {'success': True, 'balance': balance}
