"""
Migration script to fix inconsistent order data
"""

from app.extensions import db
from app.models import Order
from sqlalchemy import text

def fix_order_data():
    """Fix orders with empty status, payment_method, payment_status"""
    
    # Fix empty payment_method (default to COD)
    db.session.execute(
        text("UPDATE orders SET payment_method = 'COD' WHERE payment_method = '' OR payment_method IS NULL")
    )
    
    # Fix empty payment_status (default to unpaid)
    db.session.execute(
        text("UPDATE orders SET payment_status = 'unpaid' WHERE payment_status = '' OR payment_status IS NULL")
    )
    
    # Fix empty status (default to pending)
    db.session.execute(
        text("UPDATE orders SET status = 'pending' WHERE status = '' OR status IS NULL")
    )
    
    db.session.commit()
    print("Order data cleanup completed!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    
    with app.app_context():
        fix_order_data()