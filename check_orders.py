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

def check_orders():
    app = create_app()
    with app.app_context():
        session_db = get_session()
        try:
            # Kiểm tra tất cả đơn hàng
            print('=== TẤT CẢ ĐƠN HÀNG ===')
            all_orders = session_db.query(Order).all()
            for order in all_orders:
                print(f'ID: {order.id}, Code: {order.order_code}, Status: {order.status}, Total: {order.grand_total}, Created: {order.created_at}')
            
            print('\n=== ĐƠN HÀNG COMPLETED ===')
            completed_orders = session_db.query(Order).filter(Order.status == 'completed').all()
            for order in completed_orders:
                print(f'ID: {order.id}, Code: {order.order_code}, Status: {order.status}, Total: {order.grand_total}, Created: {order.created_at}')
            
            # Kiểm tra doanh thu 30 ngày qua
            print('\n=== DOANH THU 30 NGÀY QUA ===')
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            print(f'Từ ngày: {thirty_days_ago}')
            
            revenue_result = session_db.query(func.sum(Order.grand_total)).filter(
                Order.created_at >= thirty_days_ago,
                Order.status == 'completed'
            ).scalar()
            print(f'Doanh thu: {revenue_result}')
            
            # Kiểm tra đơn completed trong 30 ngày
            recent_completed = session_db.query(Order).filter(
                Order.created_at >= thirty_days_ago,
                Order.status == 'completed'
            ).all()
            print(f'Số đơn completed trong 30 ngày: {len(recent_completed)}')
            for order in recent_completed:
                print(f'  - {order.order_code}: {order.grand_total} VNĐ, tạo: {order.created_at}')
            
            # Kiểm tra tất cả đơn completed bất kể thời gian
            print('\n=== TẤT CẢ ĐƠN COMPLETED (KHÔNG GIỚI HẠN THỜI GIAN) ===')
            all_completed = session_db.query(Order).filter(Order.status == 'completed').all()
            total_revenue_all_time = session_db.query(func.sum(Order.grand_total)).filter(Order.status == 'completed').scalar()
            print(f'Tổng số đơn completed: {len(all_completed)}')
            print(f'Tổng doanh thu từ đơn completed: {total_revenue_all_time}')
            
        finally:
            close_session(session_db)

if __name__ == '__main__':
    check_orders()