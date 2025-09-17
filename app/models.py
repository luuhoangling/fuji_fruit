from app.db import get_base
import logging

logger = logging.getLogger(__name__)

# Auto-mapped model classes will be available after database initialization
# These will be populated by the automap_base after reflecting the database

class Models:
    """Container for all auto-mapped model classes"""
    
    def __init__(self):
        self._base = None
        self._initialized = False
    
    def init_models(self):
        """Initialize model classes from reflected database tables"""
        try:
            self._base = get_base()
            self._initialized = True
            logger.info("Models initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
            raise
    
    @property
    def base(self):
        """Get the automap base"""
        if not self._initialized:
            raise RuntimeError("Models not initialized. Call init_models() first.")
        return self._base
    
    # User and Auth related models
    @property
    def Users(self):
        """Get the Users model class"""
        return self.base.classes.users
    
    @property
    def Roles(self):
        """Get the Roles model class"""
        return self.base.classes.roles
    
    # Address model
    @property
    def Addresses(self):
        """Get the Addresses model class"""
        return self.base.classes.addresses
    
    # Product catalog models
    @property
    def Categories(self):
        """Get the Categories model class"""
        return self.base.classes.categories
    
    @property
    def Brands(self):
        """Get the Brands model class"""
        return self.base.classes.brands
    
    @property
    def Products(self):
        """Get the Products model class"""
        return self.base.classes.products
    
    @property
    def ProductVariants(self):
        """Get the ProductVariants model class"""
        return self.base.classes.product_variants
    
    @property
    def ProductMedia(self):
        """Get the ProductMedia model class"""
        return self.base.classes.product_media
    
    @property
    def ProductCategories(self):
        """Get the ProductCategories model class"""
        return self.base.classes.product_categories
    
    @property
    def InventoryStocks(self):
        """Get the InventoryStocks model class"""
        return self.base.classes.inventory_stocks
    
    # Cart and Order models
    @property
    def Carts(self):
        """Get the Carts model class"""
        return self.base.classes.carts
    
    @property
    def CartItems(self):
        """Get the CartItems model class"""
        return self.base.classes.cart_items
    
    @property
    def Orders(self):
        """Get the Orders model class"""
        return self.base.classes.orders
    
    @property
    def OrderItems(self):
        """Get the OrderItems model class"""
        return self.base.classes.order_items
    
    @property
    def OrderStatuses(self):
        """Get the OrderStatuses model class"""
        return self.base.classes.order_statuses
    
    @property
    def PaymentMethods(self):
        """Get the PaymentMethods model class"""
        return self.base.classes.payment_methods
    
    @property
    def PaymentTransactions(self):
        """Get the PaymentTransactions model class"""
        return self.base.classes.payment_transactions
    
    # Coupon model (optional)
    @property
    def Coupons(self):
        """Get the Coupons model class"""
        return self.base.classes.coupons
    
    # Store models (existing)
    @property
    def Stores(self):
        """Get the Stores model class"""
        return self.base.classes.stores
    
    @property
    def StoreHours(self):
        """Get the StoreHours model class"""
        return self.base.classes.store_hours

# Global instance to be used throughout the application
models = Models()