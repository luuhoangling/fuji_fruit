#!/usr/bin/env python3
"""
Script to create a test user for authentication testing
"""
import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.auth import hash_password
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    """Create a test user"""
    try:
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            # Check if test user already exists
            existing_user = db.session.query(User).filter_by(email='test@fuji.com').first()
            if existing_user:
                logger.info("Test user already exists!")
                return True
            
            # Create test user
            test_user = User(
                username='testuser',
                email='test@fuji.com',
                password_hash=hash_password('123456'),
                full_name='Test User',
                phone='0123456789',
                is_active=True,
                email_verified=True
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            logger.info("Test user created successfully!")
            logger.info("Email: test@fuji.com")
            logger.info("Password: 123456")
            
            return True
            
    except Exception as e:
        logger.error(f"Failed to create test user: {str(e)}")
        return False

if __name__ == '__main__':
    success = create_test_user()
    sys.exit(0 if success else 1)