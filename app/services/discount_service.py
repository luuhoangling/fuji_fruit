"""
Discount service for managing discount codes and their application
"""
from typing import List, Dict, Optional, Tuple
from app.models.discount import Discount
from app.models.user_discount_usage import UserDiscountUsage
from sqlalchemy.orm import Session
from datetime import datetime


class DiscountService:
    """Service for discount management"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_discount_by_code(self, code: str) -> Optional[Discount]:
        """Get discount by code"""
        return self.session.query(Discount).filter(
            Discount.code == code.upper(),
            Discount.is_active == True
        ).first()
    
    def validate_discount_for_user(self, discount_code: str, user_id: int, order_amount: float) -> Tuple[bool, str, Optional[Discount]]:
        """
        Validate if discount can be applied for user and order
        Returns: (is_valid, message, discount_object)
        """
        # Get discount
        discount = self.get_discount_by_code(discount_code)
        if not discount:
            return False, "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa", None
        
        # Check if discount is currently valid
        if not discount.is_valid:
            return False, "Mã giảm giá đã hết hạn hoặc chưa có hiệu lực", None
        
        # Check usage count for user
        user_usage_count = self.session.query(UserDiscountUsage).filter(
            UserDiscountUsage.user_id == user_id,
            UserDiscountUsage.discount_id == discount.id
        ).count()
        
        # Validate against order and user limits
        can_apply, message = discount.can_apply_to_order(order_amount, user_usage_count)
        if not can_apply:
            return False, message, None
        
        return True, "Mã giảm giá hợp lệ", discount
    
    def apply_discount_to_order(self, discount_code: str, user_id: int, order_id: int, order_amount: float) -> Tuple[bool, str, float]:
        """
        Apply discount to order and track usage
        Returns: (success, message, discount_amount)
        """
        is_valid, message, discount = self.validate_discount_for_user(discount_code, user_id, order_amount)
        
        if not is_valid:
            return False, message, 0
        
        # Calculate discount amount
        discount_amount = discount.calculate_discount(order_amount)
        
        # Track usage
        usage = UserDiscountUsage(
            user_id=user_id,
            discount_id=discount.id,
            order_id=order_id
        )
        self.session.add(usage)
        
        # Increment usage count
        discount.increment_usage()
        
        return True, "Áp dụng mã giảm giá thành công", discount_amount
    
    def get_available_discounts_for_user(self, user_id: int, order_amount: float = 0) -> List[Dict]:
        """Get list of available discounts for a user"""
        # Get all active discounts
        discounts = self.session.query(Discount).filter(
            Discount.is_active == True
        ).all()
        
        available_discounts = []
        
        for discount in discounts:
            if not discount.is_valid:
                continue
            
            # Check user usage
            user_usage_count = self.session.query(UserDiscountUsage).filter(
                UserDiscountUsage.user_id == user_id,
                UserDiscountUsage.discount_id == discount.id
            ).count()
            
            can_apply, _ = discount.can_apply_to_order(order_amount, user_usage_count)
            
            if can_apply:
                discount_data = discount.to_dict()
                discount_data['estimated_discount'] = discount.calculate_discount(order_amount) if order_amount > 0 else 0
                available_discounts.append(discount_data)
        
        return available_discounts
    
    def get_discount_usage_stats(self, discount_id: int) -> Dict:
        """Get usage statistics for a discount"""
        discount = self.session.query(Discount).get(discount_id)
        if not discount:
            return {}
        
        # Get usage details
        usages = self.session.query(UserDiscountUsage).filter(
            UserDiscountUsage.discount_id == discount_id
        ).all()
        
        unique_users = len(set(usage.user_id for usage in usages))
        total_uses = len(usages)
        
        return {
            'discount_info': discount.to_dict(),
            'total_uses': total_uses,
            'unique_users': unique_users,
            'usage_rate': (total_uses / discount.usage_limit * 100) if discount.usage_limit else 0,
            'recent_usages': [usage.to_dict() for usage in usages[-10:]]  # Last 10 usages
        }
    
    def create_discount(self, discount_data: Dict) -> Discount:
        """Create a new discount"""
        discount = Discount(**discount_data)
        self.session.add(discount)
        self.session.flush()  # To get the ID
        return discount
    
    def update_discount(self, discount_id: int, discount_data: Dict) -> Optional[Discount]:
        """Update an existing discount"""
        discount = self.session.query(Discount).get(discount_id)
        if not discount:
            return None
        
        for key, value in discount_data.items():
            if hasattr(discount, key):
                setattr(discount, key, value)
        
        return discount
    
    def delete_discount(self, discount_id: int) -> bool:
        """Soft delete a discount"""
        discount = self.session.query(Discount).get(discount_id)
        if not discount:
            return False
        
        discount.is_active = False
        return True
    
    def get_admin_discounts(self, page: int = 1, per_page: int = 20, search: str = '') -> Tuple[List[Dict], int]:
        """Get discounts for admin panel with pagination"""
        query = self.session.query(Discount)
        
        if search:
            query = query.filter(
                (Discount.code.ilike(f'%{search}%')) |
                (Discount.name.ilike(f'%{search}%'))
            )
        
        total = query.count()
        discounts = query.order_by(Discount.created_at.desc()).offset(
            (page - 1) * per_page
        ).limit(per_page).all()
        
        return [discount.to_dict() for discount in discounts], total