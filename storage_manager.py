"""
Multi-storage manager for different user levels
"""
import json
import sqlite3
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from auth import UserLevel, StorageType, UserProfile
from models import User, Expense, Category
import logging

logger = logging.getLogger(__name__)

class StorageBackend(ABC):
    """Abstract base class for storage backends"""
    
    @abstractmethod
    def save_user(self, user: User) -> bool:
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def save_expense(self, expense: Expense) -> bool:
        pass
    
    @abstractmethod
    def get_expenses(self, user_id: int) -> List[Expense]:
        pass
    
    @abstractmethod
    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def save_categories(self, categories: List[Category]) -> bool:
        pass
    
    @abstractmethod
    def get_categories(self) -> List[Category]:
        pass

class MemoryStorage(StorageBackend):
    """In-memory storage for guest users"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._expenses: Dict[int, List[Expense]] = {}
        self._categories: List[Category] = []
        logger.info("Memory storage initialized")
    
    def save_user(self, user: User) -> bool:
        self._users[user.id] = user
        return True
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def save_expense(self, expense: Expense) -> bool:
        if expense.user_id not in self._expenses:
            self._expenses[expense.user_id] = []
        self._expenses[expense.user_id].append(expense)
        return True
    
    def get_expenses(self, user_id: int) -> List[Expense]:
        return self._expenses.get(user_id, [])
    
    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        if user_id in self._expenses:
            self._expenses[user_id] = [
                exp for exp in self._expenses[user_id] if exp.id != expense_id
            ]
            return True
        return False
    
    def save_categories(self, categories: List[Category]) -> bool:
        self._categories = categories
        return True
    
    def get_categories(self) -> List[Category]:
        return self._categories

class FileStorage(StorageBackend):
    """File-based storage for registered users"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        logger.info(f"File storage initialized in {data_dir}")
    
    def _get_user_file(self, user_id: int) -> str:
        return os.path.join(self.data_dir, f"user_{user_id}.json")
    
    def _get_expenses_file(self, user_id: int) -> str:
        return os.path.join(self.data_dir, f"expenses_{user_id}.json")
    
    def _get_categories_file(self) -> str:
        return os.path.join(self.data_dir, "categories.json")
    
    def save_user(self, user: User) -> bool:
        try:
            with open(self._get_user_file(user.id), 'w') as f:
                json.dump(user.to_dict(), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        try:
            user_file = self._get_user_file(user_id)
            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    return User(**user_data)
        except Exception as e:
            logger.error(f"Error loading user: {e}")
        return None
    
    def save_expense(self, expense: Expense) -> bool:
        try:
            expenses_file = self._get_expenses_file(expense.user_id)
            expenses = self.get_expenses(expense.user_id)
            expenses.append(expense)
            
            with open(expenses_file, 'w') as f:
                json.dump([exp.to_dict() for exp in expenses], f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving expense: {e}")
            return False
    
    def get_expenses(self, user_id: int) -> List[Expense]:
        try:
            expenses_file = self._get_expenses_file(user_id)
            if os.path.exists(expenses_file):
                with open(expenses_file, 'r') as f:
                    expenses_data = json.load(f)
                    return [Expense(**exp_data) for exp_data in expenses_data]
        except Exception as e:
            logger.error(f"Error loading expenses: {e}")
        return []
    
    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        try:
            expenses = self.get_expenses(user_id)
            expenses = [exp for exp in expenses if exp.id != expense_id]
            
            expenses_file = self._get_expenses_file(user_id)
            with open(expenses_file, 'w') as f:
                json.dump([exp.to_dict() for exp in expenses], f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error deleting expense: {e}")
            return False
    
    def save_categories(self, categories: List[Category]) -> bool:
        try:
            with open(self._get_categories_file(), 'w') as f:
                json.dump([cat.to_dict() for cat in categories], f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving categories: {e}")
            return False
    
    def get_categories(self) -> List[Category]:
        try:
            categories_file = self._get_categories_file()
            if os.path.exists(categories_file):
                with open(categories_file, 'r') as f:
                    categories_data = json.load(f)
                    return [Category(**cat_data) for cat_data in categories_data]
        except Exception as e:
            logger.error(f"Error loading categories: {e}")
        return []

class DatabaseStorage(StorageBackend):
    """SQLite database storage for premium users"""
    
    def __init__(self, db_path: str = "premium_expenses.db"):
        self.db_path = db_path
        self._init_database()
        logger.info(f"Database storage initialized: {db_path}")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                bank_balance REAL DEFAULT 0.0,
                created_at TEXT,
                level TEXT DEFAULT 'premium'
            )
        ''')
        
        # Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category_id INTEGER,
                description TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                emoji TEXT,
                color TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user(self, user: User) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (id, telegram_id, first_name, last_name, username, bank_balance, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user.id, user.id, user.first_name, user.last_name, 
                  user.username, user.bank_balance, user.created_at))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error saving user to database: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return User(
                    id=row[0],
                    first_name=row[2],
                    last_name=row[3],
                    username=row[4],
                    language_code=None,
                    created_at=row[6],
                    bank_balance=row[5]
                )
        except Exception as e:
            logger.error(f"Error loading user from database: {e}")
        return None
    
    def save_expense(self, expense: Expense) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO expenses (user_id, amount, category_id, description, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (expense.user_id, expense.amount, expense.category_id, 
                  expense.description, expense.created_at))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error saving expense to database: {e}")
            return False
    
    def get_expenses(self, user_id: int) -> List[Expense]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            expenses = []
            for row in rows:
                expenses.append(Expense(
                    id=row[0],
                    user_id=row[1],
                    amount=row[2],
                    category_id=row[3],
                    description=row[4],
                    created_at=row[5]
                ))
            return expenses
        except Exception as e:
            logger.error(f"Error loading expenses from database: {e}")
        return []
    
    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
            deleted = cursor.rowcount > 0
            
            conn.commit()
            conn.close()
            return deleted
        except Exception as e:
            logger.error(f"Error deleting expense from database: {e}")
            return False
    
    def save_categories(self, categories: List[Category]) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clear existing categories
            cursor.execute('DELETE FROM categories')
            
            # Insert new categories
            for category in categories:
                cursor.execute('''
                    INSERT INTO categories (id, name, emoji, color)
                    VALUES (?, ?, ?, ?)
                ''', (category.id, category.name, category.emoji, category.color))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error saving categories to database: {e}")
            return False
    
    def get_categories(self) -> List[Category]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM categories')
            rows = cursor.fetchall()
            conn.close()
            
            categories = []
            for row in rows:
                categories.append(Category(
                    id=row[0],
                    name=row[1],
                    emoji=row[2],
                    color=row[3]
                ))
            return categories
        except Exception as e:
            logger.error(f"Error loading categories from database: {e}")
        return []

class CloudStorage(StorageBackend):
    """Cloud storage simulation for admin users"""
    
    def __init__(self):
        # In a real implementation, this would connect to cloud services
        # For now, we'll use enhanced database storage
        self.db_storage = DatabaseStorage("admin_cloud.db")
        logger.info("Cloud storage initialized (simulated with enhanced DB)")
    
    def save_user(self, user: User) -> bool:
        return self.db_storage.save_user(user)
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.db_storage.get_user(user_id)
    
    def save_expense(self, expense: Expense) -> bool:
        # Cloud storage would have additional features like:
        # - Automatic backups
        # - Cross-device sync
        # - Advanced analytics
        return self.db_storage.save_expense(expense)
    
    def get_expenses(self, user_id: int) -> List[Expense]:
        return self.db_storage.get_expenses(user_id)
    
    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        return self.db_storage.delete_expense(expense_id, user_id)
    
    def save_categories(self, categories: List[Category]) -> bool:
        return self.db_storage.save_categories(categories)
    
    def get_categories(self) -> List[Category]:
        return self.db_storage.get_categories()

class StorageManager:
    """Main storage manager that routes to appropriate backend"""
    
    def __init__(self):
        self._backends = {
            StorageType.MEMORY: MemoryStorage(),
            StorageType.FILE: FileStorage(),
            StorageType.DATABASE: DatabaseStorage(),
            StorageType.CLOUD: CloudStorage()
        }
        logger.info("Storage manager initialized with all backends")
    
    def get_backend(self, storage_type: StorageType) -> StorageBackend:
        """Get storage backend for specific type"""
        return self._backends.get(storage_type, self._backends[StorageType.MEMORY])
    
    def get_user_storage(self, user_profile: UserProfile) -> StorageBackend:
        """Get storage backend for specific user"""
        return self.get_backend(user_profile.storage_type)
    
    def get_storage_info(self, storage_type: StorageType) -> Dict[str, Any]:
        """Get information about storage type"""
        info = {
            StorageType.MEMORY: {
                "name": "Memory Storage",
                "description": "Fast in-memory storage for guest users",
                "persistence": "Session only",
                "capacity": "Limited",
                "features": ["Fast access", "No persistence"]
            },
            StorageType.FILE: {
                "name": "File Storage", 
                "description": "Local file-based storage for registered users",
                "persistence": "Local files",
                "capacity": "Medium",
                "features": ["Persistent", "Local backup"]
            },
            StorageType.DATABASE: {
                "name": "Database Storage",
                "description": "SQLite database for premium users",
                "persistence": "Full database",
                "capacity": "High",
                "features": ["ACID transactions", "Query optimization", "Data integrity"]
            },
            StorageType.CLOUD: {
                "name": "Cloud Storage",
                "description": "Cloud-based storage for admin users",
                "persistence": "Cloud infrastructure",
                "capacity": "Unlimited",
                "features": ["Auto backup", "Cross-device sync", "Advanced analytics", "99.9% uptime"]
            }
        }
        return info.get(storage_type, info[StorageType.MEMORY])

# Global storage manager instance
storage_manager = StorageManager()
