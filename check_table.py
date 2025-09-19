#!/usr/bin/env python3
"""
Script to check database table structure
"""
import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db

def check_users_table():
    """Check users table structure"""
    try:
        app = create_app()
        
        with app.app_context():
            result = db.session.execute(db.text('DESCRIBE users'))
            print("Users table structure:")
            for row in result:
                print(f"  {row}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_users_table()