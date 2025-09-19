"""
User model for authentication
"""
from app.models import BaseModel
from app.extensions import db
from sqlalchemy import Boolean, String, DateTime
from datetime import datetime


class User(BaseModel):
    """User model for authentication"""
    __tablename__ = 'users'
    
    # Basic info
    email = db.Column(String(255), unique=True, nullable=True, index=True)
    username = db.Column(String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(String(255), nullable=False)
    
    # Profile info
    full_name = db.Column(String(150), nullable=True)
    phone = db.Column(String(30), unique=True, nullable=True)
    avatar_url = db.Column(String(1024), nullable=True)
    
    # Account status
    is_active = db.Column(Boolean, default=True, nullable=False)
    email_verified = db.Column(Boolean, default=False, nullable=False)
    last_login_at = db.Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def display_name(self):
        """Get user's display name"""
        return self.full_name or self.username
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert user to dictionary for JSON responses"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'display_name': self.display_name,
            'phone': self.phone,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }