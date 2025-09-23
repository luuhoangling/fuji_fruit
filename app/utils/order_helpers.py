"""Helper functions for order status display and logic"""

def get_order_status_display(order):
    """
    Get consistent status display text and badge class for an order
    Returns tuple: (display_text, badge_class)
    """
    
    # Handle cancelled orders first
    if order.status == 'cancelled':
        return ('Đã hủy', 'bg-danger')
    
    # Handle different status flows
    if order.status == 'pending':
        return ('Chờ xử lý', 'bg-warning')
    
    elif order.status == 'confirmed':
        return ('Đã xác nhận', 'bg-info')
    
    elif order.status == 'fulfilled':
        # Check if customer has received (for COD orders)
        if order.payment_method == 'COD' and order.payment_status == 'mock_paid':
            return ('Đã nhận hàng (COD)', 'bg-success')
        else:
            return ('Đã hoàn thành - Chờ khách hàng xác nhận', 'bg-primary')
    
    # Fallback
    return (order.status.title(), 'bg-secondary')


def get_payment_status_display(order):
    """
    Get payment status display text and class
    Returns tuple: (display_text, text_class)
    """
    if order.payment_status == 'mock_paid':
        return ('Đã thanh toán', 'text-success')
    elif order.payment_status == 'transfer_confirmed' or order.transfer_confirmed:
        return ('Đã xác nhận chuyển khoản', 'text-info')
    else:
        return ('Chưa thanh toán', 'text-warning')


def get_payment_method_display(order):
    """
    Get payment method display text and badge class
    Returns tuple: (display_text, badge_class)
    """
    if order.payment_method == 'COD':
        return ('COD', 'bg-warning')
    elif order.payment_method == 'MOCK_TRANSFER':
        return ('Chuyển khoản', 'bg-info')
    else:
        return (order.payment_method, 'bg-secondary')


def can_cancel_order(order):
    """Check if order can be cancelled"""
    return order.status in ['pending', 'confirmed']


def can_confirm_order(order):
    """Check if admin can confirm order"""
    return order.status == 'pending'


def can_mark_fulfilled(order):
    """Check if admin can mark order as fulfilled"""
    return order.status == 'confirmed'


def can_mark_delivered(order):
    """Check if admin can mark order as delivered - DEPRECATED"""
    # This function is now deprecated since users can confirm receipt directly
    return False


def can_mark_received_by_admin(order):
    """Check if admin can mark order as received by customer - DEPRECATED"""
    # This function is now deprecated since users confirm receipt directly
    return False


def can_confirm_received_by_user(order):
    """Check if user can confirm order receipt"""
    # User can confirm receipt directly when status is fulfilled
    # No need to wait for admin to mark as delivered (transfer_confirmed)
    return (order.status == 'fulfilled' and 
            not (order.payment_method == 'COD' and order.payment_status == 'mock_paid'))


def can_pay_order(order):
    """Check if user can pay for order"""
    return (order.payment_method == 'MOCK_TRANSFER' and 
            order.payment_status == 'unpaid' and 
            order.status != 'cancelled')