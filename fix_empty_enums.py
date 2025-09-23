#!/usr/bin/env python3
"""
Script to fix empty enum values in orders table
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from sqlalchemy import text

def fix_empty_enum_values():
    """Fix empty enum values in orders table"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Fixing empty enum values...")
            
            # Fix empty payment_method
            result = db.session.execute(text("""
                UPDATE orders 
                SET payment_method = 'COD' 
                WHERE payment_method = '' OR payment_method IS NULL
            """))
            print(f"Fixed {result.rowcount} empty payment_method values")
            
            # Fix empty payment_status  
            result = db.session.execute(text("""
                UPDATE orders 
                SET payment_status = 'unpaid' 
                WHERE payment_status = '' OR payment_status IS NULL
            """))
            print(f"Fixed {result.rowcount} empty payment_status values")
            
            # Fix empty status
            result = db.session.execute(text("""
                UPDATE orders 
                SET status = 'waiting_admin_confirmation' 
                WHERE status = '' OR status IS NULL
            """))
            print(f"Fixed {result.rowcount} empty status values")
            
            db.session.commit()
            print("✅ Fixed empty enum values successfully!")
            
            # Verify
            print("\n=== VERIFICATION ===")
            result = db.session.execute(text("""
                SELECT payment_method, COUNT(*) as count 
                FROM orders 
                GROUP BY payment_method
            """)).fetchall()
            print("Payment methods after fix:")
            for row in result:
                print(f"  '{row.payment_method}': {row.count}")
            
            result = db.session.execute(text("""
                SELECT payment_status, COUNT(*) as count 
                FROM orders 
                GROUP BY payment_status
            """)).fetchall()
            print("Payment statuses after fix:")
            for row in result:
                print(f"  '{row.payment_status}': {row.count}")
            
            result = db.session.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM orders 
                GROUP BY status
            """)).fetchall()
            print("Order statuses after fix:")
            for row in result:
                print(f"  '{row.status}': {row.count}")
                
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    fix_empty_enum_values()