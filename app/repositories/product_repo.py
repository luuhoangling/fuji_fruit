"""Product repository"""

from app.repositories import BaseRepository
from app.models import Product, ProductEffectivePrice, ProductRating, ProductStock, Category
from app.extensions import db
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple


class ProductRepository(BaseRepository):
    """Repository for Product operations"""
    
    def __init__(self, db_session=None):
        super().__init__(Product)
        self.db_session = db_session
    
    def get_by_slug(self, slug: str) -> Optional[Product]:
        """Get product by slug"""
        return self.model.query.filter_by(slug=slug, is_active=True).first()
    
    def get_effective_price(self, product_id: int) -> Optional[ProductEffectivePrice]:
        """Get product with effective price from view"""
        return ProductEffectivePrice.query.filter_by(id=product_id).first()
    
    def get_effective_price_for_update(self, product_id: int) -> Optional[float]:
        """Get effective price with row lock for order creation"""
        result = db.session.query(ProductEffectivePrice.effective_price)\
            .filter_by(id=product_id)\
            .with_for_update()\
            .first()
        return float(result[0]) if result else None
    
    def search_products(self, 
                       query: str = '', 
                       category_slug: str = None,
                       category_id: int = None,
                       price_min: float = None,
                       price_max: float = None,
                       sort: str = 'newest',
                       page: int = 1,
                       per_page: int = 24) -> Tuple[List[Dict], int]:
        """Search products with filters and pagination"""
        
        # Base query with effective price
        base_query = db.session.query(
            ProductEffectivePrice,
            ProductRating.avg_rating,
            ProductRating.review_count,
            ProductStock.qty_on_hand
        ).outerjoin(
            ProductRating, ProductEffectivePrice.id == ProductRating.product_id
        ).outerjoin(
            ProductStock, ProductEffectivePrice.id == ProductStock.product_id
        )
        
        # Text search
        if query:
            base_query = base_query.filter(
                or_(
                    ProductEffectivePrice.name.ilike(f'%{query}%'),
                    ProductEffectivePrice.short_desc.ilike(f'%{query}%')
                )
            )
        
        # Category filter
        if category_slug or category_id:
            if category_slug:
                category = Category.query.filter_by(slug=category_slug).first()
                if category:
                    category_id = category.id
            
            if category_id:
                # Join with product_categories table
                base_query = base_query.join(
                    Product, ProductEffectivePrice.id == Product.id
                ).join(
                    Product.categories
                ).filter(Category.id == category_id)
        
        # Price range filter
        if price_min is not None:
            base_query = base_query.filter(ProductEffectivePrice.effective_price >= price_min)
        if price_max is not None:
            base_query = base_query.filter(ProductEffectivePrice.effective_price <= price_max)
        
        # Sorting
        if sort == 'price_asc':
            base_query = base_query.order_by(asc(ProductEffectivePrice.effective_price))
        elif sort == 'price_desc':
            base_query = base_query.order_by(desc(ProductEffectivePrice.effective_price))
        elif sort == 'name_asc':
            base_query = base_query.order_by(asc(ProductEffectivePrice.name))
        elif sort == 'name_desc':
            base_query = base_query.order_by(desc(ProductEffectivePrice.name))
        elif sort == 'oldest':
            base_query = base_query.order_by(asc(ProductEffectivePrice.created_at))
        else:  # newest (default)
            base_query = base_query.order_by(desc(ProductEffectivePrice.created_at))
        
        # Get total count
        total = base_query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        results = base_query.offset(offset).limit(per_page).all()
        
        # Format results
        products = []
        for product, avg_rating, review_count, qty_on_hand in results:
            product_dict = product.to_dict()
            product_dict['in_stock'] = (qty_on_hand or 0) > 0
            product_dict['rating'] = {
                'avg': float(avg_rating) if avg_rating else None,
                'count': review_count or 0
            }
            products.append(product_dict)
        
        return products, total
    
    def get_product_detail(self, slug: str) -> Optional[Dict]:
        """Get detailed product info by slug"""
        # Get product with effective price
        result = db.session.query(
            ProductEffectivePrice,
            ProductRating.avg_rating,
            ProductRating.review_count,
            ProductStock.qty_on_hand
        ).outerjoin(
            ProductRating, ProductEffectivePrice.id == ProductRating.product_id
        ).outerjoin(
            ProductStock, ProductEffectivePrice.id == ProductStock.product_id
        ).filter(
            ProductEffectivePrice.slug == slug,
            ProductEffectivePrice.is_active == True
        ).first()
        
        if not result:
            return None
        
        product, avg_rating, review_count, qty_on_hand = result
        
        # Get actual Product object for images
        actual_product = Product.query.filter_by(slug=slug).first()
        
        # Format response
        product_dict = product.to_dict()
        product_dict['original_price'] = float(product.price)
        product_dict['stock'] = {
            'in_stock': (qty_on_hand or 0) > 0,
            'qty': qty_on_hand or 0
        }
        product_dict['rating'] = {
            'avg': float(avg_rating) if avg_rating else None,
            'count': review_count or 0
        }
        
        # Get additional images
        if actual_product and actual_product.images:
            product_dict['images'] = [img.image_url for img in actual_product.images]
        else:
            product_dict['images'] = [product.image_url] if product.image_url else []
        
        return product_dict
    
    def get_admin_products(self, search: str = '', page: int = 1, per_page: int = 20):
        """Get products for admin with stock info"""
        query = db.session.query(
            Product,
            ProductStock.qty_on_hand
        ).outerjoin(
            ProductStock, Product.id == ProductStock.product_id
        )
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.short_desc.ilike(f'%{search}%')
                )
            )
        
        query = query.order_by(desc(Product.created_at))
        
        # Get total count
        total = query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        results = query.offset(offset).limit(per_page).all()
        
        products = []
        for product, qty_on_hand in results:
            product_dict = product.to_dict(include_relations=True)
            product_dict['stock'] = {
                'qty_on_hand': qty_on_hand or 0,
                'in_stock': (qty_on_hand or 0) > 0
            }
            products.append(product_dict)
        
        return products, total
    
    def get_latest_products(self, limit: int = 12) -> List[Product]:
        """Get latest products ordered by creation date"""
        return self.model.query.filter_by(is_active=True)\
            .order_by(desc(self.model.created_at))\
            .limit(limit)\
            .all()
    
    def get_products_on_sale(self, limit: int = 12) -> List[Product]:
        """Get products currently on sale"""
        from datetime import datetime
        now = datetime.utcnow()
        
        return self.model.query.filter(
            and_(
                self.model.is_active == True,
                self.model.sale_price.isnot(None),
                or_(
                    self.model.sale_start.is_(None),
                    self.model.sale_start <= now
                ),
                or_(
                    self.model.sale_end.is_(None),
                    self.model.sale_end >= now
                )
            )
        ).order_by(desc(self.model.created_at))\
         .limit(limit)\
         .all()
    
    def get_by_category_with_filters(self, 
                                   category_id: int,
                                   search_term: str = None,
                                   price_min: float = None,
                                   price_max: float = None,
                                   sort_by: str = 'newest',
                                   page: int = 1,
                                   per_page: int = 24) -> Tuple[List[Product], int]:
        """Get products by category with filters and pagination"""
        
        # Import the association table model
        from app.models.product import ProductCategory
        
        # Base query for products in the category using proper join
        base_query = self.model.query.join(ProductCategory).filter(
            and_(
                self.model.is_active == True,
                ProductCategory.category_id == category_id
            )
        )
        
        # Text search filter
        if search_term:
            base_query = base_query.filter(
                or_(
                    self.model.name.ilike(f'%{search_term}%'),
                    self.model.short_desc.ilike(f'%{search_term}%')
                )
            )
        
        # Price range filter
        if price_min is not None:
            base_query = base_query.filter(self.model.price >= price_min)
        if price_max is not None:
            base_query = base_query.filter(self.model.price <= price_max)
        
        # Sorting
        if sort_by == 'price_asc':
            base_query = base_query.order_by(asc(self.model.price))
        elif sort_by == 'price_desc':
            base_query = base_query.order_by(desc(self.model.price))
        elif sort_by == 'name_asc':
            base_query = base_query.order_by(asc(self.model.name))
        elif sort_by == 'name_desc':
            base_query = base_query.order_by(desc(self.model.name))
        elif sort_by == 'oldest':
            base_query = base_query.order_by(asc(self.model.created_at))
        else:  # newest (default)
            base_query = base_query.order_by(desc(self.model.created_at))
        
        # Get total count
        total = base_query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        products = base_query.offset(offset).limit(per_page).all()
        
        return products, total

    def get_all_with_filters(self, 
                           search_term: str = None,
                           category_id: int = None,
                           price_min: float = None,
                           price_max: float = None,
                           sort_by: str = 'newest',
                           page: int = 1,
                           per_page: int = 24) -> Tuple[List[Product], int]:
        """Get all products with filters and pagination"""
        
        # Base query for all active products
        base_query = self.model.query.filter(self.model.is_active == True)
        
        # Category filter
        if category_id:
            from app.models.product import ProductCategory
            base_query = base_query.join(ProductCategory).filter(
                ProductCategory.category_id == category_id
            )
        
        # Text search filter
        if search_term:
            base_query = base_query.filter(
                or_(
                    self.model.name.ilike(f'%{search_term}%'),
                    self.model.short_desc.ilike(f'%{search_term}%')
                )
            )
        
        # Price range filter
        if price_min is not None:
            base_query = base_query.filter(self.model.price >= price_min)
        if price_max is not None:
            base_query = base_query.filter(self.model.price <= price_max)
        
        # Sorting
        if sort_by == 'price_asc':
            base_query = base_query.order_by(asc(self.model.price))
        elif sort_by == 'price_desc':
            base_query = base_query.order_by(desc(self.model.price))
        elif sort_by == 'name_asc':
            base_query = base_query.order_by(asc(self.model.name))
        elif sort_by == 'name_desc':
            base_query = base_query.order_by(desc(self.model.name))
        elif sort_by == 'oldest':
            base_query = base_query.order_by(asc(self.model.created_at))
        else:  # newest (default)
            base_query = base_query.order_by(desc(self.model.created_at))
        
        # Get total count
        total = base_query.count()
        
        # Pagination
        offset = (page - 1) * per_page
        products = base_query.offset(offset).limit(per_page).all()
        
        return products, total


# Global instance
product_repo = ProductRepository()