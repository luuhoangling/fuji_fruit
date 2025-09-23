# Test order status script
from app import create_app
from app.models import Order
from app.db import get_session, close_session

app = create_app()

with app.app_context():
    session_db = get_session()
    try:
        # Find an order with waiting_admin_confirmation status
        order = session_db.query(Order).filter_by(status='waiting_admin_confirmation').first()
        if order:
            print(f'Found order {order.order_code} with status: {order.status}')
            print(f'Order details: ID={order.id}, Status={order.status}, Payment={order.payment_method}')
        else:
            print('No orders with waiting_admin_confirmation status found')
            
        # List all order statuses in database
        statuses = session_db.query(Order.status).distinct().all()
        print('All order statuses in database:', [s[0] for s in statuses])
            
    finally:
        close_session(session_db)