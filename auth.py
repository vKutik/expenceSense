"""
Authentication and authorization system for Telegram users
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class UserLevel(Enum):
    """User authentication levels"""
    GUEST = "guest"
    REGISTERED = "registered"
    PREMIUM = "premium"
    ADMIN = "admin"

class StorageType(Enum):
    """Storage types based on user level"""
    MEMORY = "memory"          # Guest users
    FILE = "file"             # Registered users
    DATABASE = "database"     # Premium users
    CLOUD = "cloud"           # Admin users

@dataclass
class AuthToken:
    """Authentication token"""
    token: str
    user_id: int
    level: UserLevel
    created_at: datetime
    expires_at: datetime
    permissions: List[str]
    
    def is_valid(self) -> bool:
        """Check if token is still valid"""
        return datetime.now() < self.expires_at
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions

@dataclass
class UserProfile:
    """Extended user profile with authentication info"""
    user_id: int
    telegram_id: int
    username: str
    first_name: str
    last_name: Optional[str]
    level: UserLevel
    storage_type: StorageType
    created_at: datetime
    last_login: datetime
    is_active: bool
    permissions: List[str]
    metadata: Dict[str, Any]

class AuthManager:
    """Authentication manager for handling user auth and permissions"""
    
    def __init__(self):
        self._tokens: Dict[str, AuthToken] = {}
        self._user_profiles: Dict[int, UserProfile] = {}
        self._admin_users: List[int] = [123456789]  # Add your Telegram ID here
        
    def generate_token(self, user_id: int, level: UserLevel, duration_hours: int = 24) -> str:
        """Generate authentication token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=duration_hours)
        
        permissions = self._get_permissions_for_level(level)
        
        auth_token = AuthToken(
            token=token,
            user_id=user_id,
            level=level,
            created_at=datetime.now(),
            expires_at=expires_at,
            permissions=permissions
        )
        
        self._tokens[token] = auth_token
        return token
    
    def validate_token(self, token: str) -> Optional[AuthToken]:
        """Validate authentication token"""
        auth_token = self._tokens.get(token)
        if auth_token and auth_token.is_valid():
            return auth_token
        return None
    
    def get_user_level(self, telegram_id: int) -> UserLevel:
        """Determine user level based on Telegram ID and other factors"""
        # Check if user is admin
        if telegram_id in self._admin_users:
            return UserLevel.ADMIN
        
        # Check if user has premium features (you can implement your own logic)
        user_profile = self._user_profiles.get(telegram_id)
        if user_profile and user_profile.level == UserLevel.PREMIUM:
            return UserLevel.PREMIUM
        
        # Check if user is registered (has profile)
        if user_profile:
            return UserLevel.REGISTERED
        
        # Default to guest
        return UserLevel.GUEST
    
    def get_storage_type(self, level: UserLevel) -> StorageType:
        """Get storage type based on user level"""
        storage_mapping = {
            UserLevel.GUEST: StorageType.MEMORY,
            UserLevel.REGISTERED: StorageType.FILE,
            UserLevel.PREMIUM: StorageType.DATABASE,
            UserLevel.ADMIN: StorageType.CLOUD
        }
        return storage_mapping.get(level, StorageType.MEMORY)
    
    def create_user_profile(self, telegram_id: int, username: str, 
                          first_name: str, last_name: Optional[str] = None) -> UserProfile:
        """Create new user profile"""
        level = self.get_user_level(telegram_id)
        storage_type = self.get_storage_type(level)
        
        profile = UserProfile(
            user_id=telegram_id,
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            level=level,
            storage_type=storage_type,
            created_at=datetime.now(),
            last_login=datetime.now(),
            is_active=True,
            permissions=self._get_permissions_for_level(level),
            metadata={}
        )
        
        self._user_profiles[telegram_id] = profile
        return profile
    
    def get_user_profile(self, telegram_id: int) -> Optional[UserProfile]:
        """Get user profile"""
        return self._user_profiles.get(telegram_id)
    
    def update_user_level(self, telegram_id: int, new_level: UserLevel) -> bool:
        """Update user level (admin function)"""
        profile = self._user_profiles.get(telegram_id)
        if profile:
            profile.level = new_level
            profile.storage_type = self.get_storage_type(new_level)
            profile.permissions = self._get_permissions_for_level(new_level)
            return True
        return False
    
    def _get_permissions_for_level(self, level: UserLevel) -> List[str]:
        """Get permissions based on user level"""
        permissions = {
            UserLevel.GUEST: [
                "expense:create",
                "expense:read_own",
                "category:read"
            ],
            UserLevel.REGISTERED: [
                "expense:create",
                "expense:read_own",
                "expense:update_own",
                "expense:delete_own",
                "category:read",
                "stats:read_own"
            ],
            UserLevel.PREMIUM: [
                "expense:create",
                "expense:read_own",
                "expense:update_own",
                "expense:delete_own",
                "expense:export",
                "category:read",
                "category:create_custom",
                "stats:read_own",
                "stats:advanced",
                "balance:manage",
                "backup:create"
            ],
            UserLevel.ADMIN: [
                "expense:create",
                "expense:read_all",
                "expense:update_all",
                "expense:delete_all",
                "expense:export_all",
                "category:read",
                "category:create",
                "category:update",
                "category:delete",
                "stats:read_all",
                "stats:system",
                "balance:manage",
                "backup:create",
                "backup:restore",
                "users:manage",
                "system:admin"
            ]
        }
        return permissions.get(level, permissions[UserLevel.GUEST])
    
    def authenticate_user(self, telegram_data: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate user and return auth info"""
        telegram_id = telegram_data.get('id')
        username = telegram_data.get('username', '')
        first_name = telegram_data.get('first_name', '')
        last_name = telegram_data.get('last_name')
        
        # Get or create user profile
        profile = self.get_user_profile(telegram_id)
        if not profile:
            profile = self.create_user_profile(telegram_id, username, first_name, last_name)
        else:
            profile.last_login = datetime.now()
        
        # Generate token
        token = self.generate_token(telegram_id, profile.level)
        
        return {
            'success': True,
            'user': {
                'id': profile.user_id,
                'telegram_id': profile.telegram_id,
                'username': profile.username,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'level': profile.level.value,
                'storage_type': profile.storage_type.value,
                'permissions': profile.permissions
            },
            'token': token,
            'expires_at': self._tokens[token].expires_at.isoformat()
        }

# Global auth manager instance
auth_manager = AuthManager()
