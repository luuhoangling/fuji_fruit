#!/usr/bin/env python3
"""
Test script to verify order status filtering in my_orders page
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.db import get_session, close_session
from app.models import Order

def test_order_status_filtering():
    """Test that order status filtering works correctly"""
    app = create_app()
    
    with app.app_context():
        session_db = get_session()
        try:
            # Check orders by status
            print("=== KIỂM TRA FILTER TRẠNG THÁI ĐƠN HÀNG ===")
            
            # Test fulfilled orders (đang giao hàng)
            fulfilled_orders = session_db.query(Order).filter_by(status='fulfilled').all()
            print(f"\n1. Đơn hàng 'fulfilled' (Đang giao hàng): {len(fulfilled_orders)}")
            for order in fulfilled_orders:
                print(f"   - {order.order_code}: status={order.status}, payment_method={order.payment_method}, payment_status={order.payment_status}")
            
            # Test completed orders (đã giao hàng)
            completed_orders = session_db.query(Order).filter_by(status='completed').all()
            print(f"\n2. Đơn hàng 'completed' (Đã giao hàng): {len(completed_orders)}")
            for order in completed_orders:
                print(f"   - {order.order_code}: status={order.status}, payment_method={order.payment_method}, payment_status={order.payment_status}")
            
            # Test all orders
            all_orders = session_db.query(Order).all()
            print(f"\n3. Tổng số đơn hàng: {len(all_orders)}")
            
            # Group by status
            status_counts = {}
            for order in all_orders:
                status = order.status
                if status not in status_counts:
                    status_counts[status] = 0
                status_counts[status] += 1
            
            print("\n4. Thống kê theo trạng thái:")
            for status, count in status_counts.items():
                print(f"   - {status}: {count} đơn hàng")
                
        finally:
            close_session(session_db)

if __name__ == '__main__':
    test_order_status_filtering()