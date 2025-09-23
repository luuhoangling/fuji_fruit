#!/usr/bin/env python3
"""
Script to migrate order enum values in database to match new model definitions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from sqlalchemy import text

def migrate_order_enums():
    """Migrate order enum values in database"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Starting order enums migration...")
            
            # 1. First check current data
            print("\n=== CHECKING CURRENT DATA ===")
            result = db.session.execute(text("SELECT COUNT(*) as total FROM orders")).fetchone()
            print(f"Total orders: {result.total}")
            
            result = db.session.execute(text("""
                SELECT payment_method, COUNT(*) as count 
                FROM orders 
                GROUP BY payment_method
            """)).fetchall()
            print("Payment methods:")
            for row in result:
                print(f"  {row.payment_method}: {row.count}")
            
            result = db.session.execute(text("""
                SELECT payment_status, COUNT(*) as count 
                FROM orders 
                GROUP BY payment_status
            """)).fetchall()
            print("Payment statuses:")
            for row in result:
                print(f"  {row.payment_status}: {row.count}")
            
            result = db.session.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM orders 
                GROUP BY status
            """)).fetchall()
            print("Order statuses:")
            for row in result:
                print(f"  {row.status}: {row.count}")
            
            # 2. Update enum definitions in database
            print("\n=== UPDATING ENUM DEFINITIONS ===")
            
            # Update payment_method enum
            print("Updating payment_method enum...")
            db.session.execute(text("""
                ALTER TABLE orders 
                MODIFY COLUMN payment_method ENUM('COD', 'BANK_TRANSFER', 'MOCK_TRANSFER') 
                NOT NULL DEFAULT 'COD'
            """))
            
            # Update payment_status enum  
            print("Updating payment_status enum...")
            db.session.execute(text("""
                ALTER TABLE orders 
                MODIFY COLUMN payment_status ENUM('unpaid', 'paid', 'transfer_confirmed', 'mock_paid') 
                NOT NULL DEFAULT 'unpaid'
            """))
            
            # Update status enum
            print("Updating status enum...")
            db.session.execute(text("""
                ALTER TABLE orders 
                MODIFY COLUMN status ENUM('pending_payment', 'waiting_admin_confirmation', 'shipping', 'delivered', 'completed', 'cancelled', 'pending', 'confirmed', 'fulfilled') 
                NOT NULL DEFAULT 'pending_payment'
            """))
            
            # Update order_events enum
            print("Updating order_events enum...")
            db.session.execute(text("""
                ALTER TABLE order_events 
                MODIFY COLUMN event_type ENUM('placed', 'payment_confirmed', 'admin_confirmed', 'shipping_started', 'delivered', 'completed', 'cancelled', 'restocked', 'mock_paid', 'confirmed', 'fulfilled', 'paid') 
                NOT NULL
            """))
            
            # 3. Migrate existing data
            print("\n=== MIGRATING EXISTING DATA ===")
            
            # Migrate payment_method values
            print("Migrating payment_method values...")
            result = db.session.execute(text("""
                UPDATE orders 
                SET payment_method = 'BANK_TRANSFER' 
                WHERE payment_method = 'MOCK_TRANSFER'
            """))
            print(f"Updated {result.rowcount} rows: MOCK_TRANSFER -> BANK_TRANSFER")
            
            # Migrate payment_status values
            print("Migrating payment_status values...")
            result = db.session.execute(text("""
                UPDATE orders 
                SET payment_status = 'paid' 
                WHERE payment_status = 'mock_paid'
            """))
            print(f"Updated {result.rowcount} rows: mock_paid -> paid")
            
            # Migrate status values
            print("Migrating status values...")
            result = db.session.execute(text("""
                UPDATE orders 
                SET status = 'waiting_admin_confirmation' 
                WHERE status = 'pending'
            """))
            print(f"Updated {result.rowcount} rows: pending -> waiting_admin_confirmation")
            
            result = db.session.execute(text("""
                UPDATE orders 
                SET status = 'waiting_admin_confirmation' 
                WHERE status = 'confirmed'
            """))
            print(f"Updated {result.rowcount} rows: confirmed -> waiting_admin_confirmation")
            
            result = db.session.execute(text("""
                UPDATE orders 
                SET status = 'completed' 
                WHERE status = 'fulfilled'
            """))
            print(f"Updated {result.rowcount} rows: fulfilled -> completed")
            
            # Migrate order_events values
            print("Migrating order_events values...")
            result = db.session.execute(text("""
                UPDATE order_events 
                SET event_type = 'paid' 
                WHERE event_type = 'mock_paid'
            """))
            print(f"Updated {result.rowcount} order_events: mock_paid -> paid")
            
            result = db.session.execute(text("""
                UPDATE order_events 
                SET event_type = 'admin_confirmed' 
                WHERE event_type = 'confirmed'
            """))
            print(f"Updated {result.rowcount} order_events: confirmed -> admin_confirmed")
            
            result = db.session.execute(text("""
                UPDATE order_events 
                SET event_type = 'completed' 
                WHERE event_type = 'fulfilled'
            """))
            print(f"Updated {result.rowcount} order_events: fulfilled -> completed")
            
            # 4. Commit changes
            db.session.commit()
            print("\n=== MIGRATION COMPLETED SUCCESSFULLY ===")
            
            # 5. Verify changes
            print("\n=== VERIFYING CHANGES ===")
            result = db.session.execute(text("""
                SELECT payment_method, COUNT(*) as count 
                FROM orders 
                GROUP BY payment_method
            """)).fetchall()
            print("New payment methods:")
            for row in result:
                print(f"  {row.payment_method}: {row.count}")
            
            result = db.session.execute(text("""
                SELECT payment_status, COUNT(*) as count 
                FROM orders 
                GROUP BY payment_status
            """)).fetchall()
            print("New payment statuses:")
            for row in result:
                print(f"  {row.payment_status}: {row.count}")
            
            result = db.session.execute(text("""
                SELECT status, COUNT(*) as count 
                FROM orders 
                GROUP BY status
            """)).fetchall()
            print("New order statuses:")
            for row in result:
                print(f"  {row.status}: {row.count}")
                
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()
            raise
        
if __name__ == "__main__":
    migrate_order_enums()