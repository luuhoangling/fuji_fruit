"""Review repository"""

from app.repositories import BaseRepository
from app.models import ProductReview
from sqlalchemy import desc
from typing import List, Optional, Tuple


class ReviewRepository(BaseRepository):
    """Repository for ProductReview operations"""
    
    def __init__(self, db_session=None):
        super().__init__(ProductReview)
        self.db_session = db_session
    
    def get_product_reviews(self, product_id: int, page: int = 1, per_page: int = 10) -> Tuple[List[ProductReview], int]:
        """Get reviews for a product with pagination"""
        query = self.model.query.filter_by(product_id=product_id)\
                     .order_by(desc(ProductReview.created_at))
        
        total = query.count()
        offset = (page - 1) * per_page
        reviews = query.offset(offset).limit(per_page).all()
        
        return reviews, total
    
    def create_review(self, product_id: int, user_name: str, rating: int, content: str) -> ProductReview:
        """Create a new review"""
        review = ProductReview(
            product_id=product_id,
            user_name=user_name,
            rating=rating,
            content=content
        )
        self.create(**review.__dict__)
        return review
    
    def get_admin_reviews(self, product_id: int = None, page: int = 1, per_page: int = 20) -> Tuple[List[ProductReview], int]:
        """Get reviews for admin panel"""
        query = self.model.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        query = query.order_by(desc(ProductReview.created_at))
        
        total = query.count()
        offset = (page - 1) * per_page
        reviews = query.offset(offset).limit(per_page).all()
        
        return reviews, total


# Global instance
review_repo = ReviewRepository()