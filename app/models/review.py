"""Review model"""

from app.extensions import db
from app.models import BaseModel


class ProductReview(BaseModel):
    """Product review model"""
    __tablename__ = 'product_reviews'
    
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.SmallInteger, nullable=False)  # 1-5
    content = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<ProductReview {self.id} - {self.rating}/5>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_name': self.user_name,
            'rating': self.rating,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }