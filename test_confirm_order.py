# Test order confirmation backend logic directly
from app import create_app
from app.models import Order
from app.db import get_session, close_session
from app.repositories.order_repo import OrderRepository

app = create_app()

with app.app_context():
    session_db = get_session()
    try:
        # Test the backend logic directly  
        order = session_db.query(Order).filter_by(order_code='FJ-TJRPB7').first()
        if order:
            print(f'Original status: {order.status}')
            
            # Test the condition check that was failing
            can_confirm = order.status in ['pending', 'waiting_admin_confirmation']
            print(f'Can confirm? {can_confirm}')
            
            if can_confirm:
                # Update order status
                order_repo = OrderRepository(session_db)
                success = order_repo.update_order_status(order.id, 'confirmed', 'Admin confirmed via test')
                
                if success:
                    session_db.commit()
                    # Reload to verify
                    session_db.refresh(order)
                    print(f'Updated status: {order.status}')
                    print('SUCCESS: Order confirmed!')
                else:
                    print('FAILED: Could not update order status')
            else:
                print(f'FAILED: Order status {order.status} cannot be confirmed')
        else:
            print('Order not found')
            
    except Exception as e:
        session_db.rollback()
        print(f'ERROR: {e}')
    finally:
        close_session(session_db)