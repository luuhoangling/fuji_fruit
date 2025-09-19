"""Stock repository"""

from app.repositories import BaseRepository
from app.models import ProductStock
from app.extensions import db
from typing import Optional


class StockRepository(BaseRepository):
    """Repository for ProductStock operations"""
    
    def __init__(self, db_session=None):
        super().__init__(ProductStock)
        self.db_session = db_session
    
    def get_by_product_id(self, product_id: int) -> Optional[ProductStock]:
        """Get stock by product ID"""
        return self.model.query.filter_by(product_id=product_id).first()
    
    def get_for_update(self, product_id: int) -> Optional[ProductStock]:
        """Get stock with row lock for updates"""
        return self.model.query.filter_by(product_id=product_id)\
                   .with_for_update().first()
    
    def decrease_stock(self, product_id: int, qty: int) -> bool:
        """Decrease stock quantity"""
        stock = self.get_for_update(product_id)
        if not stock or stock.qty_on_hand < qty:
            return False
        
        stock.qty_on_hand -= qty
        return True
    
    def increase_stock(self, product_id: int, qty: int):
        """Increase stock quantity"""
        stock = self.get_for_update(product_id)
        if stock:
            stock.qty_on_hand += qty
        else:
            # Create new stock record if not exists
            stock = ProductStock(product_id=product_id, qty_on_hand=qty)
            db.session.add(stock)
    
    def set_stock(self, product_id: int, qty: int):
        """Set stock quantity"""
        stock = self.get_by_product_id(product_id)
        if stock:
            stock.qty_on_hand = qty
        else:
            stock = ProductStock(product_id=product_id, qty_on_hand=qty)
            db.session.add(stock)
        return stock


# Global instance
stock_repo = StockRepository()