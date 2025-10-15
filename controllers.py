"""
Controller Layer - Handle HTTP Requests
Clean separation between HTTP layer and business logic
"""
from typing import Dict, Any, Optional
import logging
from flask import jsonify, request

from services import AppService
from observers import emit_event
from models import User

logger = logging.getLogger(__name__)


class BaseController:
    """Base controller with common functionality"""
    
    def __init__(self, app_service: AppService):
        self.app_service = app_service
    
    def success_response(self, data: Dict[str, Any], status_code: int = 200) -> tuple:
        """Create success response"""
        return jsonify({'success': True, **data}), status_code
    
    def error_response(self, message: str, status_code: int = 400) -> tuple:
        """Create error response"""
        return jsonify({'error': message}), status_code
    
    def handle_exception(self, e: Exception, operation: str) -> tuple:
        """Handle exceptions consistently"""
        logger.error(f"Error in {operation}: {e}")
        return self.error_response(str(e), 500)


class AppController(BaseController):
    """Controller for app initialization"""
    
    def init_app(self, init_data: str, bot_token: str) -> tuple:
        """Initialize the app with user data"""
        try:
            from app import verify_telegram_webapp_data
            
            # Authenticate user
            user_data = verify_telegram_webapp_data(init_data, bot_token)
            if not user_data:
                return self.error_response('Invalid Telegram data', 401)
            
            # Initialize user
            app_data = self.app_service.initialize_user(user_data)
            
            # Emit user creation event
            emit_event('user_created', {
                'user_id': user_data['id'],
                'username': user_data.get('username'),
                'first_name': user_data.get('first_name')
            })
            
            return self.success_response(app_data)
            
        except Exception as e:
            return self.handle_exception(e, 'init_app')


class ExpenseController(BaseController):
    """Controller for expense operations"""
    
    def get_expenses(self, user_id: int) -> tuple:
        """Get user expenses"""
        try:
            if not user_id:
                return self.error_response('User ID required')
            
            expenses_data = self.app_service.get_user_expenses(user_id)
            return self.success_response(expenses_data)
            
        except Exception as e:
            return self.handle_exception(e, 'get_expenses')
    
    def add_expense(self, expense_data: Dict[str, Any]) -> tuple:
        """Add new expense"""
        try:
            if not expense_data:
                return self.error_response('No expense data provided')
            
            # Add expense
            result = self.app_service.add_expense(expense_data)
            expense = result['expense']
            
            # Emit expense creation event
            emit_event('expense_created', {
                'user_id': expense['user_id'],
                'expense_id': expense['id'],
                'amount': expense['amount'],
                'category_id': expense['category_id']
            })
            
            return self.success_response(result, 201)
            
        except ValueError as e:
            return self.error_response(str(e), 400)
        except Exception as e:
            return self.handle_exception(e, 'add_expense')
    
    def delete_expense(self, user_id: int, expense_id: int) -> tuple:
        """Delete an expense"""
        try:
            if not user_id:
                return self.error_response('User ID required')
            
            self.app_service.delete_expense(user_id, expense_id)
            
            # Emit expense deletion event
            emit_event('expense_deleted', {
                'user_id': user_id,
                'expense_id': expense_id
            })
            
            return self.success_response({'success': True})
            
        except ValueError as e:
            return self.error_response(str(e), 404)
        except Exception as e:
            return self.handle_exception(e, 'delete_expense')


class CategoryController(BaseController):
    """Controller for category operations"""
    
    def get_categories(self) -> tuple:
        """Get available categories"""
        try:
            categories = self.app_service.category_service.get_all_categories()
            categories_data = [cat.to_dict() for cat in categories]
            return self.success_response({'categories': categories_data})
            
        except Exception as e:
            return self.handle_exception(e, 'get_categories')


class StatisticsController(BaseController):
    """Controller for statistics operations"""
    
    def get_stats(self, user_id: int) -> tuple:
        """Get user statistics"""
        try:
            if not user_id:
                return self.error_response('User ID required')
            
            stats = self.app_service.get_user_statistics(user_id)
            return self.success_response(stats)
            
        except Exception as e:
            return self.handle_exception(e, 'get_stats')


class HealthController(BaseController):
    """Controller for health check"""
    
    def health_check(self) -> tuple:
        """Health check endpoint"""
        try:
            system_stats = self.app_service.statistics_service.get_system_statistics()
            
            health_data = {
                'status': 'healthy',
                'message': 'Telegram Mini App is running',
                'users_count': self.app_service.user_repo.count(),
                'total_expenses': self.app_service.expense_repo.count_total_expenses(),
                'last_updated': system_stats['last_updated']
            }
            
            return self.success_response(health_data)
            
        except Exception as e:
            return self.handle_exception(e, 'health_check')


class BankBalanceController(BaseController):
    """Controller for bank balance operations"""
    
    def get_balance(self, user_id: int) -> tuple:
        """Get user's bank balance"""
        try:
            if not user_id:
                return self.error_response('User ID required')
            
            result = self.app_service.get_bank_balance(user_id)
            return self.success_response(result)
            
        except ValueError as e:
            return self.error_response(str(e), 404)
        except Exception as e:
            return self.handle_exception(e, 'get_balance')
    
    def update_balance(self, user_id: int, new_balance: float) -> tuple:
        """Update user's bank balance"""
        try:
            if not user_id:
                return self.error_response('User ID required')
            
            result = self.app_service.update_bank_balance(user_id, new_balance)
            return self.success_response(result)
            
        except ValueError as e:
            return self.error_response(str(e), 400)
        except Exception as e:
            return self.handle_exception(e, 'update_balance')


class ControllerFactory:
    """Factory for creating controllers"""
    
    @staticmethod
    def create_controllers(app_service: AppService) -> Dict[str, BaseController]:
        """Create all controllers with dependencies"""
        return {
            'app': AppController(app_service),
            'expense': ExpenseController(app_service),
            'category': CategoryController(app_service),
            'statistics': StatisticsController(app_service),
            'health': HealthController(app_service),
            'balance': BankBalanceController(app_service)
        }
