#!/usr/bin/env python3
"""
Migration script to remove discount-related features from the database
This script removes:
1. discount_amt and discount_code columns from orders table
2. discounts table
3. user_discount_usage table
"""

import os
import sys
import logging
from config import Config

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import after adding to path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_migration():
    """Remove discount-related features from database"""
    try:
        # Create database connection using config
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        
        with engine.connect() as conn:
            logger.info("Starting discount removal migration...")
            
            # Start transaction
            trans = conn.begin()
            
            try:
                # 1. Drop user_discount_usage table if exists
                logger.info("Dropping user_discount_usage table...")
                conn.execute(text("DROP TABLE IF EXISTS user_discount_usage"))
                
                # 2. Drop discounts table if exists  
                logger.info("Dropping discounts table...")
                conn.execute(text("DROP TABLE IF EXISTS discounts"))
                
                # 3. Remove discount_amt column from orders table
                logger.info("Removing discount_amt column from orders table...")
                try:
                    conn.execute(text("ALTER TABLE orders DROP COLUMN discount_amt"))
                except OperationalError as e:
                    if "doesn't exist" in str(e) or "Unknown column" in str(e):
                        logger.info("discount_amt column already removed or doesn't exist")
                    else:
                        raise
                
                # 4. Remove discount_code column from orders table
                logger.info("Removing discount_code column from orders table...")
                try:
                    conn.execute(text("ALTER TABLE orders DROP COLUMN discount_code"))
                except OperationalError as e:
                    if "doesn't exist" in str(e) or "Unknown column" in str(e):
                        logger.info("discount_code column already removed or doesn't exist")
                    else:
                        raise
                
                # Commit transaction
                trans.commit()
                logger.info("Migration completed successfully!")
                
            except Exception as e:
                # Rollback on error
                trans.rollback()
                logger.error(f"Migration failed: {e}")
                raise
                
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logger.info("=== Discount Removal Migration ===")
    run_migration()
    logger.info("=== Migration Complete ===")