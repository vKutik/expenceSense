"""
Simple Model Classes for Expense Tracker
Clean data structures with validation
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class Category:
    """Category model for expense categorization"""
    id: int
    name: str
    emoji: str
    color: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class User:
    """User model for Telegram users"""
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    created_at: Optional[str] = None
    bank_balance: float = 0.0
    
    def __post_init__(self):
        """Set default values after initialization"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name or ''}".strip()
    
    @property
    def display_name(self) -> str:
        """Get display name for UI"""
        return f"@{self.username}" if self.username else self.full_name
    
    def update_balance(self, new_balance: float):
        """Update bank balance"""
        self.bank_balance = new_balance
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class Expense:
    """Expense model for tracking expenses"""
    id: Optional[int]
    user_id: int
    amount: float
    category_id: int
    description: str = ""
    date: Optional[str] = None
    category: Optional[Category] = None
    
    def __post_init__(self):
        """Set default values after initialization"""
        if not self.date:
            self.date = datetime.now().isoformat()
    
    def validate(self) -> bool:
        """Validate expense data"""
        return (
            self.amount > 0 and
            self.user_id > 0 and
            self.category_id > 0
        )
    
    def set_category(self, category: Category):
        """Set category information"""
        self.category = category
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        if self.category:
            data['category'] = self.category.to_dict()
        return data


class ExpenseFactory:
    """Factory pattern for creating expenses"""
    
    @staticmethod
    def create_expense(
        user_id: int,
        amount: float,
        category_id: int,
        description: str = "",
        expense_id: Optional[int] = None
    ) -> Expense:
        """Create a new expense with validation"""
        
        # Validate inputs
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if user_id <= 0:
            raise ValueError("User ID must be positive")
        if category_id <= 0:
            raise ValueError("Category ID must be positive")
        
        return Expense(
            id=expense_id,
            user_id=user_id,
            amount=amount,
            category_id=category_id,
            description=description.strip()
        )
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Expense:
        """Create expense from dictionary"""
        return Expense(
            id=data.get('id'),
            user_id=data['user_id'],
            amount=data['amount'],
            category_id=data['category_id'],
            description=data.get('description', ''),
            date=data.get('date'),
            category=Category(**data['category']) if data.get('category') else None
        )


class CategoryFactory:
    """Factory for creating categories"""
    
    @staticmethod
    def get_default_categories() -> List[Category]:
        """Get default categories"""
        return [
            Category(1, 'Food', '🍕', '#000000'),
            Category(2, 'Transport', '🚗', '#000000'),
            Category(3, 'Shopping', '🛍️', '#000000'),
            Category(4, 'Entertainment', '🎬', '#000000'),
            Category(5, 'Health', '🏥', '#000000'),
            Category(6, 'Utilities', '⚡', '#000000'),
            Category(7, 'Other', '📦', '#000000')
        ]
    
    @staticmethod
    def find_by_id(category_id: int) -> Optional[Category]:
        """Find category by ID"""
        categories = CategoryFactory.get_default_categories()
        return next((cat for cat in categories if cat.id == category_id), None)
