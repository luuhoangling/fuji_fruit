#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from app import create_app
from app.db import get_session, close_session
from app.models import Order
from datetime import datetime, timedelta
from sqlalchemy import func

def test_order_completion():
    app = create_app()
    with app.app_context():
        session_db = get_session()
        try:
            # Get the fulfilled order
            order = session_db.query(Order).filter_by(order_code='FJ-GDNB1X').first()
            
            if order:
                print(f"Đơn hàng tìm thấy: {order.order_code}")
                print(f"Trạng thái hiện tại: {order.status}")
                print(f"Phương thức thanh toán: {order.payment_method}")
                print(f"Trạng thái thanh toán: {order.payment_status}")
                print(f"Transfer confirmed: {order.transfer_confirmed}")
                
                # Simulate user confirming receipt
                print("\n=== SIMULATE USER CONFIRM RECEIPT ===")
                order.status = 'completed'
                
                if order.payment_method == 'COD':
                    order.payment_status = 'mock_paid'
                
                if order.payment_method == 'MOCK_TRANSFER':
                    order.transfer_confirmed = True
                
                session_db.commit()
                print(f"Đã cập nhật trạng thái thành: {order.status}")
                
                # Check revenue now
                thirty_days_ago = datetime.utcnow() - timedelta(days=30)
                revenue_result = session_db.query(func.sum(Order.grand_total)).filter(
                    Order.created_at >= thirty_days_ago,
                    Order.status == 'completed'
                ).scalar()
                
                print(f"\nDoanh thu 30 ngày qua sau khi hoàn thành: {revenue_result} VNĐ")
                
            else:
                print("Không tìm thấy đơn hàng FJ-GDNB1X")
                
        finally:
            close_session(session_db)

if __name__ == '__main__':
    test_order_completion()